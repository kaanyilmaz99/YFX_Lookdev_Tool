# The actual module which creates the turntable
import json
import os
import pymxs
from pymxs import attime
from pymxs import runtime as rt


DIR_PATH = os.path.dirname(__file__)
json_path = DIR_PATH + r'\turntable_settings.json'

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
        else:
            self.domeLights = list(rt.getNodeByName('TT_HDRIs_ctrl').children)
        self.get_domeLights()
        self.hdris = []

        self.create_controls()
        self.create_ttCamera()
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
        mesh_ctrl.parent = rt.getNodeByName('TT_Assets_grp')

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
        self.dome_rotation(self.domeLights[-1])

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
            ctrl_ttAssets = rt.dummy(name='TT_Assets_grp')
            ctrl_ttAssets.parent = ctrl_ttMaster
            ctrl_ttAssets.isHidden = True
            ctrl_ttRotation = rt.dummy(name='TT_Rotation_ctrl')
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
            self.camera_rotation(ctrl_ttRotation)
        else:
            ctrl_ttMaster = rt.getNodeByName('TT_Master_ctrl')
            ctrl_ttRotation = rt.getNodeByName('TT_Rotation_ctrl')
            ctrl_ttHdris = rt.getNodeByName('TT_HDRIs_ctrl')
            ctrl_ttAssets = rt.getNodeByName('TT_Assets_grp')
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

    def create_ttCamera(self):
        if rt.getNodeByName('TT_Camera') == None:
            tt_camera = rt.vrayPhysicalCamera()
            tt_camera.name = 'TT_Camera'
            tt_camera.targeted = True
            tt_camera.type = 1
            tt_camera.exposure = 0
            tt_camera.focal_length = 40
            tt_camera.film_width = 55
            tt_camera.parent = self.create_controls()[1]
            tt_camera.setmxsprop('pos.y', -100)
            tt_camera.setmxsprop('pos.z', 50)
            #Get Camera Target
            tt_camera_target = rt.getNodeByName('TT_Camera.Target')
            tt_camera_target.setmxsprop('pos.z', 50)
            tt_camera_target.parent = self.create_controls()[1]
            #Create and move into Layer
            camera_layer = rt.LayerManager.newLayerFromName('0_Camera')
            camera_layer.addNode(tt_camera)
            camera_layer.addNode(tt_camera_target)

    def camera_rotation(self, node):
        rt.select(node)

        with pymxs.animate(True):
            with attime(1):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
            with attime(101):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")

    def dome_rotation(self, node):
        rt.select(node)

        with pymxs.animate(True):
            with attime(start_frame + 100):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 0)")
            with attime(end_frame):
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("in coordsys parent rotate $ (EulerAngles 0 0 180)")
                rt.execute("$.rotation.z_rotation.controller.keys.inTangentType = #linear")
                rt.execute("$.rotation.z_rotation.controller.keys.outTangentType = #linear")


