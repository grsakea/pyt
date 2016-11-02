import requests


# TODO expire cache to avoid filling the memory
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
            for _, url in tweet.ent['gif']:
                self.add_resource(url)
            for url in tweet.ent['profile']:
                self.add_resource(url)

    def get_tweet(self, sid):
        if sid in self.tweets_id:
            for i in self.tweets:
                if self.tweets[i].tid == sid:
                    return self.tweets[i]
        # Fetch cache

    def add_resource(self, url):
        if url not in self.resource:
            r = requests.get(url, stream=True)
            self.resource[url] = r.content

    def get_resource(self, url):
        if url not in self.resource:
            r = requests.get(url, stream=True)
            self.resource[url] = r.content
            return r.content
        else:
            return self.resource[url]

    def get_multiple_resource(self, urls):
        out = {}
        for i in urls:
            print("-" + i)
            out[i] = self.get_resource(i)
        return out
