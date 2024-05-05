import importlib
import json
import os

import qtmax
from pymxs import runtime as rt

import create_turntable as ct

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject

importlib.reload(ct)

DIR_PATH = os.path.dirname(__file__)
RS_PATH = DIR_PATH + r'\render_presets/'
RS_UI_PATH = DIR_PATH + r'\UI\renderSettings_UI.ui'
AOV_UI_PATH = DIR_PATH + r'\UI\aov_UI.ui'
CFG_PATH = os.path.abspath(os.path.join(DIR_PATH, '..', 'cfg'))
json_path = CFG_PATH + r'\turntable_settings.json'


class Render_Settings():

    def show_render_settings(self, parent):
        self.wg_util = parent
        layout_rs = self.wg_util.findChild(QVBoxLayout, 'layout_rs')

        self.wg_rs = QtUiTools.QUiLoader().load(RS_UI_PATH)
        self.wg_rs.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout_rs.insertWidget(1, self.wg_rs)
        self.refresh_render_settings()
        self.get_render_settings()

    def hide_render_settings(self, parent):
        self.wg_util = parent
        layout_rs = self.wg_util.findChild(QWidget, 'wg_rs')
        layout_rs.deleteLater()

    def show_aovs(self, parent):
        self.wg_util = parent
        layout_aov = self.wg_util.findChild(QVBoxLayout, 'layout_aov')

        self.wg_aov = QtUiTools.QUiLoader().load(AOV_UI_PATH)
        self.wg_aov.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout_aov.insertWidget(1, self.wg_aov)
        self.get_aovs()
        self.connect_aov_checkbox()

    def hide_aovs(self, parent):
        self.wg_util = parent
        layout_aov = self.wg_util.findChild(QWidget, 'wg_aov')
        layout_aov.deleteLater()

    def get_render_settings(self):
        self.wg_rs.pBtn_720.clicked.connect(self.clicked_resolution_720)
        self.wg_rs.pBtn_1080.clicked.connect(self.clicked_resolution_1080)
        self.wg_rs.pBtn_1440.clicked.connect(self.clicked_resolution_1440)
        self.wg_rs.pBtn_2160.clicked.connect(self.clicked_resolution_2160)
        self.wg_rs.sBox_width.valueChanged.connect(lambda: self.change_resolution_width(self.wg_rs.sBox_width.value()))
        self.wg_rs.sBox_height.valueChanged.connect(lambda:self.change_resolution_height(self.wg_rs.sBox_height.value()))
        self.wg_rs.sBox_startFrame.valueChanged.connect(lambda: self.change_startFrame(self.wg_rs.sBox_startFrame.value()))
        self.wg_rs.sBox_endFrame.valueChanged.connect(lambda: self.change_endFrame(self.wg_rs.sBox_endFrame.value()))
        self.wg_rs.sBox_nth.valueChanged.connect(lambda: self.change_nthFrame(self.wg_rs.sBox_nth.value()))
        
        self.wg_rs.cBox_renderSettings.currentTextChanged.connect(lambda: self.change_render_preset(self.wg_rs.cBox_renderSettings.currentText()))
        self.wg_rs.sBox_minSubdiv.valueChanged.connect(lambda: self.change_minSubdiv(self.wg_rs.sBox_minSubdiv.value()))
        self.wg_rs.sBox_maxSubdiv.valueChanged.connect(lambda: self.change_maxSubdiv(self.wg_rs.sBox_maxSubdiv.value()))
        self.wg_rs.dsBox_noise.valueChanged.connect(lambda: self.change_noiseThreshold(self.wg_rs.dsBox_noise.value()))
        self.wg_rs.sBox_shading.valueChanged.connect(lambda: self.change_shadingRate(self.wg_rs.sBox_shading.value()))
        self.wg_rs.sBox_bucket.valueChanged.connect(lambda: self.change_bucketSize(self.wg_rs.sBox_bucket.value()))
        self.wg_rs.pBtn_vfb.clicked.connect(show_vfb)

        self.wg_rs.cBox_lights.stateChanged.connect(lambda: self.toggle_lights(self.wg_rs.cBox_lights.isChecked()))
        self.wg_rs.cBox_gi.stateChanged.connect(lambda: self.toggle_gi(self.wg_rs.cBox_gi.isChecked()))
        self.wg_rs.cBox_shadows.stateChanged.connect(lambda: self.toggle_shadows(self.wg_rs.cBox_shadows.isChecked()))
        self.wg_rs.cBox_displacement.stateChanged.connect(lambda: self.toggle_displacement(self.wg_rs.cBox_displacement.isChecked()))
        self.wg_rs.cBox_colorspace.currentTextChanged.connect(lambda: self.change_colorspace(self.wg_rs.cBox_colorspace.currentText()))
        self.wg_rs.cBox_ground_plane.stateChanged.connect(self.toggle_ground_plane)
        self.wg_rs.cBox_vertical_rot.stateChanged.connect(self.enable_vertical_rotation)
        self.wg_rs.btn_vertical_rotator.clicked.connect(lambda: ct.TT_Setup().get_asset_center())

    def connect_aov_checkbox(self):
        self.wg_aov.cBox_Lighting.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Lighting.objectName()))
        self.wg_aov.cBox_GlobalIllumination.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_GlobalIllumination.objectName()))
        self.wg_aov.cBox_Reflection.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Reflection.objectName()))
        self.wg_aov.cBox_CoatReflection.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_CoatReflection.objectName()))
        self.wg_aov.cBox_Refraction.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Refraction.objectName()))
        self.wg_aov.cBox_Specular.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Specular.objectName()))
        self.wg_aov.cBox_CoatSpecular.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_CoatSpecular.objectName()))
        self.wg_aov.cBox_SSS2.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_SSS2.objectName()))
        self.wg_aov.cBox_SelfIllumination.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_SelfIllumination.objectName()))
        self.wg_aov.cBox_Atmosphere.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Atmosphere.objectName()))
        self.wg_aov.cBox_Background.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Background.objectName()))
        self.wg_aov.cBox_DiffuseFilter.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_DiffuseFilter.objectName()))
        self.wg_aov.cBox_ReflectionFilter.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_ReflectionFilter.objectName()))
        self.wg_aov.cBox_ReflectGlossiness.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_ReflectGlossiness.objectName()))
        self.wg_aov.cBox_CoatFilter.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_CoatFilter.objectName()))
        self.wg_aov.cBox_CoatGlossiness.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_CoatGlossiness.objectName()))
        self.wg_aov.cBox_RefractionFilter.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_RefractionFilter.objectName()))
        self.wg_aov.cBox_Shadows.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Shadows.objectName()))
        self.wg_aov.cBox_BumpNormals.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_BumpNormals.objectName()))
        self.wg_aov.cBox_Normals.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Normals.objectName()))
        self.wg_aov.cBox_ZDepth.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_ZDepth.objectName()))
        self.wg_aov.cBox_Wireframe.clicked.connect(lambda: self.set_aov(self.wg_aov.cBox_Wireframe.objectName()))

    def get_aovs(self):
        re = rt.MaxOps.GetCurRenderElementMgr()
        re_amount = re.NumRenderElements()
        for re_index in range(0, re_amount):
            aov = re.GetRenderElement(re_index)
            if aov.elementname != 'Alpha':
                object_name = 'cBox_' + str(aov.elementname)
                check_box = self.wg_aov.findChild(QCheckBox, object_name)
                check_box.setChecked(aov.vrayVFB)

    def set_aov(self, aov_name):
        re = rt.MaxOps.GetCurRenderElementMgr()
        re_amount = re.NumRenderElements()
        aov_name = aov_name.replace('cBox_', '')
        for re_index in range(0, re_amount):
            aov = re.GetRenderElement(re_index)
            if aov.elementname == aov_name:
                check_box = self.wg_aov.findChild(QCheckBox, 'cBox_' + aov_name)
                aov.vrayVFB = check_box.isChecked()

    def clicked_resolution_720(self):
        self.wg_rs.sBox_width.setValue(1280)
        self.wg_rs.sBox_height.setValue(720)

    def clicked_resolution_1080(self):
        self.wg_rs.sBox_width.setValue(1920)
        self.wg_rs.sBox_height.setValue(1080)

    def clicked_resolution_1440(self):
        self.wg_rs.sBox_width.setValue(2560)
        self.wg_rs.sBox_height.setValue(1440)

    def clicked_resolution_2160(self):
        self.wg_rs.sBox_width.setValue(3840)
        self.wg_rs.sBox_height.setValue(2160)

    def refresh_render_settings(self):
        vr = self.get_vray()
        vr.output_saveRawFile = True
        rt.rendTimeType = 3

        self.wg_rs.sBox_width.setValue(rt.renderWidth)
        self.wg_rs.sBox_height.setValue(rt.renderHeight)

        self.wg_rs.sBox_startFrame.setValue(rt.rendStart)
        self.wg_rs.sBox_endFrame.setValue(rt.rendEnd)
        self.wg_rs.sBox_nth.setValue(rt.rendNThFrame)

        self.wg_rs.sBox_minSubdiv.setValue(vr.twoLevel_baseSubdivs)
        self.wg_rs.sBox_maxSubdiv.setValue(vr.twoLevel_fineSubdivs)
        self.wg_rs.dsBox_noise.setValue(vr.twoLevel_threshold)
        self.wg_rs.sBox_shading.setValue(vr.imageSampler_shadingRate)
        self.wg_rs.sBox_bucket.setValue(vr.twoLevel_bucket_width)
        self.wg_rs.cBox_lights.setChecked(vr.options_lights)
        self.wg_rs.cBox_gi.setChecked(vr.gi_on)
        self.wg_rs.cBox_shadows.setChecked(vr.options_shadows)
        self.wg_rs.cBox_displacement.setChecked(vr.options_displacement)
        self.wg_rs.cBox_colorspace.setCurrentIndex(self.set_colorspace())
        self.get_ground_plane()

    def set_colorspace(self):
        vr = self.get_vray()
        index = vr.options_rgbColorSpace - 1
        return index

    def inital_render_settings(self, rs_preset):
        #Set VRay as current render
        vr = self.get_vray()
        vr.output_saveRawFile = True
        rt.rendTimeType = 3

        if rs_preset == 'High':
            rs_high_path = RS_PATH + "RS_High.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))

        elif rs_preset == 'Medium':
            rs_high_path = RS_PATH + "RS_Medium.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))

        elif rs_preset == 'Low':
            rs_high_path = RS_PATH + "RS_Low.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))

    def change_render_preset(self, rs_preset):
        self.inital_render_settings(rs_preset)
        self.refresh_render_settings()
        self.wg_rs.cBox_renderSettings.setCurrentText(rs_preset)


    def include_asset_to_wireframe(self, asset):
        re = rt.MaxOps.GetCurRenderElementMgr()
        re_amount = re.NumRenderElements()
        asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')

        for re_index in range(0, re_amount):
            aov = re.GetRenderElement(re_index)
            if aov.elementname == 'Wireframe':
                if aov.includeList == None:
                    aov.includeList = rt.array(asset)
                    aov.texture = self.create_vray_edges()
                    aov.elementname = 'Wireframe'
                else:
                    new_array = rt.array()
                    for mesh in list(aov.includeList):
                        rt.append(new_array, mesh)
                    rt.append(new_array, asset)
                    aov.includeList = new_array

    def create_vray_edges(self):
        wireframe = rt.VRayEdgesTex()
        wireframe.PixelWidth = 0.5
        return wireframe

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
        # Fix if dont have domeligth
        initial_rotation = 0
        for domeLight in ct.TT_Setup().get_domeLights():
            if domeLight.texmap != None:
                initial_rotation = ct.TT_Setup().get_dome_rotation(domeLight)

        rt.rendStart = frame
        self.update_framerange(initial_rotation, self.wg_rs.cBox_vertical_rot.isChecked())
        rt.renderSceneDialog.update()

    def change_endFrame(self, frame):
        # Fix if dont have domeligth
        initial_rotation = 0
        for domeLight in ct.TT_Setup().get_domeLights():
            if domeLight.texmap != None:
                initial_rotation = ct.TT_Setup().get_dome_rotation(domeLight)

        rt.rendEnd = frame
        self.update_framerange(initial_rotation, self.wg_rs.cBox_vertical_rot.isChecked())
        rt.renderSceneDialog.update()

    def change_nthFrame(self, value):
        rt.rendNThFrame = value
        rt.renderSceneDialog.update()

    def change_minSubdiv(self, value):
        self.wg_rs.cBox_renderSettings.setCurrentText('Custom')
        vr = self.get_vray()
        vr.twoLevel_baseSubdivs = value

    def change_maxSubdiv(self, value):
        self.wg_rs.cBox_renderSettings.setCurrentText('Custom')
        vr = self.get_vray()
        vr.twoLevel_fineSubdivs = value

    def change_noiseThreshold(self, value):
        self.wg_rs.cBox_renderSettings.setCurrentText('Custom')
        vr = self.get_vray()
        vr.twoLevel_threshold = value

    def change_shadingRate(self, value):
        self.wg_rs.cBox_renderSettings.setCurrentText('Custom')
        vr = self.get_vray()
        vr.imageSampler_shadingRate = value

    def change_bucketSize(self, value):
        self.wg_rs.cBox_renderSettings.setCurrentText('Custom')
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

    def get_ground_plane(self):
        ground_plane = rt.getNodeByName('Ground_Plane')
        if ground_plane.isHidden:
            self.wg_rs.cBox_ground_plane.setChecked(False)
        else:
            self.wg_rs.cBox_ground_plane.setChecked(True)

    def toggle_ground_plane(self):
        ground_plane = rt.getNodeByName('Ground_Plane')

        if self.wg_rs.cBox_ground_plane.isChecked():
            ground_plane.isHidden = False
        else:
            ground_plane.isHidden = True

    def enable_vertical_rotation(self, v_rot):
        initial_rotation = 0
        for domeLight in ct.TT_Setup().get_domeLights():
            if domeLight.texmap != None:
                initial_rotation = ct.TT_Setup().get_dome_rotation(domeLight)

        self.update_framerange(initial_rotation, self.wg_rs.cBox_vertical_rot.isChecked())

    def update_framerange(self, initial_rotation, v_rot):
        # Update Asset Rotation
        asset_ctrl = rt.getNodeByName('TT_Assets_ctrl')
        ct.TT_Setup().asset_hrotation(asset_ctrl, v_rot)

        # Update Dome Rotation
        for domeLight in ct.TT_Setup().get_domeLights():
            if domeLight.texmap:
                ct.TT_Setup().dome_rotation(domeLight, initial_rotation)

        rt.animationRange = rt.interval(rt.rendStart, rt.rendEnd)


class VFB_DOCK(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(VFB_DOCK, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.initUI()

    def initUI(self):
        # Load MainUI
        main_window = qtmax.GetQMaxMainWindow()
        main_layout = QtWidgets.QVBoxLayout()
        vfb_render_view = main_window.findChild(QtWidgets.QWidget, 'vray_vfb_renderview')
        vfb_main = vfb_render_view.parent()
        vfb_history = vfb_main.parent()
        vfb_stats = vfb_history.parent()
        vfb_widget = vfb_stats.parent()
        self.vfb_util = vfb_widget
        self.vfb_util.setLayout(main_layout)
        self.setWidget(self.vfb_util)

def show_vfb():
    rt.execute("vfbControl #show")
    main_window = qtmax.GetQMaxMainWindow()
    main_widget = main_window.findChild(QtWidgets.QDockWidget, 'VFB_dock')
    if main_widget:
        main_widget.close()

    main_widget = VFB_DOCK(parent=main_window)
    main_widget.setObjectName('VFB_dock')
    main_widget.setFloating(True)
    main_widget.show()

