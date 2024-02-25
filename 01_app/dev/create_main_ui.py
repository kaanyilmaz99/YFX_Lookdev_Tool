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


import create_layer_ui
import create_turntable as ct

from UI import icons
from UI import tt_icons

importlib.reload(ct)
importlib.reload(create_layer_ui)


DIR_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = DIR_PATH + r'\UI\turntable_UI.ui'
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

"""
To be able to dock your widget to the 3dsmax Main UI, you need to use class parenting.
1. You get the Max Main UI
2. Create your own Main Window Class
3. Parent your main window to the Max UI

"""


class KyScene(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(KyScene, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('KY-TurnTable-Tool')
        self.initUI()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def initUI(self):
        # Load MainUI

        main_layout = QtWidgets.QVBoxLayout()
        self.wg_util = QtUiTools.QUiLoader().load(MAIN_UI_PATH)
        self.wg_util.setLayout(main_layout)
        self.setWidget(self.wg_util)
        self.resize(500, 100)

        # Import Tab
        if rt.getNodeByName('TT_Master_ctrl'):
            self.wg_util.gBox_import.setEnabled(False)

        self.wg_util.btn_import.clicked.connect(self.import_object)
        self.wg_util.btn_create_tt.clicked.connect(self.setup_tt)
        self.wg_util.line_import.textChanged.connect(self.enable_create_tt)
        self.wg_util.btn_saveAs.clicked.connect(self.save_as)
        self.wg_util.btn_saveIncr.clicked.connect(self.save_incremental)
        self.wg_util.btn_openFile.clicked.connect(self.open_file)

        # Layers Tab
        self.wg_util.new_name_layer.textEdited.connect(self.enable_add_layer)
        self.wg_util.btn_addLyr.clicked.connect(self.add_layer)

    def import_object(self):
        object_path = QFileDialog.getOpenFileName(None, 'Import Object', 'C:\\', 
                      'All Formats (*.obj *.fbx *.abc *.max *mdl)')
        self.wg_util.line_import.setText(object_path[0])

    def enable_create_tt(self):
        if self.wg_util.line_import.displayText():
            self.wg_util.btn_create_tt.setEnabled(True)
        else:
            self.wg_util.btn_create_tt.setEnabled(False)

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

        # assetList = ca.AssetList()
        # assetList.add_asset(import_object)

        self.wg_util.line_import.clear()
        self.wg_util.gBox_import.setEnabled(False)
        self.wg_util.tab_layer.setEnabled(True)
        self.wg_util.gBox_newLayer.setEnabled(True)
        return ttSetup

    def enable_add_layer(self):
        if self.wg_util.new_name_layer.displayText():
            self.wg_util.btn_addLyr.setEnabled(True)
        else:
            self.wg_util.btn_addLyr.setEnabled(False)

    def add_layer(self):
        lyr_name = self.wg_util.new_name_layer.displayText()
        lyr_ui = create_layer_ui.LayerUI()
        if lyr_ui.check_lyr_name(lyr_name) != False:
            lyr_ui.create_layer(lyr_name, len(lyr_ui.get_lyr_list()) + 1)
            ct.TT_Setup().add_domeLight(lyr_name)
            lyr_ui.isolateLayer(lyr_name)

    def check_scene(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') != None:
            self.domeLights = ct.TT_Setup().get_domeLights()
            self.wg_util.tab_layer.setEnabled(True)
            self.wg_util.gBox_newLayer.setEnabled(True)
            if self.domeLights:
                lyr_ui = create_layer_ui.LayerUI()
                index = 1
                for domeLight in self.domeLights:
                    lyr_ui.create_layer(domeLight.name, index)
                    lyr_ui.getHDRI(domeLight)
                    index = index + 1
                    if domeLight.on:
                        lyr_ui.toggleLayer(domeLight.name)

def main():
    main_window = qtmax.GetQMaxMainWindow()
    main_widget = main_window.findChild(QtWidgets.QDockWidget, 'KY_TT')
    if main_widget:
        main_widget.close()

    main_window = qtmax.GetQMaxMainWindow()
    main_widget = KyScene(parent=main_window)
    main_widget.setObjectName('KY_TT')
    main_widget.check_scene()
    main_widget.setFloating(True)
    main_widget.show()

if __name__ == '__main__':
    main()