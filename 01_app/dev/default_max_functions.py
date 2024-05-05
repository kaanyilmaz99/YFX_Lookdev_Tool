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

from UI import icons
from UI import tt_icons
from UI import camera_icons

importlib.reload(cl)                                             # Can be deleted later
importlib.reload(ct)                                             # Can be deleted later
importlib.reload(cc)                                             # Can be deleted later
importlib.reload(ca)                                             # Can be deleted later
importlib.reload(rs)                                             # Can be deleted later

DIR_PATH = os.path.dirname(__file__)
MAIN_UI_PATH = DIR_PATH + r'\UI\turntable_UI.ui'

def open_max_file(file_path):
    rt.checkForSave()
    rt.loadMaxFile(file_path, allowPrompts = True)

def save_as(save_file_path):
    if '_' in save_file_path:
        save_file_path = save_file_path.split('_')[:-1]
        save_file_path = '_'.join(save_file_path) + '_v001.max'
    else:
        save_file_path = save_file_path + '_v001.max'
        rt.saveMaxFile(save_file_path)

def save_incremental():
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

def get_tt_setup():
    return rt.getNodeByName('TT_Master_ctrl')

def setup_initial_settings():
    vr = rs.Render_Settings().get_vray()
    vr.output_saveRawFile = True

    rs_high_path = DIR_PATH + r'\render_presets\RS_High.rps'
    rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 4, 32))

    rt.rendTimeType = 3
    rt.sliderTime = rt.rendStart

    re = rt.MaxOps.GetCurRenderElementMgr()
    re.AddRenderElement(rt.VRayExtraTex(elementname='Wireframe'))

def get_camera_transform_flags(camera):
    return str(rt.getTransformLockFlags(camera))

def set_vray_render_output(render_path):
    vr = rs.Render_Settings().get_vray()
    vr.output_rawFileName = render_path
    vr.output_force32bit_3dsmax_vfb = True

    rt.renderSceneDialog.update()

def start_render():
    rt.render(framerange=rt.Name('active'), vfb=False)