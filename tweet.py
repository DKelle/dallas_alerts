import tweepy
from tweepy.streaming import StreamListener
import json
from logger import Logger

api = None
auth = None
LOG = Logger()

tweets = {}
def main():
    init_api()

def tweet(alert):
    global tweets

    addition = 0
    if alert in tweets:
        addition = tweets[alert] + 1
    tweets[alert] = addition

    debug = False 
    if api == None:
        init_api()

    alert = alert + '({})'.format(addition)
    if debug:
        print 'Tweeting line:', alert 

    try:
        api.update_status(alert)
    except:
        LOG.exc("Encountered error while sending tweet")

def init_api():
    global api
    global auth

    CONSUMER_KEY='bnXEsSCGN3hKdMX4Ef8aZAtbQ'
    ACCESS_KEY='956737875340681216-j0d5LWt8Hb2m6RvP5aM8NImUC23TrsO'

    ACCESS_SECRET=None
    CONSUMER_SECRET=None

    with open('consumer.secret', 'r') as f:
        CONSUMER_SECRET=f.read().rstrip()

    with open('access.secret', 'r') as f:
        ACCESS_SECRET=f.read().rstrip()

    if ACCESS_SECRET and CONSUMER_SECRET:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

    elif debug:
        print 'Could not find secrets'

def monitor_messages(workers):
    LOG.info("About to start monitoring DMs")
    if api == None:
        init_api()
    stream = tweepy.Stream(auth, StdOutListener(workers))
    stream.userstream()

class StdOutListener( StreamListener ):
    def get_status(self):
        msg = ''
        for w in self.workers:
            msg += '{} - {}\n'.format(w.name, w.get_status())

        return msg

    def __init__( self, workers ):
        self.tweetCount = 0
        self.workers = workers

        self.keyword_map = {'status': self.get_status}

    def on_connect( self ):
        print "Connection established!!"

    def on_disconnect( self, notice ):
        print "Connection lost!! : "

    def on_data( self, status ):
        # Did we just get a message?
        status = json.loads(status)
        if 'direct_message' in status:
            dm = status['direct_message']
            if 'text' in dm:
                message = dm['text']

                if 'sender' in dm:
                    if 'screen_name' in dm['sender']:
                        # Who sent us this message?
                        screen_name = dm['sender']['screen_name']
                        # Make sure this message wasn't from us...
                        if not screen_name == "Dallas_Alerts":
                            LOG.info("Recieved DM {} from {}".format(message, screen_name))

                            msg = "Still alive"
                            for keyword in self.keyword_map:
                                if keyword.lower() in message:
                                    msg = self.keyword_map[keyword]()

                            try:
                                api.send_direct_message(screen_name=screen_name, text=msg)
                            except:
                                # This didn't work... Maybe we got rate limited? Doesn't matter. Just tweet.
                                tweet("@{}: {}".format(screen_name, msg))

                # Either someone is querying for a value?

        return True

    def on_error( self, status ):
        print status

if __name__ == '__main__':
    main()
