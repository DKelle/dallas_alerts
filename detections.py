from tweet import tweet
import requests
import json
import time
import logger

LOG = logger.Logger()
def ecoin_value(fsym, interval):
    LOG.info("Initiating worker for {}".format(fsym))
    # Here's an API that returns the value of different crypto currency
    BASE_URL = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(fsym)

    interval_count = 0

    # Keep track of which direction this coin is trending
    UP = 1
    DOWN = 2
    direction = UP 
    last_direction = UP
    while True:
        r = requests.get(BASE_URL)

        try:
            value = json.loads(r.content)['USD']
            LOG.info("value for {} is {}".format(fsym, value))

            # Count how many 'intervals' the value currently is
            # eg, value of 100, and interval of 50 has count 2
            next_interval_count = int(value / interval)
            LOG.info("interval for {} is {}".format(fsym, next_interval_count))
            if next_interval_count > interval_count:
                direction = UP

                # Has this coin risen twice in a row?
                if last_direction == UP:
                    msg = "{} has risen to {}".format(fsym, value)
                    LOG.info("TWEETING: {}".format(msg))
                    tweet(msg)

                last_direction = UP


            elif next_interval_count < interval_count:
                direction = DOWN

                # Has this coin dropped twice in a row?
                if last_direction == DOWN:
                    msg = "{} has fallen to {}".format(fsym, value)
                    LOG.info("TWEETING: {}".format(msg))
                    tweet(msg)

                last_direction = DOWN

            interval_count = next_interval_count

        except Exception as e:
            LOG.exc("Thread {} encountered a key error".format(fsym))
            pass

        # Check the price every 5 minutes
        time.sleep(5 * 60)
