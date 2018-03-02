from detections import ecoin_value
from logger import Logger
from worker import Worker
from threading import Thread
from tweet import monitor_messages
import simple_server
from message_scanner import watch_for_messages

LOG = Logger()
def main():
    ecoin_workers = {"ETH": 35,
                "BTC": 500,
                "LTC": 20}

    workers = []
    for worker in ecoin_workers:
        w = Worker(target=ecoin_value, args=(worker, ecoin_workers[worker]), name="{}".format(worker))
        t = Thread(target=w.start, name=w.name)
        t.daemon = True
        workers.append(w)
        t.start()

    # Create the thread that watches for DMs
    dm_worker = Worker(target=monitor_messages, name="DM Worker", args=(workers,))
    Thread(target=dm_worker.start).start()

    LOG.info('Creating threads for simple server and message scanner\n\n')
    # Create a thread that listens signals from other programs to tweet messages
    ss_worker = Worker(target=simple_server.run, name="Simple Server Worker")
    Thread(target=ss_worker.start, name="Simple Server").start()
    msg_scanner = Worker(target=watch_for_messages, name="Message Scanner Worker")
    Thread(target=msg_scanner.start, name="Message Scanner").start()

if __name__ == "__main__":
    LOG.info("runner is starting")
    main()
