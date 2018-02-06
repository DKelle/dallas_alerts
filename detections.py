from threading import Thread
from tweet import tweet
import requests
import json
import time
from datetime import datetime
import logging

logging.basicConfig(filename='alerts.log',level=logging.INFO)
def ecoin_value(fsym, low, high):
    info("Initiating worker for {}".format(fsym))
    # Here's an API that returns the value of different crypto currency
    BASE_URL = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(fsym)

    low = True
    while True:
        r = requests.get(BASE_URL)

        try:
            value = json.loads(r.content)['USD']
            info("value for {} is {}".format(fsym, value))

            # We want to tweet as soon as we cross the high threshold
            # And then not again until we fall under the low threshold
            if low and value > high:
                # We just went from being below the low value to above the high value
                # eg, ETH going from 750 -> 900
                low = False
                msg = "{} has risen to {}".format(fsym, value)
                info("TWEETING: {}".format(msg))
                tweet(msg)

            elif not low and value < low:
                # We just went from being above the high value to below the low value 
                # eg, ETH going from 900 -> 750
                low = True
                msg = "{} has fallen to {}".format(fsym, value)
                info("TWEETING: {}".format(msg))
                tweet(msg)

        except Exception as e:
            exc("Thread {} encountered a key error".format(fsym))
            pass

        # Check the price every 5 minutes
        time.sleep(5 * 60)
    
def main():
    logging.info("Starting worker threads!\n\n")
    workers = {"ETH": [750, 900],
            "BTC": [7750, 10000],
            "LTC": [120, 160]}

    for worker in workers:
        Thread(target=ecoin_value, args=(worker, workers[worker][0], workers[worker][1])).start()

def info(msg):
    date = datetime.now()
    logging.info("[{}]: {}".format(date, msg))

def exc(msg):
    date = datetime.now()
    logging.exception("[{}]: {}".format(date, msg))

if __name__ == "__main__":
    main()
