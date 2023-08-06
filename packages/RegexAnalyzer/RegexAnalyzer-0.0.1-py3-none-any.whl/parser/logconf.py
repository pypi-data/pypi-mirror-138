"""
Define logging here so it can be consistent across processes as long as this is imported
"""
# Builtin imports
import logging
import logging.handlers
import sys
import json

CONF = json.load(open('conf.json'))

FORMAT = '%(asctime)-15s %(levelname)s %(module)s %(message)s'
logging.basicConfig(level="DEBUG" if CONF["debug"] else "INFO",
                    format=FORMAT,
                    handlers=[
                        logging.handlers.RotatingFileHandler(
                            filename="regex-parser.log",
                            maxBytes=20 * 1000 * 1000,
                            backupCount=5
                        ), logging.StreamHandler(sys.stdout)
                    ])