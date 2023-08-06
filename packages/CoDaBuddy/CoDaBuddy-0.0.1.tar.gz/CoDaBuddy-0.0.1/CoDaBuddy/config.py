from Configs import ConfigBase
from typing import Dict, List


class DEFAULT(ConfigBase):
    LOG_LEVEL: str = "INFO"
    RETENTION_KEEP_NUMBER_OF_DAILY_BACKUPS: int = 7
    RETENTION_KEEP_NUMBER_OF_WEEKLY_BACKUPS: int = 4
    RETENTION_KEEP_NUMBER_OF_MONTHLY_BACKUPS: int = 12
    RETENTION_KEEP_NUMBER_OF_YEARLY_BACKUPS: int = 3
    RETENTION_KEEP_NUMBER_OF_MANUAL_BACKUPS: int = 4

    # When deleting old backups and there are two or more backups of the same day/week/month; should be keep the newer or the older backup?
    # When set to 'True', we will keep the newer backup. When set to false we will keep the older backup
    RETENTION_ON_COLLISION_KEEP_NEWEST_BACKUP: bool = True

    BACKUP_DIR: str = "./backups"

    # execution mode can be either terminal, docker or kubernetes
    EXECUTION_MODE: str = "docker"

    # The docker or kubernetes label key to find databases containers to be backed up. (Value of such a label can be "mysql" or "postgres")
    # Info on docker labels https://docs.docker.com/config/labels-custom-metadata/
    # Info on kubernetes labels: https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
    DATABASE_CONTAINER_LABEL_BASE_KEY: str = "backup.dzd-ev.de"

    # If you dont want/can controll the backupper via container labels you can also specify a container name to be backed up
    DATABASE_CONTAINER_NAME: str = None

    # WIP: we need a way to map auths to database identifiers, whcih can be names or labels
    # Databases access: A dict/json of database authenikation. key must be container name for docker or service/deployment name for kubernetes
    # example:
    # {"mysql01":{"user":"root","password":"supersecretpw","host":"127.0.0.1"}}
    # the key "host" is optional and will default to "127.0.0.1"
    # Todo: Create possibility to provide DB auth via docker or kubernetes secrets
    DATABASES_ACCESS: Dict[str, Dict[str, str]] = {}

    # TIMESTAMP_FORMAT format code -> https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
    TIMESTAMP_FORMAT: str = "%Y-%m-%d_%H-%M-%S"
    FAIL_ON_DATABASE_MISSING: bool = True

    # The command prefix to run any docker or kubectl commands inside the to be backuped container
    # `["/bin/bash", "-c"]` will work on the official mysql/mariadb/postgres containers
    BASE_EXECUTER_COMMAND: List[str] = ["/bin/bash", "-c"]
    DOCKER_COMMAND: str = "docker"
    KUBECTL_VALID_WORKLOAD_TYPES: List[str] = ["Deployment", "StatefulSet"]
    KUBECTL_COMMAND: str = "kubectl"
    KUBECTL_NAMESPACE_PARAM: str = "--all-namespaces"
    KUBECTL_DEFAULT_NAMESPACE: str = "default"
    # Where should we search for Workloads that could contain run a Database Pod
