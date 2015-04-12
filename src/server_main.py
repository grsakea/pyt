#!/usr/bin/python3

import socketserver
import os.path
import json
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


class NetworkRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        buf = ""
        temp = "0"
        while temp != b"":
            temp = self.request.recv(2048)
            buf += temp.decode('utf-8')
            print(str(temp))
        print(buf)


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
    auth = load_auth()

    start_stream(auth)
    start_server()


def start_stream(auth):
    l = StreamHandler()
    stream = Stream(auth, l)
    stream.userstream(async=True)


def start_server():
    import socket
    import threading
    address = ('localhost', 0)
    server = socketserver.TCPServer(address, NetworkRequestHandler)
    ip, port = server.server_address

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)
    t.start()

    # Connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    message = b'Hello, world'
    s.send(message)


if __name__ == '__main__':
    main()
