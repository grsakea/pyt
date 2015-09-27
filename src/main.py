#!/usr/bin/env python3

import sys
import window
from PyQt5.QtWidgets import QApplication
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    startGUI()


def startGUI():
    app = QApplication(sys.argv)
    ex = window.MainWindow()
    ex.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
