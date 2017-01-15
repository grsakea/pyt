from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QProgressDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from gui.gtweet import StatusWidget
import requests
import pickle
from common.cache import Cache
import os.path

lt = os.path.expanduser("~/.config/last_tweet")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # self.hide()

        self.tweets = []
        self.cache = Cache()

        self.fetch_tweets()

        self.show()

    def fetch_tweets(self):
        self.load_tweets()

    def load_tweets(self):
        if len(self.tweets) == 0:
            try:
                f = open(lt, 'r')
                id = int(f.read())
                print(id)
                f.close()
            except Exception as e:
                print(e)
                id = 0
        else:
            id = self.tweets[-1].tid

        r = requests.get("http://127.0.0.2:8080/status/from_id/" + str(id))
        if r.status_code == 200:
            tw = pickle.loads(r.content)
            tw.sort()
            for i in tw:
                for _, j in i.ent['pic']:
                    self.cache.queue_ressource(j)
                for j in i.ent['profile']:
                    self.cache.queue_ressource(j)
            self.cache.fetch_queue()

            for i in tw:
                self.addTweet(i)

    def initUI(self):
        self.setWindowTitle('Twitter Client')
        self.setWindowIcon(QIcon("twitter.svg"))
        QIcon.setThemeName("Adwaita")

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

        but = QPushButton("Refresh")
        lay.addWidget(but)
        but.pressed.connect(self.fetch_tweets)

        self.show()

    def addTweet(self, tweet):
        widget = StatusWidget(tweet, self.cache)

        self.tweets.append(widget)
        widget.delete_tweets.connect(self.deleteTweets)
        self.lay.addWidget(widget)

    def deleteTweets(self, string_id):
        id = int(string_id)
        for i in self.tweets:
            if i.tid <= id:
                self.lay.removeWidget(i)
                i.hide()
        f = open(lt, 'w')
        f.write(string_id)
        f.close()
