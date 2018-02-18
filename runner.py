from detections import ecoin_value
from logger import Logger
from worker import Worker
from threading import Thread
from tweet import monitor_messages

LOG = Logger()
def main():
    ecoin_workers = {"ETH": 35,
                "BTC": 500,
                "LTC": 20}

    threads = []
    for worker in ecoin_workers:
        w = Worker(target=ecoin_value, args=(worker, ecoin_workers[worker]), name="{}".format(worker))
        t = Thread(target=w.start, name=w.name)
        t.daemon = True
        threads.append(t)
        t.start()

    # Create the thread that watches for DMs
    dm_worker = Worker(target=monitor_messages, name="DM Worker", args=(threads,)).start()
    Theead(target=dm_worker.start).start()

if __name__ == "__main__":
    LOG.info("runner is starting")
    main()
