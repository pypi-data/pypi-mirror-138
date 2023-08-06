import logging
from Configs import getConfig
from config import DEFAULT


from executer import Executer
from backup_manager import BackupManager, RetentionType
from container_helper import ContainerHelper
from log import log

config: DEFAULT = getConfig(config_classes=[DEFAULT])
from label import ValidLabels

if __name__ == "__main__":
    # r = BackupManager(base_path="/tmp")
    # log.info(r.list_backups())
    # exit()
    """
    manager = Executer("docker", "mysql")
    mysql = DatabaseBackupper(
        executer=manager, host="127.0.0.1", user="root", password="498zrthfwejfef"
    )
    mysql.compress_backup = False
    # print(mysql.list_databases())
    mysql.backup(retention_type=RetentionType.DAILY)
    mysql.retention.rotate_existing_backups()
    # mysql.restore("redcado","mysqlbackup_2021-12-29_14-19-40")
    """
    print(ValidLabels.list_labels())
