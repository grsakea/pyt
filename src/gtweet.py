from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QTextBrowser,\
        QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QTextCursor, QIcon
from PyQt5 import QtCore
from datetime import timezone


class StatusWidget(QWidget):
    delete_tweets = pyqtSignal(str)

    def __init__(self, tweet, cache):
        super().__init__()

        self.tid = tweet.tid
        self.tweet = tweet
        self.cache = cache
        if tweet.rt:
            self.rt = True
            self.st = tweet.status
            self.rtst = tweet.o_status
        else:
            self.rt = False
            self.st = tweet.status

        self.initUI(tweet)

    def getPix(self, url, scaled=False):
        r = self.cache.get_resource(url)
        pi = QPixmap()
        pi.loadFromData(r)
        if scaled:
            pi = pi.scaled(30, 30,
                           transformMode=QtCore.Qt.SmoothTransformation)
        else:
            pi = pi.scaled(60, 60,
                           transformMode=QtCore.Qt.SmoothTransformation)
        pict = QLabel()
        pict.setPixmap(pi)
        return pict

    def choose_video(self, vids):
        chosen = vids['expanded_url']
        max_br = -1
        for i in vids['video_info']['variants']:
            try:
                if i['bitrate'] > max_br:
                    max_br = i['bitrate']
                    chosen = i['url']
            except:
                pass
        return(chosen)

    def process_text(self, status):
        html_text = status.text
        pretty_text = status.text

        html_text = html_text.replace("\n", "<br>")
        html_text = html_text.replace("<br><br>", "<br>")

        for i, j in self.tweet.ent['pic']:
            html_text = html_text.replace(i, " <a href='{0}'>\
                    Pic</a>".format(j))
            pretty_text = pretty_text.replace(i, ' Pic')
        for i, j in self.tweet.ent['vid']:
            html_text = html_text.replace(i, " <a href='{0}'>\
                    Vid</a>".format(j))
            pretty_text = pretty_text.replace(i, ' Vid')
        for i, j, k in self.tweet.ent['url']:
            to_rep = status.text[i[0]:i[1]]
            html_text = html_text.replace(to_rep, "<a href='{0}'>\
                    {1}</a>".format(k, j))
            pretty_text = pretty_text.replace(to_rep, j)

        self.text = html_text

        splitted = pretty_text.split("\n")
        nb = len(splitted)
        for i in splitted:
            nb += int(len(i)/72)
            if len(i) == 0:
                nb -= 1

        return nb

    def add_pic(self):
        if self.rt:
            print(self.tweet.status.user.profile_image_url_https)
            print(self.tweet.o_status.user.profile_image_url_https)
            print(self.tweet.ent['profile'])
            pict1 = self.getPix(self.tweet.ent['profile'][0], False)
            pict2 = self.getPix(self.tweet.ent['profile'][1], True)
            self.lay.addWidget(pict1, 0, 0, 2, 1)
            self.lay.addWidget(pict2, 1, 0)
        else:
            pict = self.getPix(self.tweet.ent['profile'][0], False)
            self.lay.addWidget(pict, 0, 0, 2, 1)

    def add_time(self):
        time = self.st.created_at.replace(tzinfo=timezone.utc)\
                .astimezone(tz=None)
        string = time.strftime("%d/%m - %H:%M")

        self.lay.addWidget(QLabel(string), 0, 3)

    def add_text(self):
        nb_linebreak = self.process_text(self.st)
        text = QTextBrowser()
        text.setHtml(self.text)
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
        name = "<b>" + self.st.user.name + "</b> <i>@" +\
                self.st.user.screen_name + "</i>"

        self.lay.addWidget(QLabel(name), 0, 1)

    def add_button(self):
        icon = QIcon.fromTheme("edit-delete")
        self.button = QPushButton(icon, "")
        self.button.pressed.connect(self.send_delete)
        self.lay.addWidget(self.button, 1, 4)

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
