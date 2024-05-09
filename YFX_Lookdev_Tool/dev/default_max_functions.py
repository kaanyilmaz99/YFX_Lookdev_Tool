#****************************************************************************************************
# content:        A collection of usefull functions, where the 3dsmax API is needed

# dependencies:   3dsMax and maxscript

# how to:         These functions will be executed from the other modules if needed

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#****************************************************************************************************

import os
import sys
sys.path.append(os.path.dirname(__file__))                       # Can be deleted later
import importlib

from pymxs import runtime as rt

import create_animations as anim
import create_turntable as ct
import render_setup as rs

importlib.reload(anim)
importlib.reload(rs)
importlib.reload(ct)                                                # Can be deleted later

DIR_PATH = os.path.dirname(__file__)

def get_tt_setup():
    return rt.getNodeByName('TT_Master_ctrl')

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

def get_all_children_of_node(parent, node_type=None):
    def list_children(node):
        children = []
        for child in node.Children:
            children.append(child)
            children = children + list_children(child)
        return children
    child_list = list_children(parent)

    return ([x for x in child_list if rt.superClassOf(x) == node_type]
            if node_type else child_list)

def get_camera_transform_flags(node):
    return str(rt.getTransformLockFlags(node))

def get_inital_domeLight_rotation():
    initial_rotation = 0
    for domeLight in ct.TT_Setup().get_domeLights():
        if domeLight.texmap != None:
            initial_rotation = anim.get_dome_rotation(domeLight)
    return initial_rotation

def update_framerange(initial_rotation, v_rot):
    asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
    anim.asset_hrotation(asset_ctrl, v_rot)
    for domeLight in ct.TT_Setup().get_domeLights():
        if domeLight.texmap:
            anim.dome_rotation(domeLight, initial_rotation)

    rt.animationRange = rt.interval(rt.rendStart, rt.rendEnd)
    rt.renderSceneDialog.update()

def include_asset_to_wireframe(asset):
    re = rt.MaxOps.GetCurRenderElementMgr()
    re_amount = re.NumRenderElements()
    asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')

    for re_index in range(0, re_amount):
        aov = re.GetRenderElement(re_index)
        if aov.elementname == 'Wireframe':
            if aov.includeList == None:
                aov.includeList = rt.array(asset)
                aov.texture = create_vray_edges()
                aov.elementname = 'Wireframe'
            else:
                new_array = rt.array()
                for mesh in list(aov.includeList):
                    rt.append(new_array, mesh)
                rt.append(new_array, asset)
                aov.includeList = new_array

def create_bitmap_texture(path):
    bitmap = rt.VrayBitmap()
    name = path.split('/')[-1]
    bitmap.name = name.split('.')[0]
    bitmap.HDRIMapName = path
    bitmap.coords.blur = 0.01
    return bitmap

def create_vray_material():
    material = rt.VrayMtl()
    material.reflection = rt.color(255, 255, 255)
    material.refraction_ior = 1.53
    material.brdf_useRoughness = True
    material.texmap_bump_multiplier = 100
    material.texmap_coat_bump_multiplier = 100
    return material

def create_vray_edges():
    wireframe = rt.VRayEdgesTex()
    wireframe.PixelWidth = 0.5
    return wireframe

def get_vray():
    for renderer in rt.rendererClass.classes:
        if "V_Ray" in str(renderer) and not "GPU" in str(renderer):
            rt.renderers.current = renderer
            vr = rt.renderers.current
    return vr

def set_vray_render_output(render_path):
    vr = get_vray()
    vr.output_rawFileName = render_path
    vr.output_force32bit_3dsmax_vfb = True

    rt.renderSceneDialog.update()

def start_render():
    rt.render(framerange=rt.Name('active'), vfb=False)
