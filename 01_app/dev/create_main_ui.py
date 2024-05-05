#****************************************************************************************************
# content:        Creates the MainUI for the YFX Lookdev Tool. Interacting with it
#                 executes other modules and dynamically adds new UI elements.

# dependencies:   PySide2/PyQt, 3dsMax and maxscript

# how to:         This module can be executed in 3dsMax with the 'Run Script' option directly. 
#                 By default it runs after clicking the 'YFK Turntable' button in the main menu.

# todos:          Add a 'Texture' tab to the MainUI, which will give you the option to
#                 import any texture and connect them to the material automatically.

# version:        v0.9
# date:           2024-11-02

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

import os
import sys
sys.path.append(os.path.dirname(__file__))                       # Can be deleted later
import importlib


import qtmax
from pymxs import runtime as rt

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject


import render_setup as rs
import create_asset_ui as ca
import create_layer_ui as cl
import create_turntable as ct
import create_camera_ui as cc
import default_max_functions as dmf

from UI import icons
from UI import tt_icons
from UI import camera_icons

importlib.reload(dmf)                                            # Can be deleted later 
importlib.reload(cl)                                             # Can be deleted later
importlib.reload(ct)                                             # Can be deleted later
importlib.reload(cc)                                             # Can be deleted later
importlib.reload(ca)                                             # Can be deleted later
importlib.reload(rs)                                             # Can be deleted later

DIR_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = DIR_PATH + r'\UI\turntable_UI.ui'


