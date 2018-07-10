import os
import logging
import logging.config
filepath = os.path.join(os.path.dirname(__file__), 'log.conf')
print(filepath)
logging.config.fileConfig(filepath)
log = logging.getLogger()
log.info("test")
