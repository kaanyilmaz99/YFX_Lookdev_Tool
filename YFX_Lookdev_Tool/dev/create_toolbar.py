#****************************************************************************************************
# content:        Creates a Toolbar with the YFX Icon Button. When executing it opens up the
#                 MainUI for the YFX Lookdev Tool

# dependencies:   PySide2/PyQt, 3dsmax main window (qtmax)

# how to:         Click on the YFX Icon in the upper 3dsMax Toolbar

# version:        v 1.0.0
# date:           2024-11-03

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

import os
import sys
sys.path.append(os.path.dirname(__file__))

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2.QtWidgets import QMainWindow, QDockWidget, QToolButton, QToolBar, QAction
from PySide2.QtGui import QIcon

import create_main_ui as cm

from qtmax import GetQMaxMainWindow

MENU_NAME = 'YFX_Lookdev_Tool'
DIR_PATH = os.path.dirname(__file__)
YFX_UI = DIR_PATH + r''
YFX_ICON_PATH = DIR_PATH + r'\UI\icons\yfx_logo_white.png'

def create_toolbar():
    main_window = GetQMaxMainWindow()
    
    yfx_icon = QtGui.QIcon(YFX_ICON_PATH)

    button_yfx_tool = QAction('test', main_window)
    button_yfx_tool.setIcon(QIcon(YFX_ICON_PATH))
    button_yfx_tool.triggered.connect(action_pressed)

    toolbar_widget = QToolBar(main_window)
    toolbar_widget.setIconSize(QtCore.QSize(70, 36))
    toolbar_widget.setObjectName(MENU_NAME)
    toolbar_widget.setWindowTitle(MENU_NAME)
    toolbar_widget.setFloatable(True)
    toolbar_widget.addAction(button_yfx_tool)

    main_window.addToolBar(QtCore.Qt.TopToolBarArea, toolbar_widget)
    toolbar_widget.show()

def action_pressed():
    cm.main_widget()

if __name__ == '__main__':
    create_toolbar()
