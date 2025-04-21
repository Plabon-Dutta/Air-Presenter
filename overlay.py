# overlay.py
from PyQt5 import QtWidgets, QtGui, QtCore

class Overlay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.drawing_points = []

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(255, 0, 0, 255), 6)
        painter.setPen(pen)
        for stroke in self.drawing_points:
            for i in range(1, len(stroke)):
                painter.drawLine(stroke[i - 1], stroke[i])

    def add_point(self, point):
        if not self.drawing_points:
            self.drawing_points.append([])
        self.drawing_points[-1].append(QtCore.QPoint(*point))
        self.update()

    def new_stroke(self):
        self.drawing_points.append([])

    def undo(self):
        if self.drawing_points:
            self.drawing_points.pop()
            self.update()
