import sys
import os
sys.path.append(os.path.dirname(__file__))

import create_main_ui
from pymxs import runtime as rt

import importlib
importlib.reload(create_main_ui)

MENU_NAME = 'KY-TOOLS'


def create_menu():
    # DELETE previous menu
    delete_custom_menu(MENU_NAME)

    # CREATE menu item
    main_menu = rt.menuMan.getMainMenuBar()

    # FIND an existing menu item
    # menu = rt.menuMan.findMenu('&Help')

    # SUB menu
    menu = rt.menuMan.createMenu(MENU_NAME)
    menu_item = rt.menuMan.createSubMenuItem(MENU_NAME, menu)
    main_menu.addItem(menu_item, -1)



    #***************************************************************************
    # CREATE menu item 1
    def print_hello():
        create_main_ui.main()

    # Connect to a global in the runtime:
    rt.execute('global m1')
    rt.globalVars.set('m1', print_hello)
    macro_category = 'Category'
    macro_name = 'Name'

    macro_id = rt.macros.new(macro_category, macro_name, 'Tooltip', 'Turntable', 'm1()')

    menu_item = rt.menuMan.createActionItem(macro_name, macro_category)
    menu.addItem(menu_item, -1)


    # SEPARATOR
    sep = rt.menuMan.createSeparatorItem()
    menu.addItem(sep, -1)

def delete_custom_menu(menu_name):
    while rt.menuMan.findMenu(menu_name):
        rt.menuMan.unRegisterMenu(rt.menuMan.findMenu(menu_name))

create_menu()


# delete_custom_menu('KY-TOOLS')