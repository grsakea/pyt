from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt5.QtGui import QPixmap


class MediaWidget(QWidget):
    def __init__(self, media, cache):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)
        self.cache = cache
        layout.addWidget(self.display_pic(media), 0, 0)

    def display_pic(self, url):
        lab = QLabel(self)
        img = self.cache.get_resource(url)
        pix = QPixmap()
        pix.loadFromData(img)
        lab.setPixmap(pix)
        return lab
