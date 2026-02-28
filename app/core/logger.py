import logging
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        return json.dumps(log_record)


logger = logging.getLogger("secureshare")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())

logger.addHandler(handler)