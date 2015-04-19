from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout


class StatusWidget(QWidget):
    def __init__(self, tweet):
        super().__init__()
        self.initUI(tweet)

    def initUI(self, tweet):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(tweet.status.text))
        self.setLayout(layout)
