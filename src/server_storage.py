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

    def add_resource(self, url):
        if url not in self.resource:
            r = requests.get(url, stream=True)
            name = url[url.rfind('/'):]
            print(name)
            with open('/tmp' + name) as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
