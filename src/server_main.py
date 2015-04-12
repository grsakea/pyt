#!/usr/bin/python3

import time
import socketserver
import http.server
import http.client
import os.path
import pickle
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

tweets = []
read_status = {}


class Tweet():
    def __init__(self, status):
        self.status = status
        self.tid = status.id
        self.read = False


class StreamHandler(StreamListener):

    def on_status(self, status):
        tweets.append(Tweet(status))
        print(status.text)
        """print(status.id)"""
        print("---------- " + str(len(tweets)))
        return True

    def on_error(self, status):
        print(status)


class NetworkRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html>THis is not done yet</html>".encode('utf-8'))


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


def main():
    "auth = load_auth()"

    "start_stream(auth)"
    start_server()


def start_stream(auth):
    l = StreamHandler()
    stream = Stream(auth, l)
    stream.userstream(async=True)


def start_server():
    import threading
    address = ('localhost', 8080)
    server = socketserver.TCPServer(address, NetworkRequestHandler)
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    # Connect to the server
    conn = http.client.HTTPConnection("localhost", 8080)
    conn.request("GET", "5880")
    resp = conn.getresponse()
    print(resp.status)
    print(resp.read())
    time.sleep(500)


if __name__ == '__main__':
    main()
