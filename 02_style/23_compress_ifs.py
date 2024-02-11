# STYLE ***************************************************************************
# content = assignment (Python Advanced)
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#**********************************************************************************


# COMMENT --------------------------------------------------
# Not optimal
def set_color(ctrl_List=None, color=None):

    for ctrl_name in ctrlList:
        try:
            mc.setAttr(ctrl_name + 'Shape.overrideEnabled', 1)
        except:
            pass

        try:
            color_codes = [4, 13, 25, 17, 17, 15, 6, 16]
            mc.setAttr(ctrl_name + 'Shape.overrideColor', color_codes[color - 1])
        except:
            pass


# EXAMPLE
# set_color(['circle','circle1'], 8)
