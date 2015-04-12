#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
import window


def main():
    startGUI()


def startGUI():
    app = QApplication(sys.argv)
    ex = window.MainWindow()
    tw = {"text": "bite"}
    ex.addTweet(tw)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
