import logging
from datetime import datetime

logging.basicConfig(filename='alerts.log',level=logging.INFO)

class Logger():
    def info(self, msg):
        date = datetime.now()
        logging.info("[{}]: {}".format(date, msg))

    def exc(self, msg):
        date = datetime.now()
        logging.exception("[{}]: {}".format(date, msg))
