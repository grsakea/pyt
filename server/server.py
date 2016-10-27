#!/usr/bin/env python3

import threading
import time
import sys
import queue
import tweepy
import os.path
import server.server_bottle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from common.models import Tweet
from server.server_storage import Storage


class StreamHandler(StreamListener):
    def __init__(self, store):
        self.store = store
        super().__init__()

    def on_status(self, status):
        self.store.add_tweet(Tweet(status))
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


def keepalive_stream(stream, q):
    loop = True
    while loop:
        if not stream.running:
            print("restarting")
            stream.userstream(async=True)
        if not q.empty():
            stream.disconnect()
            return
        time.sleep(5)


def startServer():
    store = Storage()
    auth = load_auth()
    api = tweepy.API(auth)
    st = api.home_timeline(count=sys.argv[1])
    for i in st:
        store.add_tweet(Tweet(i))
    store.tweets.sort()
    print("Tweets Downloaded")
    stream = start_stream(auth, store)
    q = queue.Queue()
    t = threading.Thread(target=keepalive_stream, args=(stream, q))
    t.start()
    print("Starting Server")
    server.server_bottle.launch_server(store)
    print("Finished Server")
    q.put("stop")
    t.join()
