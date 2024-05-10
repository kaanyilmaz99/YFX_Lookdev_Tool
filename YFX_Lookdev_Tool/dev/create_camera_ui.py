#****************************************************************************************************
# content:        Creates the CameraUI after importing and will be appended to the main ui dynamically.
#                 Also connects all the necessary buttons to its functions.

# dependencies:   PySide2/PyQt, 3dsmax API, main window (qtmax) and maxscript

# how to:         In the Camera tab type in a name and press create

# todos:          Maybe add more camera options

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

import os

import qtmax
from pymxs import runtime as rt

from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject

import create_asset_ui as ca
import create_layer_ui as cl
import create_turntable as ct
import create_main_ui as main_ui

from UI.icons import icons
from UI.icons import tt_icons
from UI.icons import asset_icons
from UI.icons import camera_icons

DIR_PATH = os.path.dirname(__file__)
CAMERA_UI_PATH = DIR_PATH + r'\UI\camera_UI.ui'
LAYER_OPTIONS_UI_PATH = DIR_PATH + r'\UI\camera_options_UI.ui'

class CameraUI():
    def __init__(self, parent=None):
        self.wg_util = parent
        self.cam_number = str(len(self.get_cam_list()))

# CAMERA UI ------------------------------------------------------------------------------------------------------------------------------------------------

    def check_cam_name(self, new_cam_name):
        # Check if CameraName already exists
        for cam in self.get_cam_list():
            if cam.name == new_cam_name:
                QMessageBox.warning(None, 'Warning', 'Camera name already exists!')
                return False

    def get_cam_list(self):
        cam_list = ct.TT_Setup().get_cameras()
        return cam_list

    def create_camera(self, cam_name, cam_number):
        layout_camera = self.wg_util.findChild(QVBoxLayout, 'layout_camera')

        self.wg_camera = QtUiTools.QUiLoader().load(CAMERA_UI_PATH)
        self.wg_camera.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wg_camera.gBox_cam.setTitle(cam_name)
        self.wg_camera.setObjectName('wg_camera_' + cam_name)
        self.wg_camera.gBox_cam.setObjectName('gBox_cam_' + cam_name)
        self.wg_camera.btn_camera.setObjectName('btn_camera_' + cam_name)
        self.wg_camera.btn_lock.setObjectName('btn_lock_' + cam_name)
        self.wg_camera.sBox_focal_length.setObjectName('sBox_focal_length_' + cam_name)
        self.wg_camera.btn_camera_options.setObjectName('btn_camera_options_' + cam_name)
        self.wg_camera.btn_camera_remove.setObjectName('btn_camera_remove_' + cam_name)
        layout_camera.insertWidget(cam_number, self.wg_camera)

        btn_camera_remove = self.wg_util.findChild(QPushButton, 'btn_camera_remove_' + cam_name)
        btn_camera_remove.clicked.connect(lambda: self.remove_camera(cam_name))
        btn_camera = self.wg_util.findChild(QPushButton, 'btn_camera_' + cam_name)
        btn_camera.clicked.connect(lambda: self.isolate_camera(cam_name))
        btn_camera_options = self.wg_util.findChild(QPushButton, 'btn_camera_options_' + cam_name)
        btn_camera_options.clicked.connect(lambda: self.camera_options_ui(cam_name))
        btn_lock = self.wg_util.findChild(QPushButton, 'btn_lock_' + cam_name)
        btn_lock.clicked.connect(lambda: self.toggle_camera_lock(cam_name))
        sBox_focal_length = self.wg_util.findChild(QSpinBox, 'sBox_focal_length_' + cam_name)
        sBox_focal_length.valueChanged.connect(lambda: self.sBox_focal_length_change(cam_name))

    def sBox_focal_length_change(self, cam_name):
        sBox_focal_length = self.wg_util.findChild(QSpinBox, 'sBox_focal_length_' + cam_name)
        value = sBox_focal_length.value()
        ct.TT_Setup().change_cam_focal_length(cam_name, value)
        rt.redrawViews()

    def get_cam_focal_length(self, cam):
        sBox_focal_length = self.wg_util.findChild(QSpinBox, 'sBox_focal_length_' + cam.name)
        sBox_focal_length.setValue(cam.focal_length)

    def remove_camera(self, cam_name):
        # Remove HDRI
        ct.TT_Setup().remove_camera(cam_name)
        layout_camera = self.wg_util.findChild(QVBoxLayout, 'layout_camera')

        # Remove Layer UI
        wg_camera = self.wg_util.findChild(QWidget, 'wg_camera_' + cam_name)
        wg_camera.deleteLater()

        # Reposition Groupboxes
        index = 1
        for cam in self.get_cam_list():
            wg_camera = self.wg_util.findChild(QWidget, 'wg_camera_' + cam.name)
            layout_camera.insertWidget(index, wg_camera)
            index = index + 1

    def toggle_camera(self, cam):    # Specially for the case when checking the scene
        btn_camera = self.wg_util.findChild(QPushButton, 'btn_camera_' + cam)
        btn_camera.setChecked(True)

    def isolate_camera(self, cam_current):
        for cam in self.get_cam_list():
            btn_camera = self.wg_util.findChild(QPushButton, 'btn_camera_' + cam.name)
            if cam.name == cam_current:
                cam.isHidden = False
                camera_ctrl = rt.getNodeByName('LookdevInfo_' + cam.name + '_ctrl')
                for child in camera_ctrl.children:
                    if '_HIDDEN' in child.name:
                        child.isHidden = True
                    else:
                        child.isHidden = False

                btn_camera.setChecked(True)
                ct.TT_Setup().view_camera(cam)
            else:
                cam.isHidden = True
                camera_ctrl = rt.getNodeByName('LookdevInfo_' + cam.name + '_ctrl')
                for child in camera_ctrl.children:
                    child.isHidden = True

                btn_camera.setChecked(False)

    def lock_camera(self, cam):
        btn_lock = self.wg_util.findChild(QPushButton, 'btn_lock_' + cam.name)
        btn_lock.setChecked(True)

    def toggle_camera_lock(self, cam_name):
        btn_lock = self.wg_util.findChild(QPushButton, 'btn_lock_' + cam_name)
        cam = rt.getNodeByName(cam_name)

        if  btn_lock.isChecked():
            rt.setTransformLockFlags(cam, rt.name('all'))
        else:
            rt.setTransformLockFlags(cam, rt.name('none'))

    def get_wg_camera_index(self, cam_name):
        camera_layer = self.wg_util.findChild(QVBoxLayout, 'layout_camera')
        for i in range(1, camera_layer.count()):
            camera_item = camera_layer.itemAt(i).widget()
            if cam_name in camera_item.objectName():
                return(i)

