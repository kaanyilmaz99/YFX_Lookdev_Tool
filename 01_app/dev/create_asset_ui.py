#****************************************************************************************************
# content:        Creates the AssetUI after importing and will be appended to the main ui dynamically.
#                 Also connects all the necessary buttons to its functions.

# dependencies:   PySide2/PyQt, 3dsmax API, main window (qtmax) and maxscript

# how to:         After importing an asset from the MainUI this module will be executed.

# todos:          Add more custom settings in the options tab (e.g.: Displacement V-Rax modifier settings)

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

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
from UI import asset_icons
from UI import camera_icons

sys.path.append(os.path.dirname(__file__))
importlib.reload(main_ui)
importlib.reload(ct)

DIR_PATH = os.path.dirname(__file__)
ASSET_UI_PATH = DIR_PATH + r'\UI\asset_UI.ui'
ASSET_OPTIONS_UI_PATH = DIR_PATH + r'\UI\asset_options_UI.ui'

class AssetUI():
    def __init__(self, parent=None):
        self.wg_util = parent
        self.asset_number = str(len(self.get_asset_list()))

# ASSET UI ------------------------------------------------------------------------------------------------------------------------------------------------

    def enable_asset(self, asset_name):
        btn_asset = self.wg_util.findChild(QPushButton, 'btn_asset_' + asset_name)
        btn_asset.setChecked(True)

    def get_asset_list(self):
        assets = ct.TT_Setup().get_assets()
        return assets

    def check_asset_name(self, new_asset_name):
        new_asset_ctrl_name = new_asset_name + '_ctrl'
        for asset in self.get_asset_list():
            if asset.name == new_asset_ctrl_name:
                QMessageBox.warning(None, 'Warning', 'Asset name already exists!')
                return False

    def create_asset(self, asset_name, asset_number):
        layout_asset = self.wg_util.findChild(QVBoxLayout, 'layout_asset')

        self.wg_asset = QtUiTools.QUiLoader().load(ASSET_UI_PATH)
        self.wg_asset.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.wg_asset.setObjectName('wg_asset_' + asset_name)

        self.wg_asset.gBox_asset.setTitle(asset_name)
        self.wg_asset.gBox_asset.setObjectName('gBox_asset_' + asset_name)
        self.wg_asset.btn_asset.setObjectName('btn_asset_' + asset_name)
        self.wg_asset.btn_asset_lock.setObjectName('btn_asset_lock_' + asset_name)
        self.wg_asset.sBox_subdiv.setObjectName('sBox_subdiv_' + asset_name)
        self.wg_asset.btn_asset_options.setObjectName('btn_asset_options_' + asset_name)
        self.wg_asset.btn_asset_remove.setObjectName('btn_asset_remove_' + asset_name)
        layout_asset.insertWidget(asset_number, self.wg_asset)

        btn_asset_remove = self.wg_util.findChild(QPushButton, 'btn_asset_remove_' + asset_name)
        btn_asset_remove.clicked.connect(lambda: self.remove_asset(asset_name))
        btn_asset = self.wg_util.findChild(QPushButton, 'btn_asset_' + asset_name)
        btn_asset.clicked.connect(lambda: self.toggle_asset(asset_name))
        sBox_subdiv = self.wg_util.findChild(QSpinBox, 'sBox_subdiv_' + asset_name)
        sBox_subdiv.valueChanged.connect(lambda: self.sBox_subdiv_change(asset_name))
        btn_asset_options = self.wg_util.findChild(QPushButton, 'btn_asset_options_' + asset_name)
        btn_asset_options.clicked.connect(lambda: self.asset_options_ui(asset_name))
        btn_asset_lock = self.wg_util.findChild(QPushButton, 'btn_asset_lock_' + asset_name)
        btn_asset_lock.clicked.connect(lambda: self.toggle_asset_lock(asset_name))

    def get_asset_subdivision(self, asset_name):
        sBox_subdiv = self.wg_util.findChild(QSpinBox, 'sBox_subdiv_' + asset_name)
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        for asset in asset_ctrl.Children:
            value = asset.modifiers[0].iterations
            sBox_subdiv.setValue(value)
            return value

    def sBox_subdiv_change(self, asset_name):
        sBox_subdiv = self.wg_util.findChild(QSpinBox, 'sBox_subdiv_' + asset_name)
        value = sBox_subdiv.value()
        ct.TT_Setup().change_subdiv(asset_name, value)
        rt.redrawViews()

    def remove_asset(self, asset_name):
        ct.TT_Setup().delete_asset(asset_name)
        layout_asset = self.wg_util.findChild(QVBoxLayout, 'layout_asset')
        wg_asset = self.wg_util.findChild(QWidget, 'wg_asset_' + asset_name)
        wg_asset.deleteLater()

        index = 1
        for asset in self.get_asset_list():
            asset_name = asset.name.replace('_ctrl', '')
            wg_asset = self.wg_util.findChild(QWidget, 'wg_asset_' + asset_name)
            layout_asset.insertWidget(index, wg_asset)
            index = index + 1
            
        rt.redrawViews()

    def toggle_asset(self, asset_name):
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        rt.select(asset_ctrl)
        for asset in asset_ctrl.Children:
            if asset_ctrl.isHidden:
                asset.isHidden = False
                asset_ctrl.isHidden = False
                rt.execute("max move")
            else:
                asset.isHidden = True
                asset_ctrl.isHidden = True
                rt.deselect(asset_ctrl)

            rt.redrawViews()

    def lock_asset(self, asset):
        asset_name = asset.name.replace('_ctrl', '')
        btn_asset_lock = self.wg_util.findChild(QPushButton, 'btn_asset_lock_' + asset_name)
        btn_asset_lock.setChecked(True)

    def toggle_asset_lock(self, asset_name):
        btn_asset_lock = self.wg_util.findChild(QPushButton, 'btn_asset_lock_' + asset_name)
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        for asset in asset_ctrl.Children:
            if  btn_asset_lock.isChecked():
                rt.setTransformLockFlags(asset_ctrl, rt.name('all'))
                rt.setTransformLockFlags(asset, rt.name('all'))
            else:
                rt.setTransformLockFlags(asset_ctrl, rt.name('none'))
                rt.setTransformLockFlags(asset, rt.name('none'))

    def get_wg_asset_index(self, asset_name):
        asset_layer = self.wg_util.findChild(QVBoxLayout, 'layout_asset')
        for i in range(1, asset_layer.count()):
            asset_item = asset_layer.itemAt(i).widget()
            if asset_name in asset_item.objectName():
                return(i)

