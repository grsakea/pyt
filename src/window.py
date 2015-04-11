from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from gtweet import gTweet


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Terminator Preferences')

        layout = QVBoxLayout()

        label1 = QLabel("LOL")
        label2 = QLabel("L0L")
        label3 = QLabel("1O1")

        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(label3)

        self.setLayout(layout)
        self.lol = layout

        self.show()

    def addTweet(self, tweet):
        self.lol.addWidget(gTweet(tweet))
