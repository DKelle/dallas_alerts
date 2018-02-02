from threading import Thread
from tweet import tweet
import requests
import json
import time
from datetime import datetime
import logging

logging.basicConfig(filename='alerts.log',level=logging.INFO)
def ecoin_value(fsym, threshold):
    info("Initiating worker for {}".format(fsym))
    # Here's an API that returns the value of different crypto currency
    BASE_URL = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(fsym)

    while True:
        r = requests.get(BASE_URL)

        try:
            value = json.loads(r.content)['USD']
            info("value for {} is {}".format(fsym, value))

            # Now that we have the value, is it high enough to send an alert?
            if value > threshold:
                msg = "{} has reached {}".format(fsym, value)
                tweet(msg)

                # Don't tweet more than once an hour
                info("Sent alert: {}".format(msg))
                info("{} thread now sleeping...".format(fsym))
                time.sleep(60 * 60)
                info("{} thread Done sleeping".format(fsym))

        except Exception as e:
            exc("Thread {} encountered a key error".format(fsym))
            pass

        # Check the price every 5 minutes
        time.sleep(5 * 60)
    
def main():
    logging.info("Starting worker threads!\n\n")
    workers = {"ETH": 1300,
            "BTC": 15000,
            "LTC": 180}

    for worker in workers:
        Thread(target=ecoin_value, args=(worker, workers[worker])).start()

def info(msg):
    date = datetime.now()
    logging.info("[{}]: {}".format(date, msg))

def exc(msg):
    date = datetime.now()
    logging.exception("[{}]: {}".format(date, msg))

if __name__ == "__main__":
    main()
