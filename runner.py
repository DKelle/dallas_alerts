from detections import ecoin_value
from logger import Logger
from threading import Thread
from tweet import monitor_messages

LOG = Logger()
def main():
    ecoin_workers = {"ETH": 35,
                "BTC": 500,
                "LTC": 20}

    for worker in ecoin_workers:
        Thread(target=ecoin_value, args=(worker, ecoin_workers[worker])).start()

    # Create the thread that watches for DMs
    Thread(target=monitor_messages).start()

if __name__ == "__main__":
    LOG.info("runner is starting")
    main()
