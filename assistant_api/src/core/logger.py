import logging
import sys

logger = logging.getLogger("event_api")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
)
sh.setFormatter(formatter)

logger.addHandler(sh)
