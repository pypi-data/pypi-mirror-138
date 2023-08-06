from typing import List, Dict, Union, Callable
import logging
from datetime import datetime
import time
import shutil
import os
from enum import Enum
from pathlib import Path, PurePath
from Configs import getConfig
import operator
import json
from config import DEFAULT

config: DEFAULT = getConfig(config_classes=[DEFAULT])
log = logging.getLogger("databasebackupper")

"""
Todo: 
    Refactor: 
        * tidy up, simplfy
"""


class RetentionType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    MANUAL = "manual"


class Backup:
    def __init__(self, path: Union[str, Path], backup_manager: "BackupManager"):
        # path looks like -> "basepath/database_name/retention(daily/weekly/...)/mysql_backup_2012-12-12_23-23.sql"
        self.backup_manager: "BackupManager" = backup_manager
        if isinstance(path, str):
            path = Path(path)
        self.path: Path = path
        self.name: str = path.stem
        self.retention_type: RetentionType = RetentionType(path.parent.stem)

        self.database_name: str = path.parent.parent.stem
        self.creation_time: float = self._parse_filename_for_timestamp(self.name)

    @property
    def age(self):
        return self.backup_manager.retention_get_backup_age[self.retention_type](
            self.creation_time
        )

    def _parse_filename_for_timestamp(self, filename: str) -> float:
        timestamp_string = filename.rstrip(self.backup_manager.backup_file_suffix)
        timestamp_string = timestamp_string.lstrip(
            self.backup_manager.backup_file_prefix
        )
        timestamp_datetime = datetime.strptime(
            timestamp_string, config.TIMESTAMP_FORMAT
        )
        timestamp_unix = time.mktime(timestamp_datetime.timetuple())
        return timestamp_unix

    def to_dict(self, meta_data: bool = False) -> Dict:
        data = {
            "name": self.name,
            "creation_time": self.creation_time,
            "path": self.path,
        }
        if meta_data:
            data = {
                **data,
                "retention_type": self.retention_type,
                "database_name": self.database_name,
            }
        return data

    """
    def to_dict(self):
        return {
            "name": self.name,
            "path": str(self.path),
            "type": str(self.retention_type),
        }
    """


