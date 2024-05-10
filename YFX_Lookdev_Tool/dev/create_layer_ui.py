#****************************************************************************************************
# content:        Creates the HDRI UI after importing and will be appended to the main ui dynamically.
#                 Also connects all the necessary buttons to its functions.

# dependencies:   PySide2/PyQt, 3dsmax API, main window (qtmax) and maxscript

# how to:         In the HDRI tab type in a name and press create

# todos:          Add a color which can be multiplied on top of the hdri texture

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

import os

import qtmax
from pymxs import runtime as rt

from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject

import create_asset_ui as ca
import create_turntable as ct
import create_camera_ui as cc
import create_main_ui as main_ui
import create_animations as anim

from UI.icons import icons
from UI.icons import tt_icons
from UI.icons import asset_icons
from UI.icons import camera_icons

DIR_PATH = os.path.dirname(__file__)
LAYER_UI_PATH = DIR_PATH + r'\UI\layer_UI.ui'
LAYER_OPTIONS_UI_PATH = DIR_PATH + r'\UI\layer_options_UI.ui'

class LayerUI():
    def __init__(self, parent=None):
        self.wg_util = parent
        self.lyr_number = str(len(self.get_lyr_list()))

# LAYER UI ------------------------------------------------------------------------------------------------------------------------------------------------

    def get_lyr_list(self):
        lyr_list = ct.TT_Setup().get_domeLights()
        return lyr_list

    def check_lyr_name(self, new_lyr_name):
        for lyr in self.get_lyr_list():
            if lyr.name == new_lyr_name:
                QMessageBox.warning(None, 'Warning', 'Layer name already exists!')
                return False

    def create_layer(self, lyr_name, lyr_number):
        layout_layer = self.wg_util.findChild(QVBoxLayout, 'layout_layer')

        self.wg_layer = QtUiTools.QUiLoader().load(LAYER_UI_PATH)
        self.wg_layer.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.wg_layer.setObjectName('wg_layer_' + lyr_name)
        self.wg_layer.lyr_gBox.setTitle(lyr_name)
        self.wg_layer.lyr_gBox.setObjectName('lyr_gBox_' + lyr_name)
        self.wg_layer.btn_path.setObjectName('btn_path_' + lyr_name)
        self.wg_layer.line_hdri.setObjectName('line_hdri_' + lyr_name)
        self.wg_layer.btn_remove.setObjectName('btn_remove_' + lyr_name)
        self.wg_layer.btn_enable.setObjectName('btn_enable_' + lyr_name)
        self.wg_layer.btn_options.setObjectName('btn_options_' + lyr_name)
        layout_layer.insertWidget(lyr_number, self.wg_layer)

        btn_remove = self.wg_util.findChild(QPushButton, 'btn_remove_' + lyr_name)
        btn_remove.clicked.connect(lambda: self.remove_layer(lyr_name))
        btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr_name)
        btn_enable.clicked.connect(lambda: self.isolate_layer(lyr_name))
        btn_path = self.wg_util.findChild(QPushButton, 'btn_path_' + lyr_name)
        btn_path.clicked.connect(lambda: self.browseHDRI(lyr_name))
        btn_options = self.wg_util.findChild(QPushButton, 'btn_options_' + lyr_name)
        btn_options.clicked.connect(lambda: self.layer_options_ui(lyr_name))

    def remove_layer(self, lyr_name):
        ct.TT_Setup().remove_domeLight(lyr_name)
        layout_layer = self.wg_util.findChild(QVBoxLayout, 'layout_layer')
        wg_layer = self.wg_util.findChild(QWidget, 'wg_layer_' + lyr_name)
        wg_layer.deleteLater()

        # Reposition Groupboxes
        index = 1
        for lyr in self.get_lyr_list():
            wg_layer = self.wg_util.findChild(QWidget, 'wg_layer_' + lyr.name)
            layout_layer.insertWidget(index, wg_layer)
            index = index + 1

    def toggle_layer(self, lyr):    # Specially for the case when checking the scene
        btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr)
        btn_enable.setChecked(True)

    def isolate_layer(self, lyr_current):
        for lyr in self.get_lyr_list():
            btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr.name)
            if lyr.name == lyr_current:
                ct.TT_Setup().enable_domeLight(lyr.name)
                #Fix Camera names
                domeLight = rt.getNodeByName(lyr.name)
                if domeLight.texmap != None:
                    bitmap = domeLight.texmap
                    if bitmap.name.split('_')[-1] == 'S':
                        for node in rt.scenematerials:
                             if node.name == lyr_current + '_ScreenMap':
                                rt.setUseEnvironmentMap = True
                                rt.environmentMap = node
                                rt.viewport.DispBkgImage = False
                                rt.redrawViews()

                    elif bitmap.name.split('_')[-1] == 'N':
                        for node in rt.scenematerials:
                             if node.name == lyr_current + '_GreyBG':
                                rt.setUseEnvironmentMap = True
                                rt.environmentMap = node
                                rt.viewport.DispBkgImage = False
                                rt.redrawViews()
                                
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
            self.enable_options(lyr_name)

        # Change HDRI
        ct.TT_Setup().create_hdri_bitmap(lyr_name, hdri_path[0])

    def get_wg_layer_index(self, lyr_name):
        layout_layer = self.wg_util.findChild(QVBoxLayout, 'layout_layer')
        for i in range(1, layout_layer.count()):
            layout_item = layout_layer.itemAt(i).widget()
            if lyr_name in layout_item.objectName():
                return(i)

