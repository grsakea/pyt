import requests


class Storage:
    def __init__(self):
        self.tweets = []
        self.tweets_id = set()
        self.resource = {}

    def add_tweet(self, tweet):
        if tweet.tid not in self.tweets_id:
            self.tweets_id.add(tweet.tid)
            self.tweets.append(tweet)
            for _, url in tweet.ent['pic']:
                self.add_resource(url)
            for _, url in tweet.ent['vid']:
                self.add_resource(url)
            for url in tweet.ent['profile']:
                self.add_resource(url)

    def add_resource(self, url):
        print(url)
        if url not in self.resource:
            r = requests.get(url, stream=True)
            self.resource[url] = r.content
