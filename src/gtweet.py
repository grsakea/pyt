import requests
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QTextBrowser,\
        QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QTextCursor, QIcon
from PyQt5 import QtCore
from datetime import timezone


class StatusWidget(QWidget):
    delete_tweets = pyqtSignal(str)

    def __init__(self, tweet):
        super().__init__()

        self.tid = tweet.status.id
        if hasattr(tweet.status, 'retweeted_status'):
            self.rt = True
            self.st = tweet.status.retweeted_status
            self.rtst = tweet.status
        else:
            self.rt = False
            self.st = tweet.status

        self.initUI(tweet)
        print("-----------------")

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
        html_text = status.text
        pretty_text = status.text

        html_text = html_text.replace("\n", "<br>")
        html_text = html_text.replace("<br><br>", "<br>")
        if hasattr(status, 'extended_entities'):
            for i in status.extended_entities['media']:
                if i['type'] == 'animated_gif':
                    html_text += "<a href={0}> Vid</a>".\
                                 format(i['video_info']['variants'][0]['url'])
                    html_text = html_text.replace(i['url'], '')
                    pretty_text = pretty_text.replace(i['url'], '')
                    pretty_text += " Vid"
                else:
                    html_text += "<a href={0}:orig> Pic</a>".\
                            format(i['media_url_https'])
                    html_text = html_text.replace(i['url'], '')
                    pretty_text = pretty_text.replace(i['url'], '')
                    pretty_text += " Pic"

        if 'urls' in status.entities:
            for i in status.entities['urls']:
                to_rep = orig_text[i['indices'][0]:i['indices'][1]]
                in_place = '<a href="{0}">{1}</a>'.format(i['expanded_url'],
                                                          i['display_url'])
                html_text = html_text.replace(to_rep, in_place)
                pretty_text = pretty_text.replace(to_rep, i['display_url'])

        status.text = html_text

        splitted = pretty_text.split("\n")
        nb = len(splitted)
        for i in splitted:
            nb += int(len(i)/72)
            if len(i) == 0:
                nb -= 1

        print(orig_text)
        return nb

    def add_pic(self):
        if self.rt:
            pict1 = self.getPix(self.st.user.profile_image_url_https, False)
            pict2 = self.getPix(self.rtst.user.profile_image_url_https, True)
            self.lay.addWidget(pict1, 0, 0, 2, 1)
            self.lay.addWidget(pict2, 1, 0)
        else:
            pict = self.getPix(self.st.user.profile_image_url_https, False)
            self.lay.addWidget(pict, 0, 0, 2, 1)

    def add_time(self):
        time = self.st.created_at.replace(tzinfo=timezone.utc)\
                .astimezone(tz=None)
        string = time.strftime("%d/%m - %H:%M")

        self.lay.addWidget(QLabel(string), 0, 3)

    def add_text(self):
        nb_linebreak = self.process_text(self.st)
        text = QTextBrowser()
        text.setHtml(self.st.text)
        text.setOpenExternalLinks(True)
        text.moveCursor(QTextCursor.End)
        if nb_linebreak == 1:
            text.setFixedSize(500, 30)
        elif nb_linebreak == 2:
            text.setFixedSize(500, 48)
        elif nb_linebreak == 3:
            text.setFixedSize(500, 68)
        elif nb_linebreak == 4:
            text.setFixedSize(500, 88)
        else:
            text.setFixedSize(500, 108)

        self.lay.addWidget(text, 1, 1, 1, 3)

    def add_username(self):
        if self.rt:
            name = '<b>' + self.st.user.name + '</b> <i>@' +\
                    self.st.user.screen_name +\
                   '</i> RT by: <b>' + self.rtst.user.name + '</b>'
        else:
            name = "<b>" + self.st.user.name + "</b> <i>@" +\
                    self.st.user.screen_name + "</i>"

        self.lay.addWidget(QLabel(name), 0, 1)

    def add_button(self):
        icon = QIcon.fromTheme("edit-delete")
        self.button = QPushButton(icon, "")
        self.button.pressed.connect(self.send_delete)
        self.lay.addWidget(self.button, 0, 5, -1, 1)

    def send_delete(self):
        if self.rt:
            self.delete_tweets.emit(self.rtst.id_str)
        else:
            self.delete_tweets.emit(self.st.id_str)

    def initUI(self, tweet):
        layout = QGridLayout()
        self.setLayout(layout)
        self.lay = layout

        layout.setColumnStretch(10, 100)

        self.add_pic()
        self.add_time()
        self.add_text()
        self.add_username()
        self.add_button()

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line, 4, 0, 1, -1)

        self.setLayout(layout)

        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