# ASSET OPTIONS UI ----------------------------------------------------------------------------------------------------------------------------------------

    def asset_options_ui(self, asset_name):
        self.wg_asset_options = QtUiTools.QUiLoader().load(ASSET_OPTIONS_UI_PATH)
        self.wg_asset_options.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        asset_index = self.get_wg_asset_index(asset_name)
        self.wg_asset_options.btn_asset_apply.clicked.connect(lambda: self.asset_options_ui_confirm(asset_name, asset_index))
        self.wg_asset_options.show()
        
        for asset in self.get_asset_list():
            asset_name_ctrl = asset.name.replace('_ctrl', '')
            if asset_name_ctrl == asset_name:
                total_polycount = str(self.get_asset_polycount(asset_name))
                self.wg_asset_options.setWindowTitle(asset_name + ' - Asset Options')
                self.wg_asset_options.line_asset_rename.setText(asset_name)
                self.wg_asset_options.label_polycount.setText(total_polycount)
                
    def get_asset_polycount(self, asset_name):
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        total_polycount = 0
        for asset in asset_ctrl.Children:
            asset_polycount = rt.getNumFaces(asset)
            total_polycount  = total_polycount + asset_polycount

        return total_polycount

    def asset_options_ui_confirm(self, asset_name, asset_index):
        new_asset_name = self.wg_asset_options.line_asset_rename.displayText()
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')

        for asset in self.get_asset_list():
            if asset.name == asset_ctrl.name:
                if asset_name != new_asset_name and self.check_asset_name(new_asset_name) != False:
                    for asset in asset_ctrl.Children:
                        asset.name = asset.name.replace(asset_name, new_asset_name)
                    asset_ctrl.name = new_asset_name + '_ctrl'
                    asset_layer = rt.LayerManager.getLayerFromName(asset_name + '_layer')
                    asset_layer.setName(new_asset_name + '_layer')
                    self.rename_confirm(asset_name, asset_index, new_asset_name)
                    self.wg_asset_options.close()

                elif asset_name == new_asset_name:
                    self.wg_asset_options.close()

                rt.redrawViews()

    def rename_confirm(self, asset_name, asset_index, new_asset_name):
        wg_asset = self.wg_util.findChild(QWidget, 'wg_asset_' + asset_name)
        btn_asset = self.wg_util.findChild(QPushButton, 'btn_asset_' + asset_name)
        isolate = btn_asset.isChecked()
        wg_asset.deleteLater()

        self.create_asset(new_asset_name, asset_index)
        new_btn_asset = self.wg_util.findChild(QPushButton, 'btn_asset_' + new_asset_name)
        new_btn_asset.setChecked(isolate)