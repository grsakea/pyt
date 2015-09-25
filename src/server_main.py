#!/usr/bin/env python3

import tweepy
import os.path
import server_bottle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from models import Tweet
from server_storage import Storage


class StreamHandler(StreamListener):
    def __init__(self, store):
        self.tweets = store.tweets
        super().__init__()

    def on_status(self, status):
        self.tweets.append(Tweet(status))
        return True

    def on_error(self, status):
        print(status)
        return True

    def on_timeout(self):
        print("Timeouted")


def load_auth():
    f = open(os.path.expanduser('~/.config/pyt'))

    consKey = f.readline().replace('\n', '')
    consSec = f.readline().replace('\n', '')

    accessTok = f.readline().replace('\n', '')
    accessSecret = f.readline().replace('\n', '')

    f.close()

    auth = OAuthHandler(consKey, consSec)
    auth.set_access_token(accessTok, accessSecret)
    return auth


def start_stream(auth, store):
    l = StreamHandler(store)
    stream = Stream(auth, l)
    stream.userstream(async=True)
    return stream


def main():
    store = Storage()
    auth = load_auth()
    api = tweepy.API(auth)
    st = api.home_timeline(count=200)
    for i in st:
        store.tweets.append(Tweet(i))
    store.tweets.sort()
    print("Tweets Downloaded")
    start_stream(auth, store)
    print("Starting Server")
    server_bottle.launch_server(store)


if __name__ == '__main__':
    main()
