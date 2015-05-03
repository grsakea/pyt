from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from gtweet import StatusWidget
import http.client
import pickle


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.tweets = []
        self.fetch_tweets(0)

    def fetch_tweets(self, id):
        print(id)
        conn = http.client.HTTPConnection("localhost", 8080)
        conn.request("GET", "/status/from_id/" + str(id))
        resp = conn.getresponse()
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
        self.lay.insertWidget(0, StatusWidget(tweet))
