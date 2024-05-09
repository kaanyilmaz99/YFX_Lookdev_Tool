#******************************************************************************************************************
# content:        Creates the Turntable animations for domeLight and asset rotations

# dependencies:   3dsmax API

# how to:         After creating a turntable this module creates the necessary keyframes for the asset and light
#                 rotations. Also updates dynamically when changing the frame range.

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#******************************************************************************************************************

import pymxs
from pymxs import attime
from pymxs import runtime as rt

def asset_hrotation(node, v_rot=False):
    rt.select(node)
    cur_start_frame = rt.rendStart
    cur_end_frame = rt.rendEnd

    if v_rot:
        h_rot_end = ((cur_end_frame - cur_start_frame - 1)/4) + cur_start_frame
        v_rot_start = h_rot_end + 1
        v_rot_end = ((cur_end_frame - cur_start_frame - 1)/4) + v_rot_start
    else:
        animation_end = ((cur_end_frame - cur_start_frame - 1)/2) + cur_start_frame

    with pymxs.animate(False):
        with attime(cur_start_frame):
             node.setmxsprop('rotation', rt.EulerAngles(0, 0, 0))
             rt.execute("deletekeys $ #allkeys")
    if v_rot:
        with pymxs.animate(True):
            with attime(cur_start_frame):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
            with attime(h_rot_end):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")
            with attime(v_rot_start):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")
            with attime(v_rot_end):
                rt.execute("in coordsys parent rotate $ (EulerAngles 180 0 0)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 180 0 0)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")
    else:
        with pymxs.animate(True):
            with attime(cur_start_frame):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
            with attime(animation_end):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")
    rt.deselect(node)

def dome_rotation(domeLight, initial_rotation):
    rt.select(domeLight)

    cur_start_frame = rt.rendStart
    cur_end_frame = rt.rendEnd
    animation_start = cur_end_frame - ((cur_end_frame - cur_start_frame - 1)/2)

    with pymxs.animate(False):
        with attime(animation_start):
             rt.execute("deletekeys $.texmap #allkeys")
             domeLight.texmap.horizontalRotation = 0

    with pymxs.animate(True):
        with attime(0):
            domeLight.texmap.horizontalRotation = 0 + initial_rotation

        with attime(animation_start):
            domeLight.texmap.horizontalRotation = 0 + initial_rotation
            rt.execute("$.texmap.horizontalRotation.controller.keys.inTangentType = #linear")
            rt.execute("$.texmap.horizontalRotation.controller.keys.outTangentType = #linear")

        with attime(cur_end_frame):
            domeLight.texmap.horizontalRotation = 360 + initial_rotation
            rt.execute("$.texmap.horizontalRotation.controller.keys.inTangentType = #linear")
            rt.execute("$.texmap.horizontalRotation.controller.keys.outTangentType = #linear")

def get_dome_rotation(domeLight):
    cur_start_frame = rt.rendStart
    cur_end_frame = rt.rendEnd
    animation_start = cur_end_frame - ((cur_end_frame - cur_start_frame - 1)/2)

    with pymxs.animate(False):
        with attime(animation_start):
            initial_rotation = domeLight.texmap.horizontalRotation

    return initial_rotation