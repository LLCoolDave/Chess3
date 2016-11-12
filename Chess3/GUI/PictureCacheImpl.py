from PyQt5.QtGui import QPixmap
from Chess3 import ARMY_WHITE
import os
import sys


class PictureCacheClass(object):

    def __init__(self):
        self.cached_images = {}
        if getattr(sys, 'frozen', False):
            # running in a bundle
            self.resource_roots = [os.path.abspath(os.path.join(sys._MEIPASS, 'Pictures'))]
        else:
            # running live
            self.resource_roots = [os.path.abspath(os.path.join(__file__, '..', '..', 'Pieces', 'Pictures'))]

    def get_pixmap(self, name, color):
        if (name, color) in self.cached_images:
            return self.cached_images[(name, color)]
        colorstr = 'white' if color == ARMY_WHITE else 'black'
        imagestr = '%s_%s.png' % (name, colorstr)
        for root in self.resource_roots:
            imagefile = os.path.join(root, imagestr)
            if os.path.isfile(imagefile):
                pix = QPixmap(imagefile)
                self.cached_images[(name, color)] = pix
                return pix

        # couldn't find image, use default
        imagefile = os.path.join(self.resource_roots[0], 'Unknown_%s.png' % colorstr)
        pix = QPixmap(imagefile)
        self.cached_images[(name, color)] = pix
        return pix
