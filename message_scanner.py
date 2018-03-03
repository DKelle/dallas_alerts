from os import listdir
from os.path import isfile, join
import os
from tweet import tweet
import time
from logger import Logger

LOG = Logger()
def watch_for_messages():
    while True:
        # Get the current path
        cur_path = os.path.dirname(os.path.realpath(__file__))

        # Check the 'incoming_messages' directory for files
        messages_dir = cur_path + '/incoming_messages'
        messages = ['{}/{}'.format(messages_dir, f) for f in listdir(messages_dir) if isfile(join(messages_dir, f))]

        if len(messages) > 0:
            for message in messages:
                # Read the message out of this file
                with open(message) as f:
                    msg = ' '.join(f.readlines())

                    try:
                        LOG.info('Found incoming message {}'.format(msg))
                        tweet(msg)
                    except:
                        LOG.info("Failed to execute message: {}".format(msg))

                    # Now that we have tweeted out this message, lets delete the file
                    os.remove(f.name)

        time.sleep(15)

if __name__ == "__main__":
    watch_for_messages()
