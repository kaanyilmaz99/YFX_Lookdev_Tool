#******************************************************************************************************************
# content:        Creates the Lookdev Charts and Spheres for the newly created camera.

# dependencies:   3dsmax API

# how to:         After creating a new Camera in the MainUI, this module will create and assign the lookdev charts
#				  and spheres to it. Also creates its materials.

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#*******************************************************************************************************************

import os
from pymxs import runtime as rt

DIR_PATH = os.path.dirname(__file__)
ASSET_PATH = DIR_PATH + r'\assets/'

def create_lookdev_info(cam):
    chrome_ball = rt.sphere(name='Chrome_Ball_' + cam.name, radius=2.5, segments=48, position=rt.Point3(-3, 0, 0))
    grey_ball = rt.sphere(name='Grey_Ball_' + cam.name, radius=2.5, segments=48, position=rt.Point3(3, 0, 0))

    rt.importFile(ASSET_PATH + 'prpMacbethChart.fbx', rt.Name('noPrompt'))
    macbeth_chart = rt.getNodeByName('OUT_prpMacbethChart')
    macbeth_chart.name = 'Macbeth_Chart_' + cam.name
    macbeth_chart.setmxsprop('pos.z', -53)
    macbeth_chart.setmxsprop('scale', rt.Point3(0.35, 0.35, 0.35))

    rt.importFile(ASSET_PATH + 'prpMacbethChart.fbx', rt.Name('noPrompt'))
    macbeth_diffuse_chart = rt.getNodeByName('OUT_prpMacbethChart')
    macbeth_diffuse_chart.name = 'Macbeth_Diffuse_Chart_' + cam.name
    macbeth_diffuse_chart.setmxsprop('pos.z', -44.5)
    macbeth_diffuse_chart.setmxsprop('scale', rt.Point3(0.35, 0.35, 0.35))

    lookdev_info_ctrl = rt.dummy(name = 'LookdevInfo_' + cam.name + '_ctrl')
    lookdev_info_scale_ctrl = rt.dummy(name = 'LookdevInfo_' + cam.name + '_scale_ctrl')
    lookdev_info_ctrl.parent = lookdev_info_scale_ctrl
    lookdev_info_scale_ctrl.parent = cam
    lookdev_info_scale_ctrl.isHidden = True
    lookdev_info_ctrl.isHidden = True

    chrome_ball.parent = lookdev_info_ctrl
    grey_ball.parent = lookdev_info_ctrl
    macbeth_chart.parent = lookdev_info_ctrl
    macbeth_diffuse_chart.parent = lookdev_info_ctrl

    lookdev_info_scale_ctrl.setmxsprop('position', (cam.getmxsprop('position')))
    lookdev_info_scale_ctrl.setmxsprop('rotation.x_rotation',(cam.getmxsprop('rotation.x_rotation') - 90))
    lookdev_info_scale_ctrl.setmxsprop('rotation.y_rotation',(cam.getmxsprop('rotation.y_rotation')))
    lookdev_info_scale_ctrl.setmxsprop('rotation.z_rotation',(cam.getmxsprop('rotation.z_rotation')))

    rt.select(lookdev_info_ctrl)
    rt.execute('in coordsys #parent $.pos.y = 80')
    rt.deselect(lookdev_info_ctrl)

    rt.select(chrome_ball)
    rt.execute('in coordsys #parent $.pos.x = -48')
    rt.execute('in coordsys #parent $.pos.z = 25')
    rt.deselect(chrome_ball)

    rt.select(grey_ball)
    rt.execute('in coordsys #parent $.pos.x = -42')
    rt.execute('in coordsys #parent $.pos.z = 25')
    rt.deselect(grey_ball)

    rt.select(macbeth_chart)
    rt.execute('in coordsys #parent $.pos.x = -45')
    rt.execute('in coordsys #parent $.pos.z = -25')
    rt.deselect(macbeth_chart)

    rt.select(macbeth_diffuse_chart)
    rt.execute('in coordsys #parent $.pos.x = -45')
    rt.execute('in coordsys #parent $.pos.z = -17')
    rt.deselect(macbeth_diffuse_chart)

    if rt.LayerManager.getLayerFromName('0_LookdevInfo'):
        general_lookdev_info_layer = rt.LayerManager.getLayerFromName('0_LookdevInfo')

    else:
        general_lookdev_info_layer = rt.LayerManager.newLayerFromName('0_LookdevInfo')

    camera_lookdev_info_layer = rt.LayerManager.newLayerFromName('0_LookdevInfo_' + cam.name)
    camera_lookdev_info_layer.setParent(general_lookdev_info_layer)

    camera_lookdev_info_layer.addNode(chrome_ball)
    camera_lookdev_info_layer.addNode(grey_ball)
    camera_lookdev_info_layer.addNode(macbeth_chart)
    camera_lookdev_info_layer.addNode(macbeth_diffuse_chart)
    camera_lookdev_info_layer.addNode(lookdev_info_ctrl)

    if rt.sme.GetViewByName('TT_Setup_Materials'):
        assign_lookdev_info_materials(cam)
    else:
        create_lookdev_info_materials()
        assign_lookdev_info_materials(cam)