class YFX_LDEV_UI(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(YFX_LDEV_UI, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('YFX Lookdev Tool')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def initUI(self):
        # Load MainUI
        main_layout = QtWidgets.QVBoxLayout()
        self.wg_util = QtUiTools.QUiLoader().load(MAIN_UI_PATH)
        self.wg_util.setLayout(main_layout)
        self.setWidget(self.wg_util)                                                                                                                                                                                                                                                            
        self.resize(461, 540)

        # Home Tab
        if dmf.get_tt_setup():
            self.wg_util.btn_save_as.setEnabled(True)
            self.wg_util.gBox_import.setEnabled(False)
            self.wg_util.btn_renderout.setEnabled(True)

            output_path = self.get_output_path()
            self.wg_util.lEdit_render.setText(output_path)

        self.wg_util.btn_import.clicked.connect(self.set_import_path)
        self.wg_util.btn_create_tt.clicked.connect(self.setup_tt)
        self.wg_util.line_import.textChanged.connect(self.toggle_create_tt_button)
        self.wg_util.btn_save_as.clicked.connect(self.btn_save_as_pressed)
        self.wg_util.btn_save_incr.clicked.connect(dmf.save_incremental)
        self.wg_util.btn_openFile.clicked.connect(self.btn_open_file_pressed)

        # Asset Tab
        self.wg_util.btn_asset_choose.clicked.connect(self.set_asset_path)
        self.wg_util.line_asset.textChanged.connect(self.enable_add_asset)
        self.wg_util.btn_asset_import.clicked.connect(lambda: self.import_asset(self.wg_util.line_asset.displayText()))

        # Layers Tab
        self.wg_util.new_name_layer.textEdited.connect(self.enable_add_layer)
        self.wg_util.btn_addLyr.clicked.connect(self.add_layer)

        #Cameras Tab
        self.wg_util.line_camera.textEdited.connect(self.enable_add_camera)
        self.wg_util.pBtn_createCamera.clicked.connect(self.add_camera)

        #Render Tab
        self.wg_util.btn_render_settings.clicked.connect(self.toggle_render_settings)
        self.wg_util.btn_aovs.clicked.connect(self.toggle_aovs)
        self.wg_util.btn_render_path.clicked.connect(self.set_render_path)
        self.wg_util.lEdit_render.textChanged.connect(self.enable_render)
        self.wg_util.btn_renderout.clicked.connect(dmf.start_render)

# HOME TAB ---------------------------------------------------------------------------------------------------------------------------------------------------------

    def set_import_path(self):
        object_path = QFileDialog.getOpenFileName(None, 'Import Object', 'C:\\', 
                      'All Formats (*.obj *.fbx *.abc *.max *mdl)')
        self.wg_util.line_import.setText(object_path[0])

    def toggle_create_tt_button(self):
        if self.wg_util.line_import.displayText():
            self.wg_util.btn_create_tt.setEnabled(True)
        else:
            self.wg_util.btn_create_tt.setEnabled(False)

    def btn_open_file_pressed(self):
        open_file = QFileDialog.getOpenFileName(None, 'Open Scene', 'C:\\', '3ds Max (*.max)')
        if open_file[0] != '':
            dmf.open_max_file(open_file[0])

    def btn_save_as_pressed(self):
        save_file = QFileDialog.getSaveFileName(None, 'Save As', 'C:\\', '3ds Max (*.max)')
        save_file = str(save_file[0].replace('.max', ''))
        dmf.save_as(save_file)
        self.wg_util.btn_save_as.setEnabled(False)

    def setup_tt(self):
        object_path = self.wg_util.line_import.displayText()
        dmf.setup_initial_settings()

        self.wg_util.line_import.clear()
        self.wg_util.gBox_import.setEnabled(False)
        self.wg_util.tab_asset.setEnabled(True)
        self.wg_util.tab_layer.setEnabled(True)
        self.wg_util.tab_camera.setEnabled(True)
        self.wg_util.tab_render.setEnabled(True)
        self.wg_util.gBox_asset.setEnabled(True)
        self.wg_util.gBox_newLayer.setEnabled(True)
        self.wg_util.btn_render_settings.setEnabled(True)

# ASSET TAB --------------------------------------------------------------------------------------------------------------------------------------------------------

    def set_asset_path(self):
        object_path = QFileDialog.getOpenFileName(None, 'Import Object', 'C:\\', 
                      'All Formats (*.obj *.fbx *.abc *.max *mdl)')
        self.wg_util.line_asset.setText(object_path[0])

    def enable_add_asset(self):
        if self.wg_util.line_asset.displayText():
            self.wg_util.btn_asset_import.setEnabled(True)
        else:
            self.wg_util.btn_asset_import.setEnabled(False)

    def check_duplicate_asset(self, file_name):
        asset_ui = ca.AssetUI(parent=self)
        i = 1
        for asset in asset_ui.get_asset_list():
            asset_name = asset.name.replace('_ctrl', '')
            if '_copy_' in file_name:
                copy = '_copy_' + str(i-1)
                file_name = file_name.replace(copy, '_copy_' + str(i))
                i = i + 1

            elif file_name == asset_name and '_copy_' not in file_name:
                file_name = file_name + '_copy_' + str(i)
                i = i + 1

        return file_name

    def import_asset(self, object_path):
        file_formats = ['.obj', '.fbx', '.abc', '.max', '.mdl']
        file_name = object_path.split('/')[-1:]
        file_name = ''.join(file_name)
        for file_format in file_formats:
            if file_format in file_name:
                file_name = file_name.replace(file_format, '')

        file_name = self.check_duplicate_asset(file_name)
        ttSetup = ct.TT_Setup()
        import_object = ttSetup.import_object(object_path, file_name)
        for asset in import_object.Children:
            rs.Render_Settings().include_asset_to_wireframe(asset)

        asset_ui = ca.AssetUI(parent=self)
        asset_ui.create_asset(file_name, len(asset_ui.get_asset_list()))
        asset_ui.enable_asset(file_name)
        self.wg_util.line_asset.clear()

# HDRIS TAB --------------------------------------------------------------------------------------------------------------------------------------------------------

    def enable_add_layer(self):
        if self.wg_util.new_name_layer.displayText():
            self.wg_util.btn_addLyr.setEnabled(True)
        else:
            self.wg_util.btn_addLyr.setEnabled(False)

    def add_layer(self):
        lyr_name = self.wg_util.new_name_layer.displayText()
        lyr_ui = cl.LayerUI(parent=self)
        if lyr_ui.check_lyr_name(lyr_name) != False:
            lyr_ui.create_layer(lyr_name, len(lyr_ui.get_lyr_list()) + 1)
            ct.TT_Setup().add_domeLight(lyr_name)
            lyr_ui.isolate_layer(lyr_name)

# CAMERA TAB --------------------------------------------------------------------------------------------------------------------------------------------------------

    def enable_add_camera(self):
        if self.wg_util.line_camera.displayText():
            self.wg_util.pBtn_createCamera.setEnabled(True)
        else:
            self.wg_util.pBtn_createCamera.setEnabled(False)

    def add_camera(self):
        cam_name = self.wg_util.line_camera.displayText()
        cam_ui = cc.CameraUI(parent=self)

        if cam_ui.check_cam_name(cam_name) != False:
            cam_ui.create_camera(cam_name, len(cam_ui.get_cam_list()) + 1)
            ct.TT_Setup().create_camera(cam_name)
            cam_ui.isolate_camera(cam_name)

# RENDER TAB --------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_output_path(self):
        vr = rs.Render_Settings().get_vray()
        output_path = str(vr.output_rawFileName)
        if output_path == 'None':
            self.wg_util.btn_renderout.setEnabled(False)
            return ''
        else:
            return output_path

    def set_render_path(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.AnyFile)
        render_path = dialog.getSaveFileName(None, 'Import Object', 'C:\\', 
                      'EXR File (*.exr)')

        self.wg_util.lEdit_render.setText(render_path[0])
        dmf.set_vray_render_output(render_path[0])

    def enable_render(self):
        if self.wg_util.lEdit_render.displayText():
            self.wg_util.btn_renderout.setEnabled(True)
        else:
            self.wg_util.btn_renderout.setEnabled(False)

    def toggle_render_settings(self):
        if self.wg_util.btn_render_settings.isChecked():
            self.wg_util.btn_render_settings.setText('▾  Render Settings')
            rs.Render_Settings().show_render_settings(self)
        else:
            self.wg_util.btn_render_settings.setText('▸  Render Settings')
            rs.Render_Settings().hide_render_settings(self)

    def toggle_aovs(self):
        if self.wg_util.btn_aovs.isChecked():
            self.wg_util.btn_aovs.setText('▾  AOVs')
            rs.Render_Settings().show_aovs(self)
        else:
            self.wg_util.btn_aovs.setText('▸  AOVs')
            rs.Render_Settings().hide_aovs(self)

# CHECK SCENE --------------------------------------------------------------------------------------------------------------------------------------------------------

    def check_scene(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') != None:
            self.domeLights = ct.TT_Setup().get_domeLights()
            self.cameras = ct.TT_Setup().get_cameras()
            self.assets = ct.TT_Setup().get_assets()

            self.wg_util.tab_asset.setEnabled(True)
            self.wg_util.tab_layer.setEnabled(True)
            self.wg_util.tab_camera.setEnabled(True)
            self.wg_util.tab_render.setEnabled(True)
            self.wg_util.gBox_newLayer.setEnabled(True)
            self.wg_util.gBox_asset.setEnabled(True)
            self.wg_util.btn_render_settings.setEnabled(True)

            self.check_assets()
            self.check_hdris()
            self.check_cameras()

    def check_assets(self):
        if self.assets:
            asset_ui = ca.AssetUI(parent=self)
            index = 1
            for asset in self.assets:
                asset_name = asset.name.replace('_ctrl', '')
                asset_ui.create_asset(asset_name, index)
                asset_ui.get_asset_subdivision(asset_name)
                if asset.isHidden == False:
                   asset_ui.enable_asset(asset_name)
                if str(rt.getTransformLockFlags(asset)) != r'#{}':
                    asset_ui.lock_asset(asset)
                index = index + 1

    def check_hdris(self):
        if self.domeLights:
            lyr_ui = cl.LayerUI(parent=self)
            index = 1
            for domeLight in self.domeLights:
                lyr_ui.create_layer(domeLight.name, index)
                lyr_ui.getHDRI(domeLight)
                lyr_ui.enable_options(domeLight.name)
                index = index + 1
                if domeLight.on:
                    lyr_ui.toggle_layer(domeLight.name)

    def check_cameras(self):
        if self.cameras:
            cam_ui = cc.CameraUI(parent=self)
            index = 1
            for camera in self.cameras:
                cam_ui.create_camera(camera.name, index)
                index = index + 1
                if camera.isHidden == False:
                    cam_ui.toggle_camera(camera.name)
                if dmf.get_camera_transform_flags(camera) != r'#{}':
                    cam_ui.lock_camera(camera)
                cam_ui.get_cam_focal_length(camera)

def main():
    main_window = qtmax.GetQMaxMainWindow()
    main_widget = main_window.findChild(QtWidgets.QDockWidget, 'YFX_LDEV_UI')
    if main_widget:
        main_widget.close()

    main_window = qtmax.GetQMaxMainWindow()
    main_widget = YFX_LDEV_UI(parent=main_window)
    main_widget.setObjectName('YFX_LDEV_UI')
    main_widget.check_scene()
    main_widget.setFloating(True)
    main_widget.show()

if __name__ == '__main__':
    main()