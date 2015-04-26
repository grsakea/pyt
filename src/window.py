from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from gtweet import StatusWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        self.lol = lay2

        self.show()

    def addTweet(self, tweet):
        self.lol.addWidget(StatusWidget(tweet))
