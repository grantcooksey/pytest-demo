import logging
import os
import sys

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOG_LEVEL))
formatter = logging.Formatter('[%(levelname)s] %(name)s %(asctime)s - %(message)s')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)