# LAYER OPTIONS UI ------------------------------------------------------------------------------------------------------------------------------------------------

    def enable_options(self, lyr_name):
        line_hdri = self.wg_util.findChild(QLineEdit, 'line_hdri_' + lyr_name)
        if line_hdri.displayText != '':
            btn_options = self.wg_util.findChild(QPushButton, 'btn_options_' + lyr_name)
            btn_options.setEnabled(True)

    def layer_options_ui(self, lyr_name):
        self.wg_options = QtUiTools.QUiLoader().load(LAYER_OPTIONS_UI_PATH)
        self.wg_options.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        lyr_index = self.get_wg_layer_index(lyr_name)
        self.wg_options.btn_apply.clicked.connect(lambda: self.layer_options_ui_confirm(lyr_name, lyr_index))
        self.wg_options.cBox_background.currentTextChanged.connect(self.toggle_ground_gBox)
        self.wg_options.show()
        
        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                bitmap = domeLight.texmap

                self.wg_options.setWindowTitle(lyr_name + ' - HDRI Options')
                self.wg_options.line_rename.setText(lyr_name)
                self.wg_options.cBox_invisible.setChecked(domeLight.invisible)
                self.wg_options.sBox_multiplier.setValue(domeLight.multiplier)
                self.wg_options.sBox_rotation.setValue(anim.get_dome_rotation(domeLight))

                self.wg_options.sBox_posX.setValue(bitmap.ground_position[0])
                self.wg_options.sBox_posY.setValue(bitmap.ground_position[1])
                self.wg_options.sBox_posZ.setValue(bitmap.ground_position[2])
                self.wg_options.sBox_radius.setValue(bitmap.ground_radius)
                self.check_background_option(bitmap)

    def check_background_option(self, bitmap):
        if bitmap.ground_on:
            self.wg_options.cBox_background.setCurrentIndex(3)

        elif bitmap.name.split('_')[-1] == 'S':
            self.wg_options.cBox_background.setCurrentIndex(1)

        elif bitmap.name.split('_')[-1] == 'N':
            self.wg_options.cBox_background.setCurrentIndex(2)

        else:
            self.wg_options.cBox_background.setCurrentIndex(0)

    def set_background_option(self, domeLight):
        if domeLight.texmap != None:
            if 'Ground' in self.wg_options.cBox_background.currentText():
                pos_x = self.wg_options.sBox_posX.value()
                pos_y = self.wg_options.sBox_posY.value()
                pos_z = self.wg_options.sBox_posZ.value()
                radius = self.wg_options.sBox_radius.value()
                ct.TT_Setup().set_ground_projection(domeLight, pos_x, pos_y, pos_z, radius)

            elif 'Screen' in self.wg_options.cBox_background.currentText():
                self.wg_options.cBox_invisible.setChecked(True)
                ct.TT_Setup().set_screen_background(domeLight)

            elif 'Grey' in self.wg_options.cBox_background.currentText():
                self.wg_options.cBox_invisible.setChecked(True)
                ct.TT_Setup().set_grey_background(domeLight)

            else:
                ct.TT_Setup().set_default_background(domeLight)
        else:
            QMessageBox.warning(None, 'Warning', 'Add a HDRI-Map first')

    def layer_options_ui_confirm(self, lyr_name, lyr_index):
        new_lyr_name = self.wg_options.line_rename.displayText()
        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                domeLight.invisible = self.wg_options.cBox_invisible.isChecked()
                domeLight.multiplier = self.wg_options.sBox_multiplier.value()
                self.set_background_option(domeLight)
                anim.dome_rotation(domeLight, self.wg_options.sBox_rotation.value())

                if lyr_name != new_lyr_name and self.check_lyr_name(new_lyr_name) != False:
                    domeLight.name = new_lyr_name
                    self.rename_confirm(lyr_name, lyr_index, new_lyr_name)
                    self.wg_options.close()

                elif lyr_name == new_lyr_name:
                    self.wg_options.close()

    def toggle_ground_gBox(self):
        if 'Ground' in self.wg_options.cBox_background.currentText():
            self.wg_options.gBox_groundProj.setEnabled(True)
        else:
            self.wg_options.gBox_groundProj.setEnabled(False)

    def rename_confirm(self, lyr_name, lyr_index, new_lyr_name):

        wg_layer = self.wg_util.findChild(QWidget, 'wg_layer_' + lyr_name)
        btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + lyr_name)
        isolate = btn_enable.isChecked()

        wg_layer.deleteLater()
        self.create_layer(new_lyr_name, lyr_index)

        domeLight = rt.getNodeByName(new_lyr_name)
        self.getHDRI(domeLight)
        domeLight.texmap.name = domeLight.texmap.name.replace(lyr_name, new_lyr_name)

        for node in rt.scenematerials:
            if lyr_name in node.name:
                node.name = node.name.replace(lyr_name, new_lyr_name)

        new_btn_enable = self.wg_util.findChild(QPushButton, 'btn_enable_' + new_lyr_name)
        new_btn_enable.setChecked(isolate)

