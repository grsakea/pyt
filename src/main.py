#!/usr/bin/python3

import sys
import window
import http.client
import pickle
from PyQt5.QtWidgets import QApplication


def main():
    startGUI()


def getTweets():
    # Connect to the server
    conn = http.client.HTTPConnection("localhost", 8080)
    conn.request("GET", "/status/from_id/5880")
    resp = conn.getresponse()
    return pickle.load(resp)


def startGUI():
    app = QApplication(sys.argv)
    ex = window.MainWindow()

    lt = getTweets()
    print(len(lt))
    for i in lt:
        ex.addTweet(i)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