class BackupManager:
    """Manages (List backup, Rotate existing backup, provide file names for new backups) of a single database instance"""

    # mapping of how many backups are kept per retention type
    retention_duration = {
        RetentionType.DAILY: config.RETENTION_KEEP_NUMBER_OF_DAILY_BACKUPS,
        RetentionType.WEEKLY: config.RETENTION_KEEP_NUMBER_OF_WEEKLY_BACKUPS,
        RetentionType.MONTHLY: config.RETENTION_KEEP_NUMBER_OF_MONTHLY_BACKUPS,
        RetentionType.YEARLY: config.RETENTION_KEEP_NUMBER_OF_YEARLY_BACKUPS,
        RetentionType.MANUAL: config.RETENTION_KEEP_NUMBER_OF_MANUAL_BACKUPS,
    }
    # which retention follows one another
    retention_hierachy = {
        RetentionType.DAILY: RetentionType.WEEKLY,
        RetentionType.WEEKLY: RetentionType.MONTHLY,
        RetentionType.MONTHLY: RetentionType.YEARLY,
        RetentionType.YEARLY: None,
        RetentionType.MANUAL: None,
    }

    # shorthandles to calcuate a comparable "age" of backups. Every retention type has its own scale. E.g. daily backups are calculated in days since epoch, weekly in weeks since epoch, ...
    # two backups from the same day/week/month/year will have the same age regardless of the time of creation
    # this is need to detect e.g. "oh, we need no new backup for week 42, there is already one from this week"
    retention_get_backup_age = {
        RetentionType.DAILY: lambda y: (
            datetime.utcfromtimestamp(y) - datetime(1970, 1, 1)
        ).days,
        RetentionType.WEEKLY: lambda y: int(
            (datetime.utcfromtimestamp(y) - datetime(1970, 1, 1)).days / 7
        ),
        RetentionType.MONTHLY: lambda y: (
            datetime.utcfromtimestamp(y).year - datetime(1970, 1, 1).year
        )
        * 12
        + datetime.utcfromtimestamp(y).month
        - datetime(1970, 1, 1).month,
        RetentionType.YEARLY: lambda y: datetime.utcfromtimestamp(y).year
        - datetime(1970, 1, 1).year,
        RetentionType.MANUAL: lambda y: (
            datetime.utcfromtimestamp(y) - datetime(1970, 1, 1)
        ).days,
    }

    def __init__(
        self,
        base_path: str,
        backup_file_prefix: str = "sqlbackup_",
        backup_file_suffix: str = ".sql",
    ):
        self.base_path: Path = Path(base_path)
        self.backup_file_prefix = backup_file_prefix
        self.backup_file_suffix = backup_file_suffix
        # self.create_pathes_if_not_exists()

    def list_backuped_databases(self) -> List[str]:
        """List database names based on available backups and not on available online databases"""
        return [dir.name for dir in self.base_path.iterdir() if dir.is_dir()]

    def list_backups(
        self,
        database_name: str,
        retention_type: RetentionType = None,
        order_by_key: str = "creation_time",
        desc: bool = False,
    ) -> Dict[RetentionType, List[Backup]]:
        if not self._get_base_dir_path_for_database_backups(
            database_name=database_name
        ).is_dir():
            log.warning(
                f"Can not find any backups @ '{self._get_base_dir_path_for_database_backups(database_name=database_name).absolute()}'. Maybe your base path '{self.base_path}' is wrong or there are no backups just yet..."
            )
        backup_lists: Dict[RetentionType, List[Backup]] = {}
        if retention_type:
            r_types = [retention_type]
        else:
            r_types = [t for t in RetentionType]
        for ret_type in r_types:
            backup_lists[ret_type] = []
            path = self._get_dir_path_for_backups_by_retention_type(
                database_name, ret_type
            )
            if not path.is_dir():
                continue
            for file in filter(
                lambda y: y.is_file() and y.name.endswith(self.backup_file_suffix),
                path.iterdir(),
            ):
                backup_lists[ret_type].append(Backup(path=file, backup_manager=self))
        for ret_type, backup_list in backup_lists.items():
            backup_lists[ret_type] = sorted(
                backup_list, key=operator.attrgetter(order_by_key), reverse=desc
            )

        return backup_lists

    def _get_base_dir_path_for_database_backups(self, database_name: str) -> Path:

        return Path(PurePath(self.base_path, database_name))

    def _get_dir_path_for_backups_by_retention_type(
        self, database_name: str, retention_type: RetentionType
    ) -> Path:
        return Path(
            PurePath(
                self._get_base_dir_path_for_database_backups(database_name),
                retention_type.value,
            )
        )

    def generate_backup_filename(self):
        timestamp = datetime.utcfromtimestamp(time.time()).strftime(
            config.TIMESTAMP_FORMAT
        )
        return f"{self.backup_file_prefix if self.backup_file_prefix else ''}{timestamp}{self.backup_file_suffix if self.backup_file_suffix else ''}"

    def get_new_backup_path(
        self, database_name: str, retention_type: RetentionType = RetentionType.MANUAL
    ) -> Path:
        p = Path(
            PurePath(
                self._get_dir_path_for_backups_by_retention_type(
                    database_name, retention_type
                ),
                self.generate_backup_filename(),
            )
        )
        log.debug(f"Try create base dir {p.parent}")
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def _push_backup_to_next_retention_type(
        self, backup: Backup, delete_if_no_target=True
    ):
        next_ret_type = self.retention_hierachy[backup.retention_type]
        if not next_ret_type and delete_if_no_target:
            log.info(
                f"Delete '{backup.path.absolute()}'. No succeeding retention type."
            )
            os.remove(backup.path)
            return
        backup_of_same_age_already_exists_in_next_retention_type = False
        for next_backup in self.list_backups(
            backup.database_name, retention_type=next_ret_type
        )[next_ret_type.value]:
            # loop through all backups of next retation type and check if a backup of same age is allready existent. If no we can move our backup to this retention type
            if next_backup.age == self.retention_get_backup_age[next_ret_type](
                backup.creation_time
            ):
                backup_of_same_age_already_exists_in_next_retention_type = True
        if not backup_of_same_age_already_exists_in_next_retention_type:
            self._move_backup(backup, next_ret_type)
        elif delete_if_no_target:
            log.info(
                f"Delete '{backup.path.absolute()}'. Backup of same age in succeeding retention type already existing."
            )
            os.remove(backup.path)

    def _move_backup(self, backup: Backup, to_retention: RetentionType):
        target_path = Path(
            PurePath(
                self._get_dir_path_for_backups_by_retention_type(
                    database_name=backup.database_name, retention_type=to_retention
                ),
                backup.path.name,
            )
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        log.debug(f"Move '{backup.path.absolute()}' to '{target_path}'")
        shutil.move(src=backup.path, dst=target_path)

        backup.path = target_path
        backup.retention_type = to_retention

    # def _get_retention_type_of_backup(self, backup: Backup):
    #    for ret_type, backups in self.list_backups(backup.database_name).items():
    #        if backup in backups:
    #            return RetentionType(ret_type)

    def rotate_existing_backups(self):
        log.info("Start backup rotating...")
        if not self.base_path.is_dir():
            log.warning(f"No backups to rotate at '{str(self.base_path.absolute())}'")
            return
        for database_base_backup_dir in self.base_path.iterdir():

            if not database_base_backup_dir.is_dir():
                # something is odd here. There is a file in our directory. lets skip this
                continue
            all_backups = self.list_backups(database_name=database_base_backup_dir.name)
            for ret_type in RetentionType:
                # lets loop all retentions type backup directories (daily,weekly,...)
                ret_backups = all_backups[ret_type]
                if len(ret_backups) > self.retention_duration[ret_type]:
                    # we have too much backups in store
                    # ToDo: include RETENTION_ON_COLLISION_KEEP_NEWEST_BACKUP ; Check if there backups of the same "age" and delete accordingly
                    # After we did this, we can start to delete overhanging backups
                    negative_no_of_overhanging_backups = self.retention_duration[
                        ret_type
                    ] - len(ret_backups)
                    overhanging_backups = ret_backups[
                        negative_no_of_overhanging_backups:
                    ]
                    for overhanging_backup in overhanging_backups:
                        self._push_backup_to_next_retention_type(overhanging_backup)
