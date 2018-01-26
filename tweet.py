import tweepy

def main():
    debug = True

    CONSUMER_KEY='bnXEsSCGN3hKdMX4Ef8aZAtbQ'
    ACCESS_KEY='956737875340681216-CI1MQS397hDYzVr6HZIOqvvvM1XRZ4L'

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

        tweet = 'test234'

        if debug:
            print 'Tweeting line:', tweet
        api.update_status(tweet)

    elif debug:
        print 'Could not find secrets'

if __name__ == '__main__':
    main()