def assign_lookdev_info_materials(cam):
    rt.MatEditor.mode = rt.name('advanced')
    nodeView = rt.sme.GetViewByName('TT_Setup_Materials')

    grey_ball_material = rt.getMeditMaterial(21)
    chrome_ball_material = rt.getMeditMaterial(22)
    macbeth_material = rt.getMeditMaterial(23)
    macbeth_selfIllumMaterial = rt.getMeditMaterial(24)

    grey_ball = rt.getNodeByName('Grey_Ball_' + cam.name)
    chrome_ball = rt.getNodeByName('Chrome_Ball_' + cam.name)
    macbeth_chart = rt.getNodeByName('Macbeth_Chart_' + cam.name)
    macbeth_diffuse_chart = rt.getNodeByName('Macbeth_Diffuse_Chart_' + cam.name)

    grey_ball.material = grey_ball_material
    chrome_ball.material = chrome_ball_material
    macbeth_chart.material = macbeth_material
    macbeth_diffuse_chart.material = macbeth_selfIllumMaterial

def create_lookdev_info_materials():
    rt.MatEditor.mode = rt.name('advanced')
    rt.sme.Open()

    if rt.sme.GetView(rt.sme.activeView) != None:
        nodeView = rt.sme.GetView(rt.sme.activeView)
        nodeView.name = 'TT_Setup_Materials'
    else:
        rt.sme.CreateView('TT_Setup_Materials')
        nodeView = rt.sme.GetView(rt.sme.activeView)

    # Grey Ball Material
    grey_ball_material = rt.VrayMtl()
    grey_ball_material.name = 'grey_ball_VrayMtl'
    grey_ball_material.diffuse = rt.color(76, 76, 76)
    grey_ball_material.reflection = rt.color(255, 255, 255)
    grey_ball_material.reflection_glossiness = 0.68
    grey_ball_material.brdf_useRoughness = True
    grey_ball_material.refraction_ior = 1.5
    grey_ball_material.texmap_bump_multiplier = 100
    grey_ball_material.texmap_coat_bump_multiplier = 100

    # Chrome Ball Material
    chrome_ball_material = rt.VrayMtl()
    chrome_ball_material.name = 'chrome_ball_VrayMtl'
    chrome_ball_material.diffuse = rt.color(204, 204, 204)
    chrome_ball_material.reflection = rt.color(255, 255, 255)
    chrome_ball_material.reflection_glossiness = 0.05
    chrome_ball_material.reflection_metalness = 1
    chrome_ball_material.brdf_useRoughness = True
    chrome_ball_material.refraction_ior = 1.5
    chrome_ball_material.texmap_bump_multiplier = 100
    chrome_ball_material.texmap_coat_bump_multiplier = 100

    # Macbeth Chart Material
    # Aces Texture
    macbeth_texture = rt.vrayBitmap()
    macbeth_texture.HDRIMapName = ASSET_PATH + 'prpMacbethChart_AcesCG_baseColor_col.<UDIM>.exr'
    macbeth_texture.name = 'macbeth_chart_aces_texture'

    # Diffuse Chart
    macbeth_material = rt.VrayMtl()
    macbeth_material.name = 'macbeth_chart_VrayMtl'
    macbeth_material.texmap_diffuse = macbeth_texture
    macbeth_material.reflection = rt.color(255, 255, 255)
    macbeth_material.reflection_glossiness = 0.98
    macbeth_material.brdf_useRoughness = True
    macbeth_material.refraction_ior = 1.5
    macbeth_material.texmap_bump_multiplier = 100
    macbeth_material.texmap_coat_bump_multiplier = 100

    # SelfIllum Chart
    macbeth_selfIllumMaterial = rt.VrayMtl()
    macbeth_selfIllumMaterial.name = 'macbeth_chart_VrayMtl'
    macbeth_selfIllumMaterial.diffuse = rt.color(0, 0, 0)
    macbeth_selfIllumMaterial.texmap_self_illumination = macbeth_texture
    macbeth_selfIllumMaterial.reflection = rt.color(255, 255, 255)
    macbeth_selfIllumMaterial.reflection_glossiness = 0.98
    macbeth_selfIllumMaterial.brdf_useRoughness = True
    macbeth_selfIllumMaterial.refraction_ior = 1.5
    macbeth_selfIllumMaterial.texmap_bump_multiplier = 100
    macbeth_selfIllumMaterial.texmap_coat_bump_multiplier = 100

    #Create Nodes and MeditMaterials
    nodeView.createNode(grey_ball_material, rt.Point2(250, 0))
    nodeView.createNode(chrome_ball_material, rt.Point2(250, 650))
    nodeView.createNode(macbeth_material, rt.Point2(0, 0))
    nodeView.createNode(macbeth_selfIllumMaterial, rt.Point2(0, 650))
    rt.setMeditMaterial(21, grey_ball_material)
    rt.setMeditMaterial(22, chrome_ball_material)
    rt.setMeditMaterial(23, macbeth_material)
    rt.setMeditMaterial(24, macbeth_selfIllumMaterial)

    rt.sme.Close()
