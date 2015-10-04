from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class MediaWidget(QWidget):
    def __init__(self, media, m_type, cache):
        super().__init__()
        self.setWindowTitle('Twitter Client')
        layout = QGridLayout()
        self.setLayout(layout)
        self.cache = cache
        if m_type == "pic":
            layout.addWidget(self.display_pic(media), 0, 0)
        else:
            layout.addWidget(self.display_vid(media), 0, 0)

    def display_pic(self, url):
        lab = QLabel(self)
        img = self.cache.get_resource(url)
        pix = QPixmap()
        pix.loadFromData(img)
        if (pix.height() > 800 or pix.width() > 800):
            pix = pix.scaledToHeight(800, Qt.SmoothTransformation)

        lab.setPixmap(pix)
        return lab

    def display_vid(self, url):
        self.player = QMediaPlayer()
        self.widget = QVideoWidget()
        self.content = QMediaContent(QUrl(url))
        self.player.setMedia(self.content)
        self.player.play()
        self.player.setVideoOutput(self.widget)

        return self.widget