# CAMERA OPTIONS UI ------------------------------------------------------------------------------------------------------------------------------------------

    def camera_options_ui(self, cam_name):
        self.wg_cam_options = QtUiTools.QUiLoader().load(LAYER_OPTIONS_UI_PATH)
        self.wg_cam_options.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        cam_index = self.get_wg_camera_index(cam_name)
        self.wg_cam_options.btn_cam_apply.clicked.connect(lambda: self.camera_options_ui_confirm(cam_name, cam_index))
        self.wg_cam_options.show()
        
        for camera in self.get_cam_list():
            if camera.name == cam_name:
                lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')
                self.wg_cam_options.setWindowTitle(cam_name + ' - Camera Options')
                self.wg_cam_options.line_cam_rename.setText(cam_name)
                self.wg_cam_options.sBox_filmGate.setValue(camera.film_width)
                self.wg_cam_options.cBox_target.setChecked(camera.targeted)

                for child in lookdev_info_ctrl.children:
                    if 'HIDDEN' in child.name:
                        condition = True
                    else:
                        condition = False
                self.wg_cam_options.cBox_hideChart.setChecked(condition)

    def camera_options_ui_confirm(self, cam_name, cam_index):
        new_cam_name = self.wg_cam_options.line_cam_rename.displayText()

        for camera in self.get_cam_list():
            if camera.name == cam_name:

                camera.film_width = self.wg_cam_options.sBox_filmGate.value()
                sBox_focal_length = self.wg_util.findChild(QSpinBox, 'sBox_focal_length_' + cam_name)
                fl_value = sBox_focal_length.value()
                ct.TT_Setup().change_cam_focal_length(cam_name, fl_value)

                if self.wg_cam_options.cBox_target.isChecked():
                    camera_layer = rt.LayerManager.getLayerFromName('0_Cameras')
                    camera.targeted = self.wg_cam_options.cBox_target.isChecked()
                    camera_target = rt.getNodeByName(cam_name + '.Target')
                    camera_layer.addNode(camera_target)
                else:
                    camera.targeted = self.wg_cam_options.cBox_target.isChecked()

                self.toggle_charts(cam_name, self.wg_cam_options.cBox_hideChart.isChecked())

                if cam_name != new_cam_name and self.check_cam_name(new_cam_name) != False:
                    camera.name = new_cam_name
                    self.rename_confirm(cam_name, cam_index, new_cam_name)
                    self.wg_cam_options.close()

                elif cam_name == new_cam_name:
                    self.wg_cam_options.close()

                rt.redrawViews()

    def toggle_charts(self, cam_name, condition):
        lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')
        for child in lookdev_info_ctrl.children:
            child.isHidden = condition
            if condition:
                child.name = child.name + '_HIDDEN'
            else:
                child.name = child.name.replace('_HIDDEN', '')

    def rename_confirm(self, cam_name, cam_index, new_cam_name):
        wg_camera = self.wg_util.findChild(QWidget, 'wg_camera_' + cam_name)
        btn_camera = self.wg_util.findChild(QPushButton, 'btn_camera_' + cam_name)
        isolate = btn_camera.isChecked()

        wg_camera.deleteLater()
        self.create_camera(new_cam_name, cam_index)
        lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')
        for child in lookdev_info_ctrl.children:
            child.name = child.name.replace(cam_name, new_cam_name)

        lookdev_info_ctrl.name = 'LookdevInfo_' + new_cam_name + '_ctrl'
        lookdev_info_layer = rt.LayerManager.getLayerFromName('0_LookdevInfo_' + cam_name)
        lookdev_info_layer.setName('0_LookdevInfo_' + new_cam_name)

        new_btn_camera = self.wg_util.findChild(QPushButton, 'btn_camera_' + new_cam_name)
        new_btn_camera.setChecked(isolate)
