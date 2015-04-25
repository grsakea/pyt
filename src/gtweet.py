from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
import requests


class StatusWidget(QWidget):
    def __init__(self, tweet):
        super().__init__()
        self.initUI(tweet)

    def initUI(self, tweet):

        layout = QGridLayout()

        if hasattr(tweet.status, 'retweeted_status'):
            print("Hello")
            st = tweet.status.retweeted_status
            pict1 = self.getPix(st.user.profile_image_url_https, False)
            pict2 = self.getPix(tweet.status.user.profile_image_url_https, True)
            layout.addWidget(pict1, 0, 0)
            layout.addWidget(pict2, 1, 0)
        else:
            st = tweet.status
            pict = self.getPix(st.user.profile_image_url_https, False)
            layout.addWidget(pict, 0, 0)

        text = QLabel(st.text)

        layout.addWidget(QLabel(st.user.name), 1, 1)
        layout.addWidget(text, 0, 1)
        self.setLayout(layout)

    def getPix(self, url, scaled=False):
        print(url)
        r = requests.get(url)
        pi = QPixmap()
        pi.loadFromData(r.content)
        if scaled:
            pi = pi.scaled(24, 24)
        pict = QLabel()
        pict.setPixmap(pi)
        return pict
