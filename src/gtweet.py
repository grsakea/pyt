import requests
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QTextBrowser, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore


class StatusWidget(QWidget):
    def __init__(self, tweet):
        super().__init__()
        self.initUI(tweet)

    def getPix(self, url, scaled=False):
        r = requests.get(url)
        pi = QPixmap()
        pi.loadFromData(r.content)
        if scaled:
            pi = pi.scaled(24, 24,
                           transformMode=QtCore.Qt.SmoothTransformation)
        pict = QLabel()
        pict.setPixmap(pi)
        return pict

    def process_text(self, status):
        orig_text = status.text
        print((status.entities))
        if hasattr(status, 'extended_entities'):
            print("OMG!!! ", status.extended_entities)
        if 'urls' in status.entities:
            for i in status.entities['urls']:
                to_rep = orig_text[i['indices'][0]:i['indices'][1]]
                in_place = '<a href="' + i['expanded_url'] + '">' +\
                           i['display_url'] + "</a>"
                status.text = status.text.replace(to_rep, in_place)

                print("TO REP: " + to_rep + " " + in_place)
        print("Orig : " + orig_text)

    def initUI(self, tweet):
        layout = QGridLayout()

        if hasattr(tweet.status, 'retweeted_status'):
            st = tweet.status.retweeted_status
            rtst = tweet.status
            pict1 = self.getPix(st.user.profile_image_url_https, False)
            pict2 = self.getPix(rtst.user.profile_image_url_https, True)
            layout.addWidget(pict1, 0, 0, 2, 1)
            layout.addWidget(pict2, 1, 0)
            name = '<b>' + st.user.name + '</b> <i>@' + st.user.screen_name +\
                   '</i> RT by: <b>' + rtst.user.name + '</b>'
        else:
            st = tweet.status
            pict = self.getPix(st.user.profile_image_url_https, False)
            layout.addWidget(pict, 0, 0, 2, 1)
            name = "<b>" + st.user.name + "</b> <i>@" + st.user.screen_name +\
                   "</i>"

        self.process_text(st)

        text = QTextBrowser()
        text.setHtml(st.text)
        text.setOpenExternalLinks(True)

        layout.addWidget(QLabel(name), 0, 1)
        layout.addWidget(text, 1, 1)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, 4, 0, 1, -1)

        self.setLayout(layout)

        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        print("-----------------")
