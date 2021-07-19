import sys
import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QColorDialog
import pyqtgraph as pg
import numpy as np
import nmrglue as ng


class Ui_MainWindow(object):
    spectra = {}
    current_spectrum = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1450, 920)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = pg.PlotWidget(self.centralwidget)

        # Control Object
        self.c = Control()

        # Contour Spectrum
        # self.graphicsView.setEnabled(False)
        self.graphicsView.setGeometry(QtCore.QRect(190, 70, 1211, 811))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.showGrid(x=True, y=True, alpha=0.5)
        self.graphicsView.getViewBox().invertX(True)
        self.graphicsView.getViewBox().invertY(True)

        # Mouse Location
        self.graphicsView.scene().sigMouseMoved.connect(self.on_mouse_move)

        # P0 Slider
        self.p0_slider = QtWidgets.QSlider(self.centralwidget)
        self.p0_slider.setGeometry(QtCore.QRect(360, 40, 221, 21))
        self.p0_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.p0_slider.setObjectName("p0_slider")

        # P1 Slider
        self.p1_slider = QtWidgets.QSlider(self.centralwidget)
        self.p1_slider.setGeometry(QtCore.QRect(680, 40, 221, 21))
        self.p1_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.p1_slider.setObjectName("p1_slider")

        # Contour Level Control
        self.set_contour_level = QtWidgets.QSpinBox(self.centralwidget)
        self.set_contour_level.setGeometry(QtCore.QRect(240, 30, 71, 31))
        self.set_contour_level.setObjectName("set_contour_level")
        self.set_contour_level.setValue(15)
        self.set_contour_level.valueChanged.connect(self.c.depth)

        # Labels
        self.contour_level_label = QtWidgets.QLabel(self.centralwidget)
        self.contour_level_label.setGeometry(QtCore.QRect(190, 40, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.contour_level_label.setFont(font)
        self.contour_level_label.setObjectName("contour_level_label")
        self.p0_label = QtWidgets.QLabel(self.centralwidget)
        self.p0_label.setGeometry(QtCore.QRect(330, 40, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.p0_label.setFont(font)
        self.p0_label.setObjectName("p0_label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(590, 40, 41, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.p1_label = QtWidgets.QLabel(self.centralwidget)
        self.p1_label.setGeometry(QtCore.QRect(650, 40, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.p1_label.setFont(font)
        self.p1_label.setObjectName("p1_label")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(910, 40, 41, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 70, 171, 211))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.file_label = QtWidgets.QLabel(self.groupBox)
        self.file_label.setGeometry(QtCore.QRect(10, 40, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.file_label.setFont(font)
        self.file_label.setObjectName("file_label")

        # Add Spectrum Button
        self.addButton = QtWidgets.QPushButton(self.groupBox)
        self.addButton.setGeometry(QtCore.QRect(40, 70, 61, 31))
        self.addButton.setObjectName("addButton")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.addButton.setFont(font)
        self.addButton.clicked.connect(self.openFileNameDialog)

        # Remove Spectrum Button
        self.removeButton = QtWidgets.QPushButton(self.groupBox)
        self.removeButton.setGeometry(QtCore.QRect(100, 70, 71, 31))
        self.removeButton.setObjectName("removeButton")
        self.removeButton.setFont(font)
        try:
            self.removeButton.clicked.connect(self.remove_spectrum)
        except AttributeError:
            pass

        # Spectrum Selector
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(40, 35, 131, 31))
        self.comboBox.setObjectName("comboBox")
        self.current_spectrum = self.comboBox.currentData()
        self.comboBox.activated[str].connect(self.on_selection)

        # Color Selector
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 100, 131, 32))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.openColorDialog)

        # Toggle Contours
        self.contourBox = QtWidgets.QCheckBox(self.groupBox)
        self.contourBox.setGeometry(QtCore.QRect(0, 140, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.contourBox.setFont(font)
        self.contourBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.contourBox.setObjectName("contourBox")
        self.contourBox.stateChanged.connect(self.set_spectrum_visibility)

        # Toggle Peaks
        self.peaksBox = QtWidgets.QCheckBox(self.groupBox)
        self.peaksBox.setGeometry(QtCore.QRect(70, 140, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.peaksBox.setFont(font)
        self.peaksBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.peaksBox.setObjectName("peaksBox")

        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(0, 100, 51, 31))
        self.label_5.setObjectName("label_5")
        self.label_5.setFont(font)

        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(0, 170, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(70, 170, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.checkBox_4.setObjectName("checkBox_4")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(40, 10, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1450, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(options=options)
        try:
            if fileName:
                self.add_spectrum(Spectrum(fileName))
        except:
            print('Error: Could not open file')

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.change_color(color.name())

    def add_spectrum(self, spectrum):
        if not spectrum.__str__() in self.spectra:
            for i in range(spectrum.spec_start, spectrum.spec_start + spectrum.spec_depth):
                print(f'Loading isocurve {i - spectrum.spec_start + 1} of {spectrum.spec_depth}')
                self.graphicsView.addItem(spectrum.contours[i])
            self.graphicsView.disableAutoRange()
            self.spectra[spectrum.__str__()] = spectrum
            self.comboBox.addItem(spectrum.__str__())
            self.current_spectrum = spectrum
            self.on_selection()
            #self.display_peaks(spectrum)
        else:
            print('Error: Spectrum is already loaded')

    def remove_spectrum(self):
        s = self.current_spectrum
        try:
            for i in range(s.spec_start, s.spec_start + s.spec_depth):
                self.graphicsView.removeItem(s.contours[i])
            self.spectra.pop(s.__str__())
            spec_index = self.comboBox.currentIndex()
            self.comboBox.removeItem(spec_index)
            self.pushButton_3.setStyleSheet("")
            print(f'Removed {s.__str__()}')
        except:
            print('Error: No spectrum selected')

    def on_selection(self):
        print(self.comboBox.currentText())
        self.current_spectrum = self.spectra[self.comboBox.currentText()]
        self.set_contour_level.setValue(self.current_spectrum.spec_start)
        self.pushButton_3.setStyleSheet(f'background-color: {self.current_spectrum.get_color()}')
        self.contourBox.setChecked(self.current_spectrum.get_visibility())

    def on_mouse_move(self, point):
        p = self.graphicsView.plotItem.vb.mapSceneToView(point)
        # self.pl = pg.PlotDataItem(x=[p.x(), -600], y=[p.y(), 200])
        # self.graphicsView.addItem(self.pl)
        self.label_7.setText(f'x: {round(p.x(), 3)} , y: {round(p.y(), 3)}')

    def change_depth(self, spectrum):
        val = self.set_contour_level.value()
        if val > spectrum.spec_start:
            print(f'spectrum depth: {val}')
            self.graphicsView.removeItem(spectrum.contours[spectrum.spec_start])
            spectrum.spec_start = val
            self.graphicsView.addItem(spectrum.contours[spectrum.spec_start + spectrum.spec_depth])
        elif val < spectrum.spec_start:
            print(f'spectrum depth: {val}')
            self.graphicsView.removeItem(spectrum.contours[spectrum.spec_start + spectrum.spec_depth])
            spectrum.spec_start = val
            self.graphicsView.addItem(spectrum.contours[spectrum.spec_start])

    def change_color(self, color):
        s = self.current_spectrum
        for i in range(len(s.contours)):
            s.contours[i].setPen(color)
        s.set_color(color)
        self.pushButton_3.setStyleSheet(f'background-color: {s.color}')

    def set_spectrum_visibility(self, state=True):
        s = self.current_spectrum
        print(f'{s.__str__()} visibility {True if state==2 else False}')
        for i in range(len(s.contours)):
            if state:
                s.contours[i].setPen(s.get_color())
                s.set_visibility(True)
            else:
                s.contours[i].setPen(None)
                s.set_visibility(False)

    def display_peaks(self, spectrum):
        self.graphicsView.addItem(spectrum.peaks())



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.contour_level_label.setText(_translate("MainWindow", "Level:"))
        self.p0_label.setText(_translate("MainWindow", "P0:"))
        self.p1_label.setText(_translate("MainWindow", "P1:"))
        self.groupBox.setTitle(_translate("MainWindow", "Spectrum"))
        self.file_label.setText(_translate("MainWindow", "File:"))
        self.contourBox.setText(_translate("MainWindow", "Contour"))
        self.peaksBox.setText(_translate("MainWindow", "Peaks"))
        self.checkBox_3.setText(_translate("MainWindow", "X-Slice"))
        self.checkBox_4.setText(_translate("MainWindow", "Y-Slice"))
        self.label_7.setText(_translate("MainWindow", "test"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.removeButton.setText(_translate("MainWindow", "Remove"))
        self.label_5.setText(_translate("MainWindow", " Color:"))


class Spectrum:
    contour_start = 10  # contour level start value
    contour_num = 50  # number of contour levels
    contour_factor = 1.7
    #a = 0
    spec_start = 15
    spec_depth = 15
    pthres = 50000

    def __init__(self, file):
        self.dic, self.data = ng.pipe.read(str(file))
        self.dic, self.data = ng.pipe_proc.rev(self.dic, self.data)
        self.file = file
        self.color = "%06x" % random.randint(0, 0xFFFFFF)
        self.contours = []
        self.display()
        self.contour_visibility = True

    def __str__(self):
        return str(os.path.basename(self.file))

    def display(self):
        self.dic['FDF1QUADFLAG'] = 1.0
        uc_x = ng.pipe.make_uc(self.dic, self.data, dim=1)
        uc_y = ng.pipe.make_uc(self.dic, self.data, dim=0)
        peaks = ng.analysis.peakpick.pick(self.data.real, self.pthres, table=True, algorithm='connected', msep=[0.5, 1.5],
                                          cluster=True)
        self.x0, self.x1 = uc_x.ppm_limits()
        self.y0, self.y1 = uc_y.ppm_limits()
        self.peak_xlocations_ppm = [uc_x.ppm(i) for i in peaks['X_AXIS']]
        self.peak_ylocations_ppm = [uc_y.ppm(i) for i in peaks['Y_AXIS']]
        self.peaks_list = zip(self.peak_xlocations_ppm, self.peak_ylocations_ppm)
        self.data = np.rot90(self.data)

        for x in range(self.contour_num):
            l = self.contour_start * self.contour_factor ** x
            c = pg.IsocurveItem(data=self.data, level=l, pen=self.color)
            c.translate(self.x0, self.y0)
            c.scale((self.x1 - self.x0) / self.data.shape[0], (self.y1 - self.y0) / self.data.shape[1])
            self.contours.append(c)

    def get_xslice(self):
        xslice = self.data[200, :]
        slice_plot = pg.PlotCurveItem(list(range(self.data.shape[1])), xslice / 2000)
        slice_plot.translate(self.x0, self.y0)
        slice_plot.scale((self.x1 - self.x0) / self.data.shape[0], (self.y1 - self.y0) / self.data.shape[1])
        return slice_plot

    def peaks(self):
        peak_plot = pg.ScatterPlotItem(pos=self.peaks_list, pen='w')
        return peak_plot

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

    def get_visibility(self):
        return self.contour_visibility

    def set_visibility(self, state):
        self.contour_visibility = state


class Control:
    def depth(self):
        ui.change_depth(ui.current_spectrum)

    def add(self):
        pass


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

screen = app.primaryScreen()
size = screen.size()
print(size.width())

layout = pg.GraphicsLayout()
ax = pg.PlotItem()
layout.addItem(ax)


def main():
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
