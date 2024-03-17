import os
import sys
import webbrowser

from Qt import QtWidgets, QtGui, QtCore, QtCompat


#*******************************************************************
# VARIABLE
TITLE = os.path.splitext(os.path.basename(__file__))[0]


#*******************************************************************
# CLASS
class SimpleUI():
    def __init__(self):
        # BUILD local ui path
        path_ui = ("/").join([os.path.dirname(__file__), "ui", TITLE + ".ui"])

        # LOAD ui with absolute path
        self.wgUtil = QtCompat.loadUi(path_ui)
        self.wgUtil.setWindowTitle('Units Setup')

        self.wgUtil.rBtn_metric.toggled.connect(self.enable_metric)
        self.wgUtil.rBtn_usStandard.toggled.connect(self.enable_usStandard)
        self.wgUtil.rBtn_custom.toggled.connect(self.enable_custom)
        self.wgUtil.rBtn_generic.toggled.connect(self.disable_all_units)
        self.wgUtil.btn_ok.clicked.connect(self.btn_ok_pressed)
        self.wgUtil.btn_cancel.clicked.connect(self.wgUtil.close)
        self.wgUtil.btn_systemSetup.clicked.connect(print('No options yet'))

        # SHOW the UI
        self.wgUtil.show()



    #************************************************************
    # PRESS
    def enable_metric(self):
        self.disable_all_units()
        self.wgUtil.cBox_metric.setEnabled(True)

    def enable_usStandard(self):
        self.disable_all_units()
        self.wgUtil.cBox_usStandard.setEnabled(True)
        self.wgUtil.cBox_usSteps.setEnabled(True)
        self.wgUtil.label_usdefaults.setEnabled(True)
        self.wgUtil.rBtn_Feet.setEnabled(True)
        self.wgUtil.rBtn_Inches.setEnabled(True)

    def enable_custom(self):
        self.disable_all_units()
        self.wgUtil.lEdit_custom.setEnabled(True)
        self.wgUtil.lEdit_customValue.setEnabled(True)
        self.wgUtil.lEdit_customUnits.setEnabled(True)

    def disable_all_units(self):
        self.wgUtil.cBox_metric.setEnabled(False)

        self.wgUtil.cBox_usStandard.setEnabled(False)
        self.wgUtil.cBox_usSteps.setEnabled(False)
        self.wgUtil.label_usdefaults.setEnabled(False)
        self.wgUtil.rBtn_Feet.setEnabled(False)
        self.wgUtil.rBtn_Feet.setChecked(False)
        self.wgUtil.rBtn_Inches.setEnabled(False)
        self.wgUtil.rBtn_Inches.setChecked(False)

        self.wgUtil.lEdit_custom.setEnabled(False)
        self.wgUtil.lEdit_customValue.setEnabled(False)
        self.wgUtil.lEdit_customUnits.setEnabled(False)

    def btn_ok_pressed(self):
        print('Applied Changes')
        self.wgUtil.close()


    def press_help(self):
        webbrowser.open("https://www.alexanderrichtertd.com")


#*******************************************************************
# START
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    classVar = SimpleUI()
    app.exec_()

