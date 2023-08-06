import logging
from Configs import getConfig

from config import DEFAULT

config: DEFAULT = getConfig(config_classes=[DEFAULT])
logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
    level=config.LOG_LEVEL,
)
log: logging.Logger = logging.getLogger("databasebackupper")
