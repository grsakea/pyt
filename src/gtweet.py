from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class gTweet(QWidget):
    def __init__(self, tweet):
        super().__init__()
        self.initUI(tweet)

    def initUI(self, tweet):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(tweet['text']))
        layout.addWidget(QLabel(tweet['text']))
        self.setLayout(layout)
