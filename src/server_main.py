#!/usr/bin/env python

import tweepy
import os.path
import server_bottle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from models import Tweet
from server_storage import Storage

store = Storage()


class StreamHandler(StreamListener):
    def __init__(self):
        self.tweets = store.tweets

    def on_status(self, status):
        self.tweets.append(Tweet(status))
        return True

    def on_error(self, status):
        print(status)


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


def start_stream(auth):
    l = StreamHandler()
    stream = Stream(auth, l)
    stream.userstream(async=True)


def main():
    auth = load_auth()
    api = tweepy.API(auth)
    st = api.home_timeline(count=20)
    for i in st:
        store.tweets.append(Tweet(i))
    store.tweets.sort()
    print("Tweets Downloaded")
    print(store.tweets[-1].tid)

    # start_stream(auth)

    print("Starting Server")
    server_bottle.launch_server(store)


if __name__ == '__main__':
    main()
