# The actual module which creates the turntable
import json
import os
import pymxs
from pymxs import attime
from pymxs import runtime as rt


DIR_PATH = os.path.dirname(__file__)
RS_PATH = DIR_PATH + r'\render_presets/'
CFG_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', 'cfg'))
json_path = CFG_PATH + r'\turntable_settings.json'

'''
user_data = {
    "Start Frame" : 1001,
    "End Frame" : 1200
}

with open(json_path, 'w') as outfile:
    json.dump(user_data, outfile, indent=4)

---------------------------------------------

With this .json file you are able to use a easy readeable configuration to set up
some specific parameters for this script. Currently I am only using it to set the animation Range
of 3Dsmax and animate the domeLight once a layer is created. 

Later I will use this also for resolutions and specific render settings as well.

'''

with open(json_path) as json_file:
    data = json.load(json_file)

start_frame = data['Start Frame']
end_frame = data['End Frame']


class TT_Setup():

    def __init__(self):
        if rt.getNodeByName('TT_HDRIs_ctrl') == None:
            self.domeLights = []
            rt.animationRange = rt.interval(start_frame, end_frame)
            self.initial_frame_range(start_frame, end_frame)
        else:
            self.domeLights = list(rt.getNodeByName('TT_HDRIs_ctrl').children)
        self.get_domeLights()
        self.hdris = []

        self.create_controls()
        # self.create_ttCamera()
        self.create_groundPlane()

    def import_object(self, path):
        rt.importFile(path, rt.Name('noPrompt'))
        meshes = rt.selection

        file_formats = ['.obj', '.fbx', '.abc', '.max', '.mdl']
        file_name = path.split('/')[-1:]
        file_name = ''.join(file_name)
        for file_format in file_formats:
            if file_format in file_name:
                file_name = file_name.replace(file_format, '')

        mesh_ctrl = rt.dummy(name = file_name.capitalize() + '_ctrl')
        mesh_ctrl.parent = rt.getNodeByName('TT_Assets_ctrl')

        assets_layer = rt.LayerManager.getLayerFromName('0_Assets')
        mesh_layer = rt.LayerManager.newLayerFromName(file_name.capitalize())
        mesh_layer.setParent(assets_layer)
        mesh_layer.addNode(mesh_ctrl)
        for mesh in meshes:
            mesh.parent = mesh_ctrl
            mesh_layer.addNode(mesh)
      
        rt.clearSelection()
        return mesh_ctrl

    def get_domeLights(self):
        return self.domeLights

    def add_domeLight(self, name):
        self.domeLights.append(rt.vrayLight())
        self.domeLights[-1].type = 1
        self.domeLights[-1].dome_adaptive = False
        self.domeLights[-1].multiplier = 1
        # self.domeLights[-1].invisible = True
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

    def create_controls(self):
        if rt.getNodeByName('TT_Master_ctrl') == None:
            ctrl_ttMaster = rt.dummy(name='TT_Master_ctrl')
            ctrl_ttMaster.isHidden = True
            ctrl_ttAssets = rt.dummy(name='TT_Assets_ctrl')
            ctrl_ttAssets.parent = ctrl_ttMaster
            ctrl_ttAssets.isHidden = True
            ctrl_ttRotation = rt.dummy(name='TT_Cameras_ctrl')
            ctrl_ttRotation.isHidden = True
            ctrl_ttRotation.parent = ctrl_ttMaster
            ctrl_ttHdris = rt.dummy(name='TT_HDRIs_ctrl')
            ctrl_ttHdris.parent = ctrl_ttMaster
            ctrl_ttHdris.isHidden = True
            #Create Assets Layer
            assets_layer = rt.LayerManager.newLayerFromName('0_Assets')
            #Create Control Layer
            control_layer = rt.LayerManager.newLayerFromName('0_CTRLs')
            control_layer.addNode(ctrl_ttMaster)
            control_layer.addNode(ctrl_ttRotation)
            control_layer.addNode(ctrl_ttHdris)
            control_layer.addNode(ctrl_ttAssets)
            #Create Animations
            self.asset_hrotation(ctrl_ttAssets)
        else:
            ctrl_ttMaster = rt.getNodeByName('TT_Master_ctrl')
            ctrl_ttRotation = rt.getNodeByName('TT_Cameras_ctrl')
            ctrl_ttHdris = rt.getNodeByName('TT_HDRIs_ctrl')
            ctrl_ttAssets = rt.getNodeByName('TT_Assets_ctrl')
            #Return controls
            return [ctrl_ttMaster, ctrl_ttRotation, ctrl_ttHdris, ctrl_ttAssets]

    def create_groundPlane(self):
        if rt.getNodeByName('Ground_Plane') == None:
            ground_plane = rt.vrayPlane()
            ground_plane.name = 'Ground_Plane'
            ground_plane.parent = self.create_controls()[0]
            #Set ground plane properties
            rt.setUserProp(ground_plane, 'VRay_Matte_Alpha', -1.0)
            rt.setUserProp(ground_plane, 'VRay_Matte_Enable', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_Shadows', True)
            rt.setUserProp(ground_plane, 'VRay_Matte_ShadowAlpha', True)
            rt.setUserProp(ground_plane, 'VRay_Secondary_Matte_Enable', True)
            #Create Layer for ground Plane
            ground_layer = rt.LayerManager.newLayerFromName('0_Ground')
            ground_layer.addNode(ground_plane)

    def create_camera(self, cam_name):
        # if 'persp' in str(rt.viewport.getType()):
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

        #Get Camera Target
        # tt_camera_target = rt.getNodeByName(cam_name + '.Target')
        # tt_camera_target.setmxsprop('pos.z', 50)
        # tt_camera_target.parent = self.create_controls()[1]

        # Create and move into Layer
        if rt.LayerManager.getLayerFromName('0_Cameras'):
            camera_layer = rt.LayerManager.getLayerFromName('0_Cameras')
        else:
            camera_layer = rt.LayerManager.newLayerFromName('0_Cameras')
        camera_layer.addNode(tt_camera)
        # camera_layer.addNode(tt_camera_target)


# RENDER SETTINGS ---------------------------------------------------------------------------------------------------------

    def inital_render_settings(self, rs_preset):
        #Set VRay as current render
        vr = self.get_vray()
        rt.rendTimeType = 3

        if rs_preset == 'High':
            rs_high_path = RS_PATH + "RS_High.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 3, 4, 32))

        elif rs_preset == 'Medium':
            rs_high_path = RS_PATH + "RS_Medium.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 3, 4, 32))

        elif rs_preset == 'Low':
            rs_high_path = RS_PATH + "RS_Low.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 3, 4, 32))

    def get_vray(self):
        for renderer in rt.rendererClass.classes:
            if "V_Ray" in str(renderer) and not "GPU" in str(renderer):
                rt.renderers.current = renderer
                vr = rt.renderers.current
        return vr

    def initial_frame_range(self, start, end):
        rt.rendStart = start
        rt.endStart = end

    def change_resolution_width(self, width):
        rt.renderWidth = width
        rt.renderSceneDialog.update()

    def change_resolution_height(self, height):
        rt.renderHeight = height
        rt.renderSceneDialog.update()

    def change_startFrame(self, frame):
        rt.rendStart = frame
        rt.renderSceneDialog.update()

    def change_endFrame(self, frame):
        rt.rendEnd = frame
        rt.renderSceneDialog.update()

    def change_nthFrame(self, value):
        rt.rendNThFrame = value
        rt.renderSceneDialog.update()

    def change_minSubdiv(self, value):
        vr = self.get_vray()
        vr.twoLevel_baseSubdivs = value

    def change_maxSubdiv(self, value):
        vr = self.get_vray()
        vr.twoLevel_fineSubdivs = value

    def change_noiseThreshold(self, value):
        vr = self.get_vray()
        vr.twoLevel_threshold = value

    def change_shadingRate(self, value):
        vr = self.get_vray()
        vr.imageSampler_shadingRate = value

    def change_bucketSize(self, value):
        vr = self.get_vray()
        vr.twoLevel_bucket_width = value

    def toggle_lights(self, value):
        vr = self.get_vray()
        vr.options_lights = value

    def toggle_gi(self, value):
        vr = self.get_vray()
        vr.gi_on = value

    def toggle_shadows(self, value):
        vr = self.get_vray()
        vr.options_shadows = value

    def toggle_displacement(self, value):
        vr = self.get_vray()
        vr.options_displacement = value

    def change_colorspace(self, colorspace):
        vr = self.get_vray()
        if 'sRGB' in colorspace:
            vr.options_rgbColorSpace = 1 

        elif 'ACES' in colorspace:
            vr.options_rgbColorSpace = 2

# ANIMATION ---------------------------------------------------------------------------------------------------------

    def asset_hrotation(self, node):
        rt.select(node)

        with pymxs.animate(True):
            with attime(start_frame):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
            with attime(end_frame - 100):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")

    def dome_rotation(self, domeLight, initial_rotation):
        rt.select(domeLight)

        with pymxs.animate(True):
            with attime(0):
                domeLight.texmap.horizontalRotation = 0 + initial_rotation

            with attime(start_frame + 100):
                domeLight.texmap.horizontalRotation = 0 + initial_rotation
                rt.execute("$.texmap.horizontalRotation.controller.keys.inTangentType = #linear")
                rt.execute("$.texmap.horizontalRotation.controller.keys.outTangentType = #linear")

            with attime(end_frame):
                domeLight.texmap.horizontalRotation = 360 + initial_rotation
                rt.execute("$.texmap.horizontalRotation.controller.keys.inTangentType = #linear")
                rt.execute("$.texmap.horizontalRotation.controller.keys.outTangentType = #linear")

    def get_dome_rotation(self, domeLight):
        with pymxs.animate(False):
            with attime(start_frame + 100):
                initial_rotation = domeLight.texmap.horizontalRotation

        return initial_rotation



