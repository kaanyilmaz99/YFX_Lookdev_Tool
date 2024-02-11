# Dynamically builds the "Layers" into the main_ui 

import os
import sys
import importlib


import qtmax
from pymxs import runtime as rt

from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject


import create_turntable as ct
import create_main_ui as main_ui

from UI import icons
from UI import tt_icons


sys.path.append(os.path.dirname(__file__))
importlib.reload(ct)
importlib.reload(main_ui)

DIR_PATH = os.path.dirname(__file__)
LAYER_UI_PATH = DIR_PATH + r'\UI\layer_UI.ui'
RENAME_UI_PATH = DIR_PATH + r'\UI\rename_UI.ui'


class LayerUI():
    def __init__(self):
        main_window = qtmax.GetQMaxMainWindow()
        self.wg_util = main_window.findChild(QtWidgets.QDockWidget, 'KY_TT')
        self.lyr_number = str(len(self.get_lyr_list()))

    def check_lyr_name(self, new_lyr_name):
        # Check if LayerName already exists
        for lyr in self.get_lyr_list():
            if lyr.name == new_lyr_name:
                QMessageBox.warning(None, 'Warning', 'Name already exists!')
                return False

    def get_lyr_list(self):
        lyr_list = ct.TT_Setup().get_domeLights()
        return lyr_list

    def create_layer(self, lyr_name, lyr_number):
        vLayout = self.wg_util.findChild(QVBoxLayout, 'vLayout')

        self.wg_layer = QtUiTools.QUiLoader().load(LAYER_UI_PATH)
        self.wg_layer.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wg_layer.lyr_gBox.setTitle(lyr_name)
        self.wg_layer.lyr_gBox.setObjectName('lyr_gBox_' + lyr_name)
        self.wg_layer.btn_path.setObjectName('btn_path_' + lyr_name)
        self.wg_layer.line_hdri.setObjectName('line_hdri_' + lyr_name)
        self.wg_layer.btn_remove.setObjectName('btn_remove_' + lyr_name)
        self.wg_layer.btn_enable.setObjectName('btn_enable_' + lyr_name)
        self.wg_layer.btn_options.setObjectName('btn_options_' + lyr_name)
        vLayout.insertWidget(lyr_number, self.wg_layer)

        btn_remove = self.wg_util.findChild(QPushButton, 'btn_remove_' + lyr_name)
        btn_remove.clicked.connect(lambda: self.remove_layer(lyr_name))
        btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr_name)
        btn_enable.clicked.connect(lambda: self.isolateLayer(lyr_name))
        btn_path = self.wg_util.findChild(QPushButton, 'btn_path_' + lyr_name)
        btn_path.clicked.connect(lambda: self.browseHDRI(lyr_name))
        btn_options = self.wg_util.findChild(QPushButton, 'btn_options_' + lyr_name)
        btn_options.clicked.connect(lambda: self.options_ui(lyr_name))

    def remove_layer(self, lyr_name):
        # Remove HDRI
        ct.TT_Setup().remove_domeLight(lyr_name)

        # Remove Layer UI
        lyr_gBox = self.wg_util.findChild(QGroupBox, 'lyr_gBox_' + lyr_name)
        lyr_gBox.deleteLater()
        btn_remove = self.wg_util.findChild(QPushButton, 'btn_remove_' + lyr_name)
        btn_remove.clicked.disconnect()

        # Reposition Groupboxes
        vLayout = self.wg_util.findChild(QVBoxLayout, 'vLayout')
        index = 1
        for lyr in self.get_lyr_list():
            lyr_gBox = self.wg_util.findChild(QGroupBox, 'lyr_gBox_' + lyr.name)
            vLayout.insertWidget(index, lyr_gBox)
            index = index + 1

    def toggleLayer(self, lyr):    #Specially for the case when checking the scene
        btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr)
        btn_enable.setChecked(True)

    def isolateLayer(self, lyr_current):
        for lyr in self.get_lyr_list():
            btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr.name)
            if lyr.name == lyr_current:
                ct.TT_Setup().enable_domeLight(lyr.name)
                btn_enable.setChecked(True)
            else:
                btn_enable.setChecked(False)
                ct.TT_Setup().disable_domeLight(lyr.name)

    def getHDRI(self, lyr):
        lyr_name = lyr.name
        lyr_bitmap = lyr.texmap
        hdri_path = lyr_bitmap.HDRIMapName
        line_hdri = self.wg_util.findChild(QLineEdit, 'line_hdri_' + lyr_name)
        line_hdri.setText(hdri_path)

    def browseHDRI(self, lyr_name):
        hdri_path = QFileDialog.getOpenFileName(None, 'Choose HDRI', 'C:\\', 'HDRI File (*.exr *.hdr *.jpg *.png *.tif *.tiff)')
        if hdri_path[0] != '':
            line_hdri = self.wg_util.findChild(QLineEdit, 'line_hdri_' + lyr_name)
            line_hdri.setText(hdri_path[0])

        # Change HDRI
        ct.TT_Setup().create_hdri_bitmap(lyr_name, hdri_path[0])

    def options_ui(self, lyr_name):
        self.wg_options = QtUiTools.QUiLoader().load(RENAME_UI_PATH)
        self.wg_options.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.wg_options.btn_exit.clicked.connect(self.wg_options.close)
        self.wg_options.btn_ok.clicked.connect(lambda: self.options_ui_confirm(lyr_name))
        self.wg_options.show()
        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                bitmap = domeLight.texmap
                self.wg_options.setWindowTitle(lyr_name + ' - Layer Options')
                self.wg_options.line_rename.setText(lyr_name)
                self.wg_options.cBox_invisible.setChecked(domeLight.invisible)
                self.wg_options.sBox_multiplier.setValue(domeLight.multiplier)
                self.wg_options.sBox_rotation.setValue(bitmap.horizontalRotation)

    def options_ui_confirm(self, lyr_name):
        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                bitmap = domeLight.texmap
                bitmap.horizontalRotation = self.wg_options.sBox_rotation.value()
                domeLight.invisible = self.wg_options.cBox_invisible.isChecked()
                domeLight.multiplier = self.wg_options.sBox_multiplier.value()
                # domeLight.name = self.wg_options.line_rename.text()

                # lyr_gBox = self.wg_util.findChild(QGroupBox, 'lyr_gBox_' + lyr_name)
                # lyr_gBox.setTitle(self.wg_options.line_rename.text())
                
                self.wg_options.close()


    # def rename_confirm(self, self.lyr_name):
    #     new_name = self.wg_rename.line_newName.displayText()
    #     for layer in self.lyr_gBoxs:
    #         if layer.objectName() == 'lyr_gBox_' + new_name:
    #             QMessageBox.warning(None, 'Warning', 'Name already exists!')
    #             return None

    #     groupBox = self.findChild(QGroupBox, 'lyr_gBox_' + self.lyr_name)
    #     line_hdri = self.findChild(QLineEdit, 'line_hdri_' + self.lyr_name)
    #     btn_remove = self.findChild(QPushButton, 'btn_remove_' + self.lyr_name)
    #     btn_enable = self.findChild(QPushButton, 'btn_enable_' + self.lyr_name)
    #     btn_path = self.findChild(QPushButton, 'btn_path_' + self.lyr_name)
    #     btn_rename = self.findChild(QPushButton, 'btn_rename_' + self.lyr_name)

    #     groupBox.setObjectName('lyr_gBox_' + new_name)
    #     groupBox.setTitle(new_name)
    #     line_hdri.setObjectName('line_hdri_' + new_name)
    #     btn_remove.clicked.disconnect()
    #     btn_remove.setObjectName('btn_remove_' + new_name)
    #     btn_remove.clicked.connect(lambda: self.remove_layer(new_name))
    #     btn_enable.clicked.disconnect()
    #     btn_enable.setObjectName('btn_enable_' + new_name)
    #     btn_enable.clicked.connect(lambda: self.isolateLayer(new_name))
    #     btn_path.clicked.disconnect()
    #     btn_path.setObjectName('btn_path_' + new_name)
    #     btn_path.clicked.connect(lambda: self.browseHDRI(new_name))
    #     btn_rename.clicked.disconnect()
    #     btn_rename.setObjectName('btn_rename_' + new_name)
    #     btn_rename.clicked.connect(lambda: self.rename_ui(new_name))

    #     ct.TT_Setup().rename_domeLights(self.lyr_name, new_name)
    #     self.wg_rename.close()

