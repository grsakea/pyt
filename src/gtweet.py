from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import requests


class StatusWidget(QWidget):
    def __init__(self, tweet):
        super().__init__()
        self.initUI(tweet)

    def initUI(self, tweet):
        st = tweet.status
        r = requests.get(st.user.profile_image_url_https)
        pi = QPixmap()
        pi.loadFromData(r.content)
        lab = QLabel()
        lab.setPixmap(pi)

        layout = QHBoxLayout()
        layout.addWidget(lab)
        layout.addWidget(QLabel(st.user.name))
        layout.addWidget(QLabel(st.text))
        self.setLayout(layout)
