from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from gtweet import StatusWidget
import requests
import pickle


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.hide()

        self.tweets = []

        self.fetch_tweets()
        self.tim = QTimer(self)
        self.tim.timeout.connect(self.fetch_tweets)
        self.tim.start(60000)

        self.show()

    def fetch_tweets(self):
        if len(self.tweets) == 0:
            try:
                f = open("last_tweet", 'r')
                id = int(f.read())
                print(id)
                f.close()
            except:
                id = 0
        else:
            id = self.tweets[-1].tid

        r = requests.get("127.0.0.2:8080/status/from_id" + str(id))
        if r.status_code == 200:
            tw = pickle.load(r.data)
            tw.sort()
            for i in tw:
                self.addTweet(i)

    def initUI(self):
        self.setWindowTitle('Twitter Client')
        QIcon.setThemeName("Faenza-Dark")

        lay = QVBoxLayout(self)
        scr = QScrollArea(self)
        scr.setWidgetResizable(True)
        scr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        lay2 = QVBoxLayout()
        self.setLayout(lay)
        placehold = QWidget()
        lay.addWidget(scr)
        scr.setWidget(placehold)
        placehold.setLayout(lay2)
        self.lay = lay2

        lay2.setSpacing(0)
        lay.setSpacing(0)
        lay.setContentsMargins(0, 0, 0, 0)

        self.show()

    def addTweet(self, tweet):
        widget = StatusWidget(tweet)

        self.tweets.append(widget)
        widget.delete_tweets.connect(self.deleteTweets)
        self.lay.addWidget(widget)

    def deleteTweets(self, string_id):
        id = int(string_id)
        for i in self.tweets:
            if i.tid <= id:
                self.lay.removeWidget(i)
                i.hide()
        f = open("last_tweet", 'w')
        f.write(string_id)
        f.close()
