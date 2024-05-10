#******************************************************************************************************************
# content:        Creates the actual Turntable in Max. Also contains all the functions and information to 
#                 interacting with all the Turntable assets, hdris, cameras and other nodes.

# dependencies:   3dsmax API

# how to:         After pressing the Create Turntable button the setup is built in Max. Changing values/settings
#                 inside the YFX Tool will interact with the Turntable.

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#******************************************************************************************************************

import os
import math

import render_setup as rs
import create_animations as anim
import default_max_functions as dmf
import create_lookdev_charts as clc

from pymxs import runtime as rt

DIR_PATH = os.path.dirname(__file__)
RS_PATH = DIR_PATH + r'\render_presets/'
ASSET_PATH = DIR_PATH + r'\assets/'
CFG_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', 'cfg'))

class TT_Setup():
    def __init__(self):
        self.get_domeLights()
        self.create_controls()
        self.create_groundPlane()

# ASSET INTERACTIONS  ------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_assets(self):
        asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
        assets = []
        for asset in list(asset_ctrl.Children):
            assets.append(asset)
        return assets

    def get_asset_center(self):
        asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
        master_ctrl = rt.getNodeByName('TT_Master_ctrl')
        z_heights = []
        children = []
        for child in list(asset_ctrl.Children):
            z_height = child.getmxsprop('pos.z')
            z_heights.append(z_height)
            children.append(child)
            child.parent = None

        asset_ctrl_height = sum(z_heights)/len(z_heights)
        asset_ctrl.setmxsprop('pos.z', asset_ctrl_height)
        for child in children:
            child.parent = asset_ctrl

    def import_object(self, path, file_name):
        rt.sliderTime = rt.rendStart
        rt.importFile(path, rt.Name('noPrompt'))
        meshes = rt.selection
        z_height = rt.execute("($.max - $.min).z")
        mesh_ctrl = rt.point(name = file_name + '_ctrl', size=0)
        mesh_ctrl.setmxsprop('pos.z', z_height/2)
        mesh_ctrl.parent = rt.getNodeByName('TT_Assets_ctrl')

        self.get_asset_center()

        assets_layer = rt.LayerManager.getLayerFromName('0_Assets')
        mesh_layer = rt.LayerManager.newLayerFromName(file_name + '_layer')
        mesh_layer.setParent(assets_layer)
        mesh_layer.addNode(mesh_ctrl)
        for mesh in meshes:
            mesh.name = file_name + '_' + mesh.name
            mesh.parent = mesh_ctrl
            mesh_layer.addNode(mesh)
            rt.addModifier(mesh, rt.TurboSmooth(iterations=0))

        rt.clearSelection()
        return mesh_ctrl

    def update_asset_ctrl(self):
        tt_master_ctrl = rt.getNodeByName('TT_Master_ctrl')
        tt_asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')

        rt.select(dmf.get_all_children_of_node(tt_asset_ctrl))
        z_height = rt.execute("($.max - $.min).z")
        assets = []
        for asset in tt_asset_ctrl.Children:
            assets.append(asset)
            asset.parent = None

        tt_asset_ctrl.parent = None
        tt_asset_ctrl.setmxsprop('pos.z', z_height/2)
        tt_asset_ctrl.parent = tt_master_ctrl
        for asset in assets:
            asset.parent = tt_asset_ctrl

    def change_subdiv(self, asset_name, value):
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        for asset in asset_ctrl.Children:
            asset.modifiers[0].iterations = value

    def delete_asset(self, asset_name):
        asset_ctrl = rt.getNodeByName(asset_name + '_ctrl')
        for asset in asset_ctrl.Children:
            rt.delete(asset)
            
        rt.delete(asset_ctrl)
        rt.LayerManager.deleteLayerByName(asset_name + '_layer')

