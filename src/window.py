from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gtweet import StatusWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Terminator Preferences')

        layout = QVBoxLayout()

        self.setLayout(layout)
        self.lol = layout

        self.show()

    def addTweet(self, tweet):
        self.lol.addWidget(StatusWidget(tweet))
