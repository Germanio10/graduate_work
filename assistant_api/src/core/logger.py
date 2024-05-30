import logging
import sys

import logging_loki

loki = logging_loki.LokiHandler(
    url='http://loki:3100/loki/api/v1/push',
    tags={"application": "assistant_api"},
)
sh = logging.StreamHandler(sys.stdout)

logger = logging.getLogger("assistant_api")
logger.addHandler(loki)
logger.addHandler(sh)
logger.setLevel(logging.INFO)
