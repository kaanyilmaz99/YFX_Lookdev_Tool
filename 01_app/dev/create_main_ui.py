#*********************************************************************
# content   = creates the main working ui
#             executes other scripts which build the turntables
# todos     = wip turntable creation, more rendersettings implementation

# version   = 0.1
# date      = 2024-11-02
#
# author    = Kaan Yilmaz
#*********************************************************************

import os
import sys
sys.path.append(os.path.dirname(__file__))
import importlib

import qtmax
from pymxs import runtime as rt

from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject
from PySide2.QtGui import *


# import create_layer_ui
import create_turntable as ct

from UI import icons
from UI import tt_icons

importlib.reload(ct)
# importlib.reload(create_layer_ui)


DIR_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = DIR_PATH + r'\UI\turntable_UI.ui'
LAYER_UI_PATH = DIR_PATH + r'\UI\layer_UI.ui'
LAYER_OPTIONS_UI_PATH = DIR_PATH + r'\UI\layer_options_UI.ui'


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
        self.resize(393, 405)

        # Home Tab
        if rt.getNodeByName('TT_Master_ctrl'):
            self.wg_util.gBox_import.setEnabled(False)

        self.wg_util.btn_import.clicked.connect(self.import_object)
        self.wg_util.btn_create_tt.clicked.connect(self.setup_tt)
        self.wg_util.line_import.textChanged.connect(self.enable_create_tt)
        self.wg_util.btn_save_as.clicked.connect(self.save_as)
        self.wg_util.btn_save_incr.clicked.connect(self.save_incremental)
        self.wg_util.btn_openFile.clicked.connect(self.open_file)

        # Layers Tab
        self.wg_util.new_name_layer.textEdited.connect(self.enable_add_layer)
        self.wg_util.btn_addLyr.clicked.connect(self.add_layer)

        #Cameras Tab
        self.wg_util.line_camera.textEdited.connect(self.enable_create_camera)
        self.wg_util.pBtn_createCamera.clicked.connect(self.create_camera)

        #Render Tab
        self.wg_util.cBox_renderSettings.currentTextChanged.connect(self.render_setting_preset)

        self.wg_util.pBtn_720.clicked.connect(self.clicked_resolution_720)
        self.wg_util.pBtn_1080.clicked.connect(self.clicked_resolution_1080)
        self.wg_util.pBtn_1440.clicked.connect(self.clicked_resolution_1440)
        self.wg_util.pBtn_2160.clicked.connect(self.clicked_resolution_2160)
        self.wg_util.sBox_width.valueChanged.connect(lambda: ct.TT_Setup().change_resolution_width(self.wg_util.sBox_width.value()))
        self.wg_util.sBox_height.valueChanged.connect(lambda: ct.TT_Setup().change_resolution_height(self.wg_util.sBox_height.value()))
        self.wg_util.sBox_startFrame.valueChanged.connect(lambda:ct.TT_Setup().change_startFrame(self.wg_util.sBox_startFrame.value()))
        self.wg_util.sBox_endFrame.valueChanged.connect(lambda:ct.TT_Setup().change_endFrame(self.wg_util.sBox_endFrame.value()))
        self.wg_util.sBox_nth.valueChanged.connect(lambda: ct.TT_Setup().change_nthFrame(self.wg_util.sBox_nth.value()))

        self.wg_util.sBox_minSubdiv.valueChanged.connect(lambda: ct.TT_Setup().change_minSubdiv(self.wg_util.sBox_minSubdiv.value()))
        self.wg_util.sBox_maxSubdiv.valueChanged.connect(lambda: ct.TT_Setup().change_maxSubdiv(self.wg_util.sBox_maxSubdiv.value()))
        self.wg_util.dsBox_noise.valueChanged.connect(lambda: ct.TT_Setup().change_noiseThreshold(self.wg_util.dsBox_noise.value()))
        self.wg_util.sBox_shading.valueChanged.connect(lambda: ct.TT_Setup().change_shadingRate(self.wg_util.sBox_shading.value()))
        self.wg_util.sBox_bucket.valueChanged.connect(lambda: ct.TT_Setup().change_bucketSize(self.wg_util.sBox_bucket.value()))

        self.wg_util.cBox_lights.stateChanged.connect(lambda: ct.TT_Setup().toggle_lights(self.wg_util.cBox_lights.isChecked()))
        self.wg_util.cBox_gi.stateChanged.connect(lambda: ct.TT_Setup().toggle_gi(self.wg_util.cBox_gi.isChecked()))
        self.wg_util.cBox_shadows.stateChanged.connect(lambda: ct.TT_Setup().toggle_shadows(self.wg_util.cBox_shadows.isChecked()))
        self.wg_util.cBox_displacement.stateChanged.connect(lambda: ct.TT_Setup().toggle_displacement(self.wg_util.cBox_displacement.isChecked()))
        self.wg_util.cBox_colorspace.currentTextChanged.connect(lambda: ct.TT_Setup().change_colorspace(self.wg_util.cBox_colorspace.currentText()))

    def import_object(self):
        object_path = QFileDialog.getOpenFileName(None, 'Import Object', 'C:\\', 
                      'All Formats (*.obj *.fbx *.abc *.max *mdl)')
        self.wg_util.line_import.setText(object_path[0])

    def enable_create_tt(self):
        if self.wg_util.line_import.displayText():
            self.wg_util.btn_create_tt.setEnabled(True)
        else:
            self.wg_util.btn_create_tt.setEnabled(False)

    def enable_create_camera(self):
        if self.wg_util.line_camera.displayText():
            self.wg_util.pBtn_createCamera.setEnabled(True)
        else:
            self.wg_util.pBtn_createCamera.setEnabled(False)

    def create_camera(self):
        cam_name = self.wg_util.line_camera.displayText()
        ct.TT_Setup().create_camera(cam_name)

    def open_file(self):
        open_file = QFileDialog.getOpenFileName(None, 'Open Scene', 'C:\\', '3ds Max (*.max)')
        if open_file[0] != '':
            rt.checkForSave()
            rt.loadMaxFile(open_file[0], allowPrompts = True)

    def save_as(self):
        save_file = QFileDialog.getSaveFileName(None, 'Save As', 'C:\\', '3ds Max (*.max)')
        if save_file[0] != '':
            save_file = save_file[0].replace('.max', '')
            save_tags = ['v1', 'v01', 'v001', 'v0001']
            for save_tag in save_tags:
                if save_tag in save_file.split('_')[-1]:
                    save_file = save_file.split('_')[:-1]
                    save_file = '_'.join(save_file)

            save_file = save_file + '_v001'
            rt.saveMaxFile(save_file)

    def save_incremental(self):
        if rt.maxFileName != '':
            file_path = rt.maxFilePath
            file_name = rt.maxFileName
            file_name = file_name.replace('.max', '')
            file_split = file_name.split('_')
            for part in file_split:
                if part.startswith('v') and part[1:4].isdigit():
                    old_version = part[1:]
                    break
            new_version = int(old_version) + 1
            new_version = 'v{:03}'.format(new_version)
            new_file_name = file_name.replace('v' + old_version, new_version)
            rt.saveMaxFile(file_path + new_file_name)
        else:
            QMessageBox.warning(None, 'Warning', 'Save/Open a scene first!')
            return None

    def setup_tt(self):
        object_path = self.wg_util.line_import.displayText()

        ttSetup = ct.TT_Setup()
        import_object = ttSetup.import_object(object_path)

        self.wg_util.line_import.clear()
        self.wg_util.gBox_import.setEnabled(False)
        self.wg_util.tab_layer.setEnabled(True)
        self.wg_util.gBox_newLayer.setEnabled(True)
        
        self.refresh_render_settings()
        return ttSetup

    def enable_add_layer(self):
        if self.wg_util.new_name_layer.displayText():
            self.wg_util.btn_addLyr.setEnabled(True)
        else:
            self.wg_util.btn_addLyr.setEnabled(False)

    def add_layer(self):
        lyr_name = self.wg_util.new_name_layer.displayText()
        lyr_ui = LayerUI(parent=self)
        if lyr_ui.check_lyr_name(lyr_name) != False:
            lyr_ui.create_layer(lyr_name, len(lyr_ui.get_lyr_list()) + 1)
            ct.TT_Setup().add_domeLight(lyr_name)
            lyr_ui.isolateLayer(lyr_name)

    def check_scene(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') != None:
            self.refresh_render_settings()
            self.domeLights = ct.TT_Setup().get_domeLights()
            self.wg_util.tab_layer.setEnabled(True)
            self.wg_util.gBox_newLayer.setEnabled(True)
            if self.domeLights:
                lyr_ui = LayerUI(parent=self)
                index = 1
                for domeLight in self.domeLights:
                    lyr_ui.create_layer(domeLight.name, index)
                    lyr_ui.getHDRI(domeLight)
                    index = index + 1
                    if domeLight.on:
                        lyr_ui.toggleLayer(domeLight.name)

    def render_setting_preset(self):
        rs_preset = str(self.wg_util.cBox_renderSettings.currentText())
        ct.TT_Setup().inital_render_settings(rs_preset)
        self.refresh_render_settings()

    def refresh_render_settings(self):
        vr = ct.TT_Setup().get_vray()
        rt.rendTimeType = 3

        self.wg_util.sBox_width.setValue(rt.renderWidth)
        self.wg_util.sBox_height.setValue(rt.renderHeight)

        self.wg_util.sBox_startFrame.setValue(rt.rendStart)
        self.wg_util.sBox_endFrame.setValue(rt.rendEnd)
        self.wg_util.sBox_nth.setValue(rt.rendNThFrame)

        self.wg_util.sBox_minSubdiv.setValue(vr.twoLevel_baseSubdivs)
        self.wg_util.sBox_maxSubdiv.setValue(vr.twoLevel_fineSubdivs)
        self.wg_util.dsBox_noise.setValue(vr.twoLevel_threshold)
        self.wg_util.sBox_shading.setValue(vr.imageSampler_shadingRate)
        self.wg_util.sBox_bucket.setValue(vr.twoLevel_bucket_width)
        self.wg_util.cBox_lights.setChecked(vr.options_lights)
        self.wg_util.cBox_gi.setChecked(vr.gi_on)
        self.wg_util.cBox_shadows.setChecked(vr.options_shadows)
        self.wg_util.cBox_displacement.setChecked(vr.options_displacement)
        self.wg_util.cBox_colorspace.setCurrentIndex(self.set_colorspace())

    def clicked_resolution_720(self):
        self.wg_util.sBox_width.setValue(1280)
        self.wg_util.sBox_height.setValue(720)

    def clicked_resolution_1080(self):
        self.wg_util.sBox_width.setValue(1920)
        self.wg_util.sBox_height.setValue(1080)

    def clicked_resolution_1440(self):
        self.wg_util.sBox_width.setValue(2560)
        self.wg_util.sBox_height.setValue(1440)

    def clicked_resolution_2160(self):
        self.wg_util.sBox_width.setValue(3840)
        self.wg_util.sBox_height.setValue(2160)

    def set_colorspace(self):
        vr = ct.TT_Setup().get_vray()
        index = vr.options_rgbColorSpace - 1
        return index

class LayerUI(YFX_LDEV_UI):
    def __init__(self, parent):
        super(LayerUI, self).__init__()
        self.parent = parent
        self.lyr_number = str(len(self.get_lyr_list()))

    def get_lyr_list(self):
        lyr_list = ct.TT_Setup().get_domeLights()

    def check_lyr_name(self, new_lyr_name):
        # Check if LayerName already exists
        for lyr in self.get_lyr_list():
            if lyr.name == new_lyr_name:
                QMessageBox.warning(None, 'Warning', 'Name already exists!')
                return False

    def create_layer(self, lyr_name, lyr_number):
        layout_layer = self.parent.findChild(QVBoxLayout, 'layout_layer')

        self.wg_layer = QtUiTools.QUiLoader().load(LAYER_UI_PATH)
        self.wg_layer.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wg_layer.lyr_gBox.setTitle(lyr_name)
        self.wg_layer.lyr_gBox.setObjectName('lyr_gBox_' + lyr_name)
        self.wg_layer.btn_path.setObjectName('btn_path_' + lyr_name)
        self.wg_layer.line_hdri.setObjectName('line_hdri_' + lyr_name)
        self.wg_layer.btn_remove.setObjectName('btn_remove_' + lyr_name)
        self.wg_layer.btn_enable.setObjectName('btn_enable_' + lyr_name)
        self.wg_layer.btn_options.setObjectName('btn_options_' + lyr_name)

        layout_layer.insertWidget(lyr_number, self.wg_layer)

        btn_remove = self.parent.findChild(QPushButton, 'btn_remove_' + lyr_name)
        btn_remove.clicked.connect(lambda: self.remove_layer(lyr_name))
        btn_enable = self.parent.findChild(QPushButton, 'btn_enable_' + lyr_name)
        btn_enable.clicked.connect(lambda: self.isolateLayer(lyr_name))
        btn_path = self.parent.findChild(QPushButton, 'btn_path_' + lyr_name)
        btn_path.clicked.connect(lambda: self.browseHDRI(lyr_name))
        btn_options = self.parent.findChild(QPushButton, 'btn_options_' + lyr_name)
        btn_options.clicked.connect(lambda: self.layer_options_ui(lyr_name))

    def remove_layer(self, lyr_name):
        # Remove HDRI
        ct.TT_Setup().remove_domeLight(lyr_name)

        # Remove Layer UI
        lyr_gBox = self.parent.findChild(QGroupBox, 'lyr_gBox_' + lyr_name)
        lyr_gBox.deleteLater()
        btn_remove = self.parent.findChild(QPushButton, 'btn_remove_' + lyr_name)
        btn_remove.clicked.disconnect()

        # Reposition Groupboxes
        layout_layer = self.parent.findChild(QVBoxLayout, 'layout_layer')
        index = 1
        for lyr in self.get_lyr_list():
            lyr_gBox = self.parent.findChild(QGroupBox, 'lyr_gBox_' + lyr.name)
            layout_layer.insertWidget(index, lyr_gBox)
            index = index + 1

    def toggleLayer(self, lyr):    
        # Specially for the case when checking the scene
        btn_enable = self.parent.findChild(QPushButton, 'btn_enable_' + lyr)
        btn_enable.setChecked(True)

    def isolateLayer(self, lyr_current):
        for lyr in self.get_lyr_list():
            btn_enable = self.parent.findChild(QPushButton, 'btn_enable_' + lyr.name)
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
        line_hdri = self.parent.findChild(QLineEdit, 'line_hdri_' + lyr_name)
        line_hdri.setText(hdri_path)

    def browseHDRI(self, lyr_name):
        hdri_path = QFileDialog.getOpenFileName(None, 'Choose HDRI', 'C:\\', 'HDRI File (*.exr *.hdr *.jpg *.png *.tif *.tiff)')
        if hdri_path[0] != '':
            line_hdri = self.parent.findChild(QLineEdit, 'line_hdri_' + lyr_name)
            line_hdri.setText(hdri_path[0])

        # Change HDRI
        ct.TT_Setup().create_hdri_bitmap(lyr_name, hdri_path[0])

    def layer_options_ui(self, lyr_name):
        self.wg_options = QtUiTools.QUiLoader().load(LAYER_OPTIONS_UI_PATH)
        self.wg_options.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.wg_options.btn_apply.clicked.connect(lambda: self.layer_options_ui_confirm(lyr_name))

        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                self.wg_options.setWindowTitle(lyr_name + ' - HDRI Options')
                self.wg_options.line_rename.setText(lyr_name)
                self.wg_options.cBox_invisible.setChecked(domeLight.invisible)
                self.wg_options.sBox_multiplier.setValue(domeLight.multiplier)
                self.wg_options.sBox_rotation.setValue(ct.TT_Setup().get_dome_rotation(domeLight))

        self.wg_options.show()

    def layer_options_ui_confirm(self, lyr_name):
        for domeLight in self.get_lyr_list():
            if domeLight.name == lyr_name:
                domeLight.invisible = self.wg_options.cBox_invisible.isChecked()
                domeLight.multiplier = self.wg_options.sBox_multiplier.value()
                ct.TT_Setup().dome_rotation(domeLight, self.wg_options.sBox_rotation.value())
                # domeLight.name = self.wg_options.line_rename.text()
                # lyr_gBox = self.wg_util.findChild(QGroupBox, 'lyr_gBox_' + lyr_name)
                # lyr_gBox.setTitle(self.wg_options.line_rename.text())
                
                self.wg_options.close()


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