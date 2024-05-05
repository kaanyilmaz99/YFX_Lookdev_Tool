# The actual module which creates the turntable
import json
import math
import os

import render_setup as rs

import pymxs
from pymxs import attime
from pymxs import runtime as rt


DIR_PATH = os.path.dirname(__file__)
RS_PATH = DIR_PATH + r'\render_presets/'
ASSET_PATH = DIR_PATH + r'\assets/'
CFG_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', 'cfg'))
json_path = CFG_PATH + r'\turntable_settings.json'

with open(json_path) as json_file:
    data = json.load(json_file)

start_frame = data['Start Frame']
end_frame = data['End Frame']

# user_data = {
#     "Start Frame" : 1001,
#     "End Frame" : 1200
# }

# with open(json_path, 'w') as outfile:
#     json.dump(user_data, outfile, indent=4)

class TT_Setup():

    def __init__(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') == None:
            self.domeLights = []
            rt.animationRange = rt.interval(start_frame, end_frame)
            rs.Render_Settings().initial_frame_range(start_frame, end_frame)
        else:
            self.domeLights = list(rt.getNodeByName('TT_HDRIs_ctrl').children)
        self.get_domeLights()
        self.hdris = []

        self.create_controls()
        self.create_groundPlane()

    def get_assets(self):
        asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
        assets = []
        for asset in list(asset_ctrl.Children):
            assets.append(asset)
        return assets

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

        # self.update_asset_ctrl() FIX THIS
        rt.clearSelection()

        return mesh_ctrl

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

    def update_asset_ctrl(self):
        tt_master_ctrl = rt.getNodeByName('TT_Master_ctrl')
        tt_asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
        rt.select(get_all_children_of_node(tt_asset_ctrl))
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

    def get_domeLights(self):
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

        #Create HDRI Layers
        if rt.LayerManager.getLayerFromName('0_HDRIs'):
            hdriLayer = rt.LayerManager.getLayerFromName('0_HDRIs')
        else:
            hdriLayer = rt.LayerManager.newLayerFromName('0_HDRIs')
        #Add domeLight to layer
        hdriLayer.addNode(self.domeLights[-1])
        #Animate domeLight
        self.dome_rotation(self.domeLights[-1], 0)

    def remove_domeLight(self, name):
        for domeLight in self.domeLights:
            if domeLight.name == name:
                rt.delete(domeLight)
                self.domeLights.remove(domeLight)

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
            #Create Assets Layer
            assets_layer = rt.LayerManager.newLayerFromName('0_Assets')
            #Create Control Layer
            control_layer = rt.LayerManager.newLayerFromName('0_CTRLs')
            control_layer.addNode(ctrl_ttMaster)
            control_layer.addNode(ctrl_ttCameras)
            control_layer.addNode(ctrl_ttHdris)
            control_layer.addNode(ctrl_ttAssets)
            #Create Animations
            self.asset_hrotation(ctrl_ttAssets)
        else:
            ctrl_ttMaster = rt.getNodeByName('TT_Master_ctrl')
            ctrl_ttCameras = rt.getNodeByName('TT_Cameras_ctrl')
            ctrl_ttHdris = rt.getNodeByName('TT_HDRIs_ctrl')
            ctrl_ttAssets = rt.getNodeByName('TT_Assets_ctrl')
            #Return controls
            return [ctrl_ttMaster, ctrl_ttCameras, ctrl_ttHdris, ctrl_ttAssets]

    def create_groundPlane(self):
        if rt.getNodeByName('Ground_Plane') == None:
            ground_plane = rt.vrayPlane()
            ground_plane.name = 'Ground_Plane'
            ground_plane.parent = self.create_controls()[0]
            ground_plane.IconText_on = False
            ground_plane.IconSize = 0
            #Set ground plane properties
            rt.setUserProp(ground_plane, 'VRay_Matte_Alpha', -1.0)
            rt.setUserProp(ground_plane, 'VRay_Matte_Enable', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_Shadows', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_ShadowAlpha', True)
            rt.setUserProp(ground_plane, 'VRay_Secondary_Matte_Enable', True)
            #Create Layer for ground Plane
            ground_layer = rt.LayerManager.newLayerFromName('0_Ground')
            ground_layer.addNode(ground_plane)

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
        self.create_lookdev_info(tt_camera)
        self.view_camera(tt_camera)

        # Create and move into Layer
        if rt.LayerManager.getLayerFromName('0_Cameras'):
            camera_layer = rt.LayerManager.getLayerFromName('0_Cameras')
        else:
            camera_layer = rt.LayerManager.newLayerFromName('0_Cameras')
        camera_layer.addNode(tt_camera)

    def get_cameras(self):
        cameras = rt.getNodeByName('TT_Cameras_ctrl').children
        cameras = list(cameras)

        new_cameras = []
        for camera in cameras:
            if '.Target' not in camera.name:
                new_cameras.append(camera)

        return new_cameras

    def remove_camera(self, cam_name):
        # FIX THIS
        camera = rt.getNodeByName(cam_name)
        lookdev_info_ctrl = rt.getNodeByName('LookdevInfo_' + cam_name + '_ctrl')

        for child in list(lookdev_info_ctrl.children):
            rt.delete(child)

        rt.delete(lookdev_info_ctrl)
        rt.delete(camera)
        rt.LayerManager.deleteLayerByName('0_LookdevInfo_' + cam_name)
        rt.redrawViews()

    def create_lookdev_info(self, cam):
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
        lookdev_info_ctrl.parent = cam
        lookdev_info_ctrl.isHidden = True

        chrome_ball.parent = lookdev_info_ctrl
        grey_ball.parent = lookdev_info_ctrl
        macbeth_chart.parent = lookdev_info_ctrl
        macbeth_diffuse_chart.parent = lookdev_info_ctrl

        lookdev_info_ctrl.setmxsprop('position', (cam.getmxsprop('position')))
        lookdev_info_ctrl.setmxsprop('rotation.x_rotation',(cam.getmxsprop('rotation.x_rotation') - 90))
        lookdev_info_ctrl.setmxsprop('rotation.y_rotation',(cam.getmxsprop('rotation.y_rotation')))
        lookdev_info_ctrl.setmxsprop('rotation.z_rotation',(cam.getmxsprop('rotation.z_rotation')))

        rt.select(lookdev_info_ctrl)
        rt.execute('in coordsys #parent $.pos.z = -80')
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
            self.assign_lookdev_info_materials(cam)
        else:
            self.create_lookdev_info_materials()
            self.assign_lookdev_info_materials(cam)

    def assign_lookdev_info_materials(self, cam):
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

    def create_lookdev_info_materials(self):
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

# ANIMATION ---------------------------------------------------------------------------------------------------------

    def asset_hrotation(self, node, v_rot=False):
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

    def dome_rotation(self, domeLight, initial_rotation):
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

    def get_dome_rotation(self, domeLight):
        cur_start_frame = rt.rendStart
        cur_end_frame = rt.rendEnd
        animation_start = cur_end_frame - ((cur_end_frame - cur_start_frame - 1)/2)

        with pymxs.animate(False):
            with attime(animation_start):
                initial_rotation = domeLight.texmap.horizontalRotation

        return initial_rotation