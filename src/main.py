#!/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication
import window

import libnacl.secret
import libnacl.dual
import libnacl.public


def main():
    message = b"TESTTTTT"

    key = libnacl.public.SecretKey()

    box = libnacl.public.Box(key.sk, key.pk)

    encrypted = box.encrypt(message)
    decrypt = box.decrypt(encrypted)

    print(decrypt.decode('utf-8'))


def startGUI():
    app = QApplication(sys.argv)
    ex = window.MainWindow()
    tw = {"text": "bite"}
    ex.addTweet(tw)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
