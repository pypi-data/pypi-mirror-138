from typing import List, Dict, Union
import logging
import json
from Configs import getConfig
from pathlib import PurePath, Path
from config import DEFAULT
from executer import Executer
from backup_manager import Backup, BackupManager, RetentionType
from container_helper import Container
from label import ValidLabels, Label

config: DEFAULT = getConfig(config_classes=[DEFAULT])
# log = logging.getLogger("BaseBackupper")
from log import log


class BaseBackupper:
    __compress_backup: bool = True
    add_drop_table: bool = True
    add_drop_database: bool = True
    bin_dump: str = None
    bin_cmd: str = None
    backup_file_prefix: str = None
    backup_file_suffix: str = None
    ignore_databases: List[str] = []

    def get_list_database_command() -> List[str]:
        raise NotImplementedError

    def get_list_user_command() -> List[str]:
        raise NotImplementedError

    def get_backup_command(self, database_name, target_filepath) -> str:
        raise NotImplementedError

    def get_restore_command(self, database_name, source_filepath) -> str:
        raise NotImplementedError

    def get_create_database_command(
        self,
        database_name,
        encoding,
        collation,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        raise NotImplementedError

    def get_create_user_command(
        self,
        username,
        password,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        raise NotImplementedError

    def get_grant_access_to_user_command(
        self,
        username,
        database,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        raise NotImplementedError

    def __init__(self, db_container: Container, target_base_dir: Path = None):
        self.executer = Executer(
            mode=db_container.mode,
            container_name=db_container.name,
            namespace=db_container.kubernetes_namespace,
        )
        # generate target path for backups
        target_dir = Path(
            PurePath(
                target_base_dir
                if target_base_dir
                else db_container.coda_labels[ValidLabels.backup_dir].val,
                db_container.kubernetes_namespace
                if db_container.kubernetes_namespace
                else "",
                db_container.backup_name.replace("/", ""),
            )
        )

        self.manager = BackupManager(
            base_path=target_dir,
            backup_file_prefix=self.backup_file_prefix,
            backup_file_suffix=f"{self.backup_file_suffix}.gz"
            if self.compress_backup
            else self.backup_file_suffix,
        )
        self.manager.retention_duration = {
            RetentionType.DAILY: db_container.coda_labels[
                ValidLabels.retention_daily
            ].val,
            RetentionType.WEEKLY: db_container.coda_labels[
                ValidLabels.retention_weekly
            ].val,
            RetentionType.MONTHLY: db_container.coda_labels[
                ValidLabels.retention_monthly
            ].val,
            RetentionType.YEARLY: db_container.coda_labels[
                ValidLabels.retention_yearly
            ].val,
            RetentionType.MANUAL: db_container.coda_labels[
                ValidLabels.retention_manual
            ].val,
        }

        self.host = db_container.coda_labels[ValidLabels.database_host].val
        self.user = db_container.coda_labels[ValidLabels.database_username].val
        self.password = db_container.coda_labels[ValidLabels.database_password].val
        self.container = db_container
        databases = db_container.coda_labels[ValidLabels.database_names].val
        if isinstance(databases, str):
            self.databases = databases.split(",")
        else:
            self.databases = databases

    @property
    def compress_backup(self):
        return self.__compress_backup

    @compress_backup.setter
    def compress_backup(self, val: bool):
        self.__compress_backup = val
        self.manager.backup_file_suffix = (
            f"{self.backup_file_suffix}.gz" if val else self.backup_file_suffix
        )

    def list_databases(self, show_all: bool = False) -> List[str]:
        result = self.executer.container_exec(command=self.get_list_database_command())

        return [
            database.strip()
            for database in result.decode("utf-8").splitlines()
            if (database.strip() not in self.ignore_databases or show_all)
            and database.strip() != ""
        ]

    def list_users(self) -> List[str]:
        result = self.executer.container_exec(command=self.get_list_user_command())

        return [
            user.strip()
            for user in result.decode("utf-8").splitlines()
            if user.strip() != ""
        ]

    def backup(
        self,
        databases: List[str] = None,
        retention_type: RetentionType = RetentionType.MANUAL,
    ) -> List[Path]:
        log.info(
            f"Start backup of instance '{self.executer.container_name}' databases..."
        )
        if not databases:
            # no certain databases specified. We backup all available databases

            databases = self.list_databases()
            log.debug("No database specified. Will backup all...")
        elif isinstance(databases, str):
            # Caller just provided single database name. Thats ok we can handle that
            databases = [databases]
        backup_pathes = []
        log.debug(f"Following databases will be backuped: {databases}")
        if len(databases) == 0:
            log.warning("No Databases found to backup...")
        for database in databases:
            if not database in self.list_databases():
                msg = f"Database {database} does not exists @ '{self.host}' with user '{self.user}'"
                if config.FAIL_ON_DATABASE_MISSING:
                    raise ValueError(msg)
                else:
                    log.error(msg)
                    return
            filepath = self.manager.get_new_backup_path(
                database_name=database, retention_type=retention_type
            )
            cmd = self.get_backup_command(database, filepath)
            log.info(f"Backup '{database}' to '{filepath.absolute()}'")

            self.executer.container_exec(command=cmd)
            backup_pathes.append(filepath)
        return backup_pathes

    def _find_backup_by_name(self, database_name: str, backup_name: str) -> Dict:
        backup: Backup = None
        for retention_type, backups in self.manager.list_backups(
            database_name=database_name
        ).items():
            backup = next((b for b in backups if b.name == backup_name), None)
            if backup:
                break
        if backup is None:
            raise ValueError(
                f"No backup with name '{backup_name}'  for database '{database_name}' found."
            )
        return backup

    def restore(self, database: str, backup_name: str, dry_run: bool = False):
        log.debug(
            f"Restore order for database '{database}'. backup_name: '{backup_name}'"
        )
        backup: Backup = self._find_backup_by_name(database, backup_name)
        log.debug(f"Found backup to restore: {backup}")
        com = self.get_restore_command(database_name=database)
        self.executer.container_exec(
            command=com,
            prefix=f"{'zcat' if self.compress_backup else 'cat'} <{backup.path.absolute()} |",
            dry_run=dry_run,
        )

    def auto_create(self) -> List[str]:
        """Create databases and users if not existent"""
        if not self.container.coda_labels[ValidLabels.auto_create_enabled].val:
            log.debug(
                f"Skip auto-create for {self.container.name} no '{ValidLabels.auto_create_enabled.key}'-Label"
            )
            return
        created_dbs: List[str] = []
        # First: Lets gather the database username and pw for the user that will execute the database and user creation
        executive_user = self.container.coda_labels[
            ValidLabels.auto_create_user_name
        ].val
        executive_user_pw = self.container.coda_labels[
            ValidLabels.auto_create_user_password
        ].val
        if not executive_user:
            # there is no extra user configures to execute the DB and user creation. we take the current user from label 'username'
            executive_user = self.user
            executive_user_pw = self.password

        # Lets find which databases we have to create, or lets say 'should exists'?
        try:
            to_be_existing_databases_data = json.loads(
                self.container.coda_labels[ValidLabels.auto_create_databases].val
            )
        except:
            log.error(
                f"Can not parse '{ValidLabels.auto_create_databases.key}'-Label. Valid format is json list of obects. got {self.container.coda_labels[ValidLabels.auto_create_databases]}"
            )
            raise
        for to_exist_db in to_be_existing_databases_data:
            # Lets find out which databases allready exists
            existing_databases = self.list_databases()
            existing_users = self.list_users()
            # example value for to_exist_db: 'mydb/myuser/supersavepassw,otherdb/otheruser/savepw'
            database_name = None
            user_name = None
            user_password = None
            if "database" in to_exist_db:
                database_name = to_exist_db["database"].lower()
            else:
                raise ValueError(
                    f"Expeted property 'database' in auto-create config object in label {ValidLabels.auto_create_databases.key}. got '{to_exist_db}'"
                )

            if "user" in to_exist_db:
                user_name = to_exist_db["user"].lower()
            if "password" in to_exist_db:
                user_password = to_exist_db["password"]
            if not user_name:
                user_name = self.user
                user_password = self.password
            # lets go
            touched_user_or_database: bool = False
            if not user_name in existing_users:
                # user does not exists. lets create it
                log.info(f"Create user '{user_name}'@'{self.container.name}' ")
                self.executer.container_exec(
                    command=self.get_create_user_command(
                        username=user_name,
                        password=user_password,
                        executive_db_user_name=executive_user,
                        executive_db_user_pw=executive_user_pw,
                    )
                )
                touched_user_or_database = True
            if not database_name in existing_databases:
                # database does not exists. lets create it
                log.info(f"Create database '{database_name}'@'{self.container.name}' ")

                self.executer.container_exec(
                    command=self.get_create_database_command(
                        database_name,
                        encoding=self.container.coda_labels[
                            ValidLabels.auto_create_encoding
                        ].val,
                        collation=self.container.coda_labels[
                            ValidLabels.auto_create_collation
                        ].val,
                        executive_db_user_name=executive_user,
                        executive_db_user_pw=executive_user_pw,
                    ),
                )
                touched_user_or_database = True

                created_dbs.append(database_name)

            if touched_user_or_database:
                # Grant access for user to DB
                self.executer.container_exec(
                    command=self.get_grant_access_to_user_command(
                        database=database_name,
                        username=user_name,
                        executive_db_user_name=executive_user,
                        executive_db_user_pw=executive_user_pw,
                    ),
                )
        return created_dbs


class MySQLBackupper(BaseBackupper):
    bin_dump: str = "/usr/bin/mysqldump"
    bin_cmd: str = "/usr/bin/mysql"
    backup_file_prefix: str = "sqlbackup_"
    backup_file_suffix: str = ".sql"
    ignore_databases: List[str] = [
        "performance_schema",
        "information_schema",
        "mysql",
        "sys",
    ]
    custom_extra_options: Dict = {"backup": ["--add-drop-table", "--add-drop-database"]}

    def get_backup_command(self, database_name, target_filepath):
        return f"{self.bin_dump} {' '.join(self.custom_extra_options['backup'])} -h{self.host} -u{self.user} --password={self.password} --databases {database_name} {'| gzip -9' if self.compress_backup else ''} >{target_filepath}"

    def get_restore_command(self, database_name):
        return f"""{self.bin_cmd} -u{self.user} -p{self.password} {database_name}"""

    def get_list_database_command(self):
        return f"""{self.bin_cmd} -N -h{self.host} -u{self.user} -p{self.password} -e "SHOW DATABASES;" """

    def get_list_user_command(self):
        return f"""{self.bin_cmd} -N -h{self.host} -u{self.user} -p{self.password} -e "SELECT User FROM mysql.user;" """

    def get_create_database_command(
        self,
        database_name,
        encoding,
        collation,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        # character set UTF8mb4 collate utf8mb4_bin
        command_base = f"""{self.bin_cmd} -N -h{self.host} -u{executive_db_user_name if executive_db_user_name else self.user} -p{executive_db_user_pw if executive_db_user_name else self.password} -e """
        return f"""{command_base} "CREATE DATABASE {database_name} {"CHARACTER SET = '" + encoding + "'" if encoding else ""} {"COLLATE = '" + collation + "'" if collation else ""};" """

    def get_create_user_command(
        self,
        username,
        password,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        log.warning("Create mysql user with no network restrictions (@'%')")
        return f"""{self.bin_cmd} -N -h{self.host} -u{executive_db_user_name if executive_db_user_name else self.user} -p{executive_db_user_pw if executive_db_user_name else self.password} -e "CREATE USER '{username}'@'%' IDENTIFIED BY '{password}';" """

    def get_grant_access_to_user_command(
        self,
        username,
        database,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        log.warning(
            f"Grant access to '{database}' for user '{username}' with no network restrictions (@'%')"
        )
        return f"""{self.bin_cmd} -N -h{self.host} -u{executive_db_user_name if executive_db_user_name else self.user} -p{executive_db_user_pw if executive_db_user_name else self.password} -e "GRANT ALL privileges ON {database}.* TO '{username}'@'%';FLUSH PRIVILEGES;" """


class PostgresBackupper(BaseBackupper):
    bin_dump: str = "/usr/bin/pg_dump"
    bin_cmd: str = "/usr/bin/psql"
    backup_file_prefix: str = "postgresbackup_"
    backup_file_suffix: str = ".sql"
    ignore_databases: List[str] = [
        "postgres",
        "POSTGRES_USER",
        "template0",
        "template1",
    ]

    # https://www.postgresql.org/docs/10/app-pgdump.html
    custom_extra_options: Dict = {"backup": ["--clean"]}

    def get_backup_command(self, database_name, target_filepath):
        return f"env PGPASSWORD={self.password} {self.bin_dump} {' '.join(self.custom_extra_options['backup'])} -h {self.host} -U {self.user} -d {database_name} {'| gzip -9' if self.compress_backup else ''} >{target_filepath}"

    def get_restore_command(self, database_name):
        return f"""env PGPASSWORD={self.password} {self.bin_cmd} -U {self.user} -d {database_name}"""

    def get_list_database_command(self):
        return f"""env PGPASSWORD={self.password} {self.bin_cmd} -U {self.user} -h {self.host} -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;" """

    def get_list_user_command(self):
        return f"""env PGPASSWORD={self.password} {self.bin_cmd} -U {self.user} -h {self.host} -t -c "SELECT usename FROM pg_catalog.pg_user;" """

    def get_create_database_command(
        self,
        database_name,
        encoding,
        collation,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        password_export = f"env PGPASSWORD={executive_db_user_pw if executive_db_user_name else self.password}"
        command_base = f"{self.bin_cmd} -U {executive_db_user_name if executive_db_user_name else self.user} -h {self.host} -t -c "
        create_database_transaction = f"""CREATE DATABASE {database_name} {"ENCODING '"+ encoding + "'" if encoding else ''} {"LC_COLLATE = '"+ collation + "'" if collation else ''};"""
        return f"""{password_export} {command_base} "{create_database_transaction}" """

    def get_create_user_command(
        self,
        username,
        password,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        return f"""env PGPASSWORD={executive_db_user_pw if executive_db_user_name else self.password} {self.bin_cmd} -U {executive_db_user_name if executive_db_user_name else self.user} -h {self.host} -t -c "CREATE USER {username} WITH PASSWORD '{password}'; " """

    def get_grant_access_to_user_command(
        self,
        username,
        database,
        executive_db_user_name=None,
        executive_db_user_pw=None,
    ):
        log.warning(
            f"Grant access to {database} for user {username} with no network restrictions (@'%')"
        )
        password_export = f"env PGPASSWORD={executive_db_user_pw if executive_db_user_name else self.password}"
        command_base = f"{self.bin_cmd} -U {executive_db_user_name if executive_db_user_name else self.user} -h {self.host} -t -c "
        grant_privs_transaction = (
            f"""GRANT ALL PRIVILEGES ON DATABASE {database} TO {username};"""
        )
        return f"""{password_export} {command_base} "{grant_privs_transaction}" """


class Neo4jOnlineBackupper(BaseBackupper):
    bin_dump: str = "/usr/bin/neo4j-admin backup"
    bin_cmd: str = "/usr/bin/neo4j-admin"
    backup_file_prefix: str = "neo4jbackup_"
    backup_file_suffix: str = ".dump"
    ignore_databases: List[str] = [
        "system",
    ]

    def get_backup_command(self, database_name, target_filepath):
        raise NotImplementedError
        return f"export PGPASSWORD=${self.password} && {self.bin_dump} {'--clean' if self.add_drop_database else ''} -h {self.host} -U {self.user} {database_name} {'| gzip -9' if self.compress_backup else ''} >{target_filepath}"

    def list_databases(self, show_all: bool = False) -> List[str]:
        raise NotImplementedError
        result = self.executer.container_exec(
            command=f"""export PGPASSWORD=${self.password} && psql -U {self.user} -h {self.host} -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;" """,
        )
        return [
            database.strip()
            for database in result.decode("utf-8").splitlines()
            if database not in self.ignore_databases or show_all
        ]


class Neo4jOfflineBackupper(BaseBackupper):
    bin_dump: str = "/usr/bin/neo4j-admin dump"
    bin_cmd: str = "/usr/bin/neo4j-admin"
    backup_file_prefix: str = "neo4jbackup_"
    backup_file_suffix: str = ".dump"
    ignore_databases: List[str] = [
        "system",
    ]

    def get_backup_command(self, database_name, target_filepath):
        raise NotImplementedError
        return f"export PGPASSWORD=${self.password} && {self.bin_dump} {'--clean' if self.add_drop_database else ''} -h {self.host} -U {self.user} {database_name} {'| gzip -9' if self.compress_backup else ''} >{target_filepath}"

    def list_databases(self, show_all: bool = False) -> List[str]:
        raise NotImplementedError
        result = self.executer.container_exec(
            command=f"""export PGPASSWORD=${self.password} && psql -U {self.user} -h {self.host} -t -c "SELECT datname FROM pg_database WHERE datistemplate = false;" """,
        )
        return [
            database.strip()
            for database in result.decode("utf-8").splitlines()
            if database not in self.ignore_databases or show_all
        ]