# DOMELIGHT INTERACTIONS  ------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_domeLights(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') == None:
            self.domeLights = []
        else:
            self.domeLights = list(rt.getNodeByName('TT_HDRIs_ctrl').children)
        return self.domeLights

    def add_domeLight(self, name):
        self.domeLights.append(rt.vrayLight())
        self.domeLights[-1].type = 1
        self.domeLights[-1].dome_adaptive = False
        self.domeLights[-1].multiplier = 1
        self.domeLights[-1].texmap_resolution = 2048
        self.domeLights[-1].name = name
        self.domeLights[-1].parent = self.create_controls()[2]
        self.domeLights[-1].texmap = rt.vrayBitmap()
        bitmap = self.domeLights[-1].texmap
        bitmap.mapType = 2

        if rt.LayerManager.getLayerFromName('0_HDRIs'):
            hdriLayer = rt.LayerManager.getLayerFromName('0_HDRIs')
        else:
            hdriLayer = rt.LayerManager.newLayerFromName('0_HDRIs')

        hdriLayer.addNode(self.domeLights[-1])
        anim.dome_rotation(self.domeLights[-1], 0)

    def enable_domeLight(self, name):
        for domeLight in self.domeLights:
            if domeLight.name == name:
                domeLight.on = True
                domeLight.isHidden = False

    def disable_domeLight(self, name):
        for domeLight in self.domeLights:
            if domeLight.name == name:
                domeLight.on = False
                domeLight.isHidden = True

    def rename_domeLights(self, lyr_name, new_name):
        for domeLight in self.domeLights:
            if domeLight.name == lyr_name:
                domeLight.name = new_name

    def remove_domeLight(self, name):
        for domeLight in self.domeLights:
            if domeLight.name == name:
                rt.delete(domeLight)
                self.domeLights.remove(domeLight)

    def create_hdri_bitmap(self, name, path):
        for domeLight in self.domeLights:
            if domeLight.name == name:
                vrayBitmap = domeLight.texmap
                vrayBitmap.HDRIMapName = path
                vrayBitmap.name = name
                vrayBitmap.mapType = 2

    def set_default_background(self, domeLight):
        domeLight.invisible = False
        bitmap = domeLight.texmap
        bitmap.name = domeLight.name
        bitmap.ground_on = False
        rt.setUseEnvironmentMap = False

    def set_screen_background(self, domeLight):
        domeLight.invisible = True
        bitmap = domeLight.texmap
        bitmap.name = domeLight.name
        bitmap.ground_on = False

        screen_map = rt.VrayBitmap()
        screen_map.HDRIMapName = bitmap.HDRIMapName
        screen_map.name = bitmap.name + '_ScreenMap'
        screen_map.coords.mappingType = 1
        screen_map.coords.mapping = 3
        bitmap.name = bitmap.name + '_S'

        rt.setUseEnvironmentMap = True
        rt.environmentMap = screen_map
        rt.viewport.DispBkgImage = False
        rt.redrawViews()

    def set_grey_background(self, domeLight):
        domeLight.invisible = True
        bitmap = domeLight.texmap
        bitmap.name = domeLight.name
        bitmap.ground_on = False

        noise = rt.Noise()
        noise.color1 = rt.color(40, 40, 40)
        noise.color2 = rt.color(52, 52, 52)
        noise.type = 1
        noise.size = 14
        noise.levels = 10
        noise.thresholdLow = 0.1
        noise.thresholdHigh = 0.9
        noise.coords.blur = 0.01
        noise.name = bitmap.name + '_GreyBG'
        bitmap.name = bitmap.name + '_N'

        rt.setUseEnvironmentMap = True
        rt.environmentMap = noise
        rt.viewport.DispBkgImage = False
        rt.redrawViews()

    def set_ground_projection(self, domeLight, pos_x, pos_y, pos_z, radius):
        domeLight.invisible = False
        bitmap = domeLight.texmap
        bitmap.name = domeLight.name
        bitmap.ground_on = True
        bitmap.ground_position = rt.Point3(pos_x, pos_y, pos_z)
        bitmap.ground_radius = radius

