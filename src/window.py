from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import QTimer
from gtweet import StatusWidget
import http.client
import pickle


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.hide()

        self.tweets = []
        self.fetch_tweets()

        tim = QTimer(self)
        tim.timeout.connect(self.fetch_tweets)
        tim.start(10000)

        self.show()

    def fetch_tweets(self):
        if len(self.tweets) == 0:
            id = 0
        else:
            id = self.tweets[-1].tid

        conn = http.client.HTTPConnection("localhost", 8080)
        conn.request("GET", "/status/from_id/" + str(id))
        resp = conn.getresponse()
        if resp.status == 200:
            tw = pickle.load(resp)
            tw.sort()
            for i in tw:
                self.addTweet(i)

    def initUI(self):
        self.setWindowTitle('Terminator Preferences')

        lay = QVBoxLayout(self)
        scr = QScrollArea(self)
        scr.setWidgetResizable(True)

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
        self.tweets.append(tweet)
        self.lay.insertWidget(0, StatusWidget(tweet))
