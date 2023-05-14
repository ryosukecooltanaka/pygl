'''

  Standalone Qt app with 3D graphics

  Started 5/13/2023

'''

import numpy as np
import sys
import time
import imageio

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel
)
from PyQt5.QtGui import QPixmap, QImage
from qimage2ndarray import array2qimage

from gl import glWorld

from utils.modeller import Cone

class MyMainWindow(QMainWindow):
    """
    Main GUI window class.
    """

    def __init__(self):
        """
        Constructer of the main GUI window class.
        """

        # run the parental constructor
        super().__init__()

        ### Prepare Q widgets ###
        # define the window geometry
        self.mainSize = (800, 600)
        self.setGeometry(50,50,self.mainSize[0],self.mainSize[1])
        self.setWindowTitle("3D Graphics")

        # set a single label as the central widget.
        # rendered images will be pasted onto this
        self.mainWidget = QLabel("")
        self.mainWidget.setAlignment(Qt.AlignCenter)
        self.mainWidget.setScaledContents(False)
        self.setCentralWidget(self.mainWidget)

        # set a time to allow timed update of the image
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timerCallback)

        ### Prepare OpenGL world and objects ###
        self.world = glWorld(self.mainSize[1], self.mainSize[0])

        # add objects
        img = np.random.randint(0,255,(100,100,3)).astype(np.uint8)
        self.world.addObject(Cone(5,10), img)

        # time stamps
        self.elapsed = 0
        self.started = time.time()

        # start the timer
        self.timer.start()


    def timerCallback(self):
        """
        The callback function of the timer. Render frames and assign it to
        the main QLabel.
        Note that the coordinate system of ndarray and Qt is different.
        """
        self.elapsed = time.time() - self.started
        frame = self.world.renderFrame()
        self.mainWidget.setPixmap(QPixmap.fromImage(array2qimage(frame)))

    def keyPressEvent(self, e):
        """
        Called when key is pressed
        """
        if e.key()==83: # S for left
            self.world.camera.eye[0] -= 1
        if e.key()==70: # F for right
            self.world.camera.eye[0] += 1
        if e.key()==69: # D for backward
            self.world.camera.eye[2] -= 1
        if e.key()==68: # E for forward
            self.world.camera.eye[2] += 1









def main():
    """
    The first function to be called when running the code.
    Create and kick start the window.
    """
    app = QApplication([])
    win = MyMainWindow()
    win.show()
    sys.exit(app.exec_())

# Script to boot the main function
if __name__ == '__main__':
    main()