# CAMERA INTERACTIONS  ------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_cameras(self):
        cameras = rt.getNodeByName('TT_Cameras_ctrl').children
        cameras = list(cameras)
        new_cameras = []
        for camera in cameras:
            if '.Target' not in camera.name:
                new_cameras.append(camera)

        return new_cameras

    def create_camera(self, cam_name):
        transform_matrix = rt.viewport.getTM()
        inverted_matrix = rt.inverse(transform_matrix)

        tt_camera = rt.vrayPhysicalCamera()
        tt_camera.name = cam_name
        tt_camera.targeted = False
        tt_camera.type = 1
        tt_camera.exposure = 0
        tt_camera.focal_length = 40
        tt_camera.film_width = 55
        tt_camera.parent = self.create_controls()[1]
        tt_camera.transform = inverted_matrix
        clc.create_lookdev_info(tt_camera)
        self.view_camera(tt_camera)

        if rt.LayerManager.getLayerFromName('0_Cameras'):
            camera_layer = rt.LayerManager.getLayerFromName('0_Cameras')
        else:
            camera_layer = rt.LayerManager.newLayerFromName('0_Cameras')
        camera_layer.addNode(tt_camera)

    def view_camera(self, cam):
        rt.viewport.setCamera(cam)
        rt.redrawViews()

    def change_cam_focal_length(self, cam_name, value):
        cam = rt.getNodeByName(cam_name)
        cam.focal_length = value
        lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')
        h_width = 2*math.tan(math.radians(cam.fov/2))*(-80)
        scale_value = ((h_width*(-9.27))/10)/100
        lookdev_info_ctrl.setmxsprop('scale', rt.Point3(scale_value, scale_value, scale_value))

    def remove_camera(self, cam_name):
        # FIX THIS
        camera = rt.getNodeByName(cam_name)
        lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')
        lookdev_info_scale_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_scale_ctrl')

        for child in list(lookdev_info_ctrl.children):
            rt.delete(child)

        rt.delete(camera)
        rt.delete(lookdev_info_ctrl)
        rt.delete(lookdev_info_scale_ctrl)
        rt.LayerManager.deleteLayerByName('0_LookdevInfo_' + cam_name)
        rt.redrawViews()

# TT CONTROLLERS ------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_controls(self):
        if rt.getNodeByName('TT_Master_ctrl') == None:
            ctrl_ttMaster = rt.dummy(name='TT_Master_ctrl')
            ctrl_ttMaster.isHidden = True
            ctrl_ttAssets = rt.dummy(name='TT_Assets_ctrl')
            ctrl_ttAssets.parent = ctrl_ttMaster
            ctrl_ttAssets.isHidden = True
            ctrl_ttCameras = rt.dummy(name='TT_Cameras_ctrl')
            ctrl_ttCameras.isHidden = True
            ctrl_ttCameras.parent = ctrl_ttMaster
            ctrl_ttHdris = rt.dummy(name='TT_HDRIs_ctrl')
            ctrl_ttHdris.parent = ctrl_ttMaster
            ctrl_ttHdris.isHidden = True

            assets_layer = rt.LayerManager.newLayerFromName('0_Assets')
            control_layer = rt.LayerManager.newLayerFromName('0_CTRLs')
            control_layer.addNode(ctrl_ttMaster)
            control_layer.addNode(ctrl_ttCameras)
            control_layer.addNode
            control_layer.addNode(ctrl_ttAssets)
            anim.asset_hrotation(ctrl_ttAssets)
        else:
            ctrl_ttMaster = rt.getNodeByName('TT_Master_ctrl')
            ctrl_ttCameras = rt.getNodeByName('TT_Cameras_ctrl')
            ctrl_ttHdris = rt.getNodeByName('TT_HDRIs_ctrl')
            ctrl_ttAssets = rt.getNodeByName('TT_Assets_ctrl')

            return [ctrl_ttMaster, ctrl_ttCameras, ctrl_ttHdris, ctrl_ttAssets]

# GROUND PLANE ------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_groundPlane(self):
        if rt.getNodeByName('Ground_Plane') == None:
            ground_plane = rt.vrayPlane()
            ground_plane.name = 'Ground_Plane'
            ground_plane.parent = self.create_controls()[0]
            ground_plane.IconText_on = False
            ground_plane.IconSize = 0

            rt.setUserProp(ground_plane, 'VRay_Matte_Alpha', -1.0)
            rt.setUserProp(ground_plane, 'VRay_Matte_Enable', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_Shadows', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_ShadowAlpha', True)
            rt.setUserProp(ground_plane, 'VRay_Secondary_Matte_Enable', True)

            ground_layer = rt.LayerManager.newLayerFromName('0_Ground')
            ground_layer.addNode(ground_plane)