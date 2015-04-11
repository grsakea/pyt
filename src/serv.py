#!/usr/bin/python3

import socketserver
import os.path
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

tweets = []


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
        print(self.request.recv(1024))


def main():

    f = open(os.path.expanduser('~/.config/pyt'))

    consKey = f.readline().replace('\n', '')
    consSec = f.readline().replace('\n', '')

    accessTok = f.readline().replace('\n', '')
    accessSecret = f.readline().replace('\n', '')

    f.close()

    auth = OAuthHandler(consKey, consSec)
    auth.set_access_token(accessTok, accessSecret)

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
