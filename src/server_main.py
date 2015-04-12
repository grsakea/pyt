#!/usr/bin/python3

import time
import socketserver
import http.server
import http.client
import os.path
import pickle
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from models import Tweet

tweets = []


class StreamHandler(StreamListener):

    def on_status(self, status):
        tweets.append(Tweet(status))
        return True

    def on_error(self, status):
        print(status)


class NetworkRequestHandler(http.server.BaseHTTPRequestHandler):

    """ Get every tweet with id > of path"""
    def do_GET(self):
        try:
            if "/status/from_id/" in self.path:
                status_id = int(self.path.replace("/status/from_id/"))
                print(status_id)
                self.send_tweets(status_id)
            else:
                raise Exception("Unknown Request")

        except Exception as ex:
            self.send_response(500)
            self.send_header("Content-type", "stacktrace")
            self.end_headers()

            self.wfile.write(str(ex).encode("utf-8"))

    def send_tweets(self, status_id):
        if tweets[-1].tid <= status_id:
            self.send_response(204)
            self.end_headers()

        else:
            to_send = []

            i = len(tweets) - 1
            while True:
                cur = tweets[i]
                if cur.tid <= status_id or i <= 0:
                    break
                to_send.append(cur)
                i -= 1

            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            pickle.dump(to_send, self.wfile)


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
