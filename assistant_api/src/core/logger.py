import logging
import logging_loki

handler = logging_loki.LokiHandler(
    url='http://loki:3100/loki/api/v1/push',
    tags={"application": "assistant_api"},
)

logger = logging.getLogger('assistant')
logger.addHandler(handler)
logger.error(
    "Something happend"
)

