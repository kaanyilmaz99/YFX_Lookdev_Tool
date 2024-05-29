#******************************************************************************************************************
# content:        Creates the Render Settings UI after importing and will be appended to the main ui dynamically.
#                 Also connects all the necessary buttons to its functions.

# dependencies:   PySide2/PyQt, 3dsmax API, main window (qtmax) and maxscript

# how to:         In the RENDER tab you have the option to choose different settings

# todos:          Add different render engines (next Arnold renderer)

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#******************************************************************************************************************

import os
import json

import qtmax
from pymxs import runtime as rt

import create_turntable as ct
import default_max_functions as dmf

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject

DIR_PATH = os.path.dirname(__file__)
RS_PATH = DIR_PATH + r'\render_presets/'
RS_UI_PATH = DIR_PATH + r'\UI\renderSettings_UI.ui'
VRAY_UI_PATH = DIR_PATH + r'\UI\vray_settings_UI.ui'
VRAY_GPU_UI_PATH = DIR_PATH + r'\UI\vray_gpu_settings_UI.ui'
AOV_UI_PATH = DIR_PATH + r'\UI\aov_UI.ui'
JSON_PATH = DIR_PATH + r'\Turntable_Configuration.json'

# READ .JSON CONFIG FILE  ------------------------------------------------------------------------------------------------------------------------------------------------

with open(JSON_PATH) as json_file:
    data = json.load(json_file)

init_start_frame = data['Start Frame']
init_end_frame = data['End Frame']
init_width = data['Width']
init_height = data['Height']
init_nth_frame = data['Nth Frame']
init_v_asset_rot = data['Vertical Asset Rotation']
init_render_preset = data['Quality Preset']

class Render_Settings():

# SET UP INITIAL SETTINGS FROM THE CONFIG FILE ---------------------------------------------------------------------------------------------------------------------------

    def setup_initial_settings(self):
        vr = dmf.get_vray()
        vr.output_saveRawFile = True

        rs_high_path = DIR_PATH + r'\render_presets\RS_' + init_render_preset + '.rps'
        rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 4, 32))

        rt.rendTimeType = 3
        rt.renderWidth = init_width
        rt.renderHeight = init_height
        rt.rendStart = init_start_frame
        rt.rendEnd = init_end_frame
        rt.animationRange = rt.interval(init_start_frame, init_end_frame)
        rt.rendNThFrame = init_nth_frame
        self.toggle_vertical_rotation(init_v_asset_rot)

        re = rt.MaxOps.GetCurRenderElementMgr()
        re.AddRenderElement(rt.VRayExtraTex(elementname='Wireframe'))

# RENDER SETTINGS  ------------------------------------------------------------------------------------------------------------------------------------------------------

    def show_render_settings(self, parent, render_engine):
        self.wg_util = parent
        self.wg_rs = QtUiTools.QUiLoader().load(RS_UI_PATH)
        self.wg_rs.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout_rs = self.wg_util.findChild(QVBoxLayout, 'layout_rs')
        layout_rs.insertWidget(1, self.wg_rs)

        self.add_render_engine(render_engine)
        self.refresh_render_settings()
        self.connect_common_settings()

    def hide_render_settings(self, parent):
        self.wg_util = parent
        layout_rs = self.wg_util.findChild(QWidget, 'wg_rs')
        layout_rs.deleteLater()

    def add_render_engine(self, render_engine):
        if render_engine == 'V-Ray':
            self.wg_vray = QtUiTools.QUiLoader().load(VRAY_UI_PATH)
            layout_settings = self.wg_rs.findChild(QVBoxLayout, 'layout_render_settings')
            layout_settings.insertWidget(1, self.wg_vray)
            self.connect_vray_settings()
            self.refresh_vray_settings()

        elif render_engine == 'V-Ray GPU':
            self.wg_vray_gpu = QtUiTools.QUiLoader().load(VRAY_GPU_UI_PATH)
            layout_settings = self.wg_rs.findChild(QVBoxLayout, 'layout_render_settings')
            layout_settings.insertWidget(1, self.wg_vray_gpu)
            self.connect_vray_gpu_settings()
            self.refresh_vray_gpu_settings()

    def connect_vray_gpu_settings(self):
        self.wg_vray_gpu.sBox_gpu_samples.valueChanged.connect(lambda: self.change_samples(self.wg_vray_gpu.sBox_gpu_samples.value()))
        self.wg_vray_gpu.dsBox_gpu_noise.valueChanged.connect(lambda: self.change_gpu_noise(self.wg_vray_gpu.dsBox_gpu_noise.value()))
        self.wg_vray_gpu.dsBox_gpu_noise.valueChanged.connect(lambda: self.change_gpu_noise(self.wg_vray_gpu.dsBox_gpu_noise.value()))
        self.wg_vray_gpu.cBox_engine.currentTextChanged.connect(lambda: self.change_engine(self.wg_vray_gpu.cBox_engine.currentText()))
        self.wg_vray_gpu.cBox_displacement.stateChanged.connect(lambda: self.toggle_gpu_displacement(self.wg_vray_gpu.cBox_displacement.isChecked()))

    def connect_vray_settings(self):
        self.wg_vray.cBox_renderSettings.currentTextChanged.connect(lambda: self.change_render_preset(self.wg_vray.cBox_renderSettings.currentText()))
        self.wg_vray.sBox_minSubdiv.valueChanged.connect(lambda: self.change_minSubdiv(self.wg_vray.sBox_minSubdiv.value()))
        self.wg_vray.sBox_maxSubdiv.valueChanged.connect(lambda: self.change_maxSubdiv(self.wg_vray.sBox_maxSubdiv.value()))
        self.wg_vray.dsBox_noise.valueChanged.connect(lambda: self.change_noiseThreshold(self.wg_vray.dsBox_noise.value()))
        self.wg_vray.sBox_shading.valueChanged.connect(lambda: self.change_shadingRate(self.wg_vray.sBox_shading.value()))
        self.wg_vray.sBox_bucket.valueChanged.connect(lambda: self.change_bucketSize(self.wg_vray.sBox_bucket.value()))

        self.wg_vray.cBox_lights.stateChanged.connect(lambda: self.toggle_lights(self.wg_vray.cBox_lights.isChecked()))
        self.wg_vray.cBox_gi.stateChanged.connect(lambda: self.toggle_gi(self.wg_vray.cBox_gi.isChecked()))
        self.wg_vray.cBox_shadows.stateChanged.connect(lambda: self.toggle_shadows(self.wg_vray.cBox_shadows.isChecked()))
        self.wg_vray.cBox_displacement.stateChanged.connect(lambda: self.toggle_displacement(self.wg_vray.cBox_displacement.isChecked()))

    def connect_common_settings(self):
        self.wg_rs.pBtn_720.clicked.connect(self.clicked_resolution_720)
        self.wg_rs.pBtn_1080.clicked.connect(self.clicked_resolution_1080)
        self.wg_rs.pBtn_1440.clicked.connect(self.clicked_resolution_1440)
        self.wg_rs.pBtn_2160.clicked.connect(self.clicked_resolution_2160)
        self.wg_rs.sBox_width.valueChanged.connect(lambda: self.change_resolution_width(self.wg_rs.sBox_width.value()))
        self.wg_rs.sBox_height.valueChanged.connect(lambda:self.change_resolution_height(self.wg_rs.sBox_height.value()))
        self.wg_rs.sBox_startFrame.valueChanged.connect(lambda: self.change_startFrame(self.wg_rs.sBox_startFrame.value()))
        self.wg_rs.sBox_endFrame.valueChanged.connect(lambda: self.change_endFrame(self.wg_rs.sBox_endFrame.value()))
        self.wg_rs.sBox_nth.valueChanged.connect(lambda: self.change_nthFrame(self.wg_rs.sBox_nth.value()))

        self.wg_rs.cBox_vertical_rot.stateChanged.connect(lambda: self.toggle_vertical_rotation(self.wg_rs.cBox_vertical_rot.isChecked()))
        self.wg_rs.btn_vertical_rotator.clicked.connect(lambda: ct.TT_Setup().get_asset_center())

        self.wg_rs.cBox_ground_plane.stateChanged.connect(self.toggle_ground_plane)
        
        self.wg_rs.cBox_colorspace.currentTextChanged.connect(lambda: self.change_colorspace(self.wg_rs.cBox_colorspace.currentText()))
        self.wg_rs.btn_ocio.clicked.connect(self.choose_ocio_file)
        self.wg_rs.line_ocio.textChanged.connect(self.set_ocio_path)

# RENDER SETTINGS - COMMON PARAMETERS ---------------------------------------

    def change_resolution_width(self, width):
        rt.renderWidth = width
        rt.renderSceneDialog.update()

    def change_resolution_height(self, height):
        rt.renderHeight = height
        rt.renderSceneDialog.update()

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

    def change_startFrame(self, frame):
        initial_rotation = dmf.get_inital_domeLight_rotation()
        rt.rendStart = frame
        dmf.update_framerange(initial_rotation, self.wg_rs.cBox_vertical_rot.isChecked())

    def change_endFrame(self, frame):
        initial_rotation = dmf.get_inital_domeLight_rotation()
        rt.rendEnd = frame
        dmf.update_framerange(initial_rotation, self.wg_rs.cBox_vertical_rot.isChecked())

    def change_nthFrame(self, value):
        rt.rendNThFrame = value
        rt.renderSceneDialog.update()

    def toggle_vertical_rotation(self, v_rot):
        initial_rotation = dmf.get_inital_domeLight_rotation()
        dmf.update_framerange(initial_rotation, v_rot)

# RENDER SETTINGS - V-RAY PARAMETERS ---------------------------------------

    def change_render_preset(self, rs_preset):
        self.initial_render_settings(rs_preset)
        self.refresh_vray_settings()
        self.wg_vray.cBox_renderSettings.setCurrentText(rs_preset)

    def initial_render_settings(self, rs_preset):
        vr = dmf.get_vray()
        vr.output_saveRawFile = True
        rt.rendTimeType = 3
        if 'GPU' in dmf.get_current_render():
            colorspace = vr.V_Ray_settings.options_rgbColorSpace - 1
        else:
            colorspace = vr.options_rgbColorSpace - 1

        if colorspace:
            colorspace = 'ACES'
        else:
            colorspace = 'sRGB'

        if rs_preset == 'High':
            rs_high_path = RS_PATH + "RS_High.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))
            self.change_colorspace(colorspace)

        elif rs_preset == 'Medium':
            rs_high_path = RS_PATH + "RS_Medium.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))
            self.change_colorspace(colorspace)

        elif rs_preset == 'Low':
            rs_high_path = RS_PATH + "RS_Low.rps"
            rt.renderpresets.Load(0, rs_high_path, rt.BitArray(2, 32))
            self.change_colorspace(colorspace)

    def change_minSubdiv(self, value):
        self.wg_vray.cBox_renderSettings.setCurrentText('Custom')
        vr = dmf.get_vray()
        vr.twoLevel_baseSubdivs = value

    def change_maxSubdiv(self, value):
        self.wg_vray.cBox_renderSettings.setCurrentText('Custom')
        vr = dmf.get_vray()
        vr.twoLevel_fineSubdivs = value

    def change_noiseThreshold(self, value):
        self.wg_vray.cBox_renderSettings.setCurrentText('Custom')
        vr = dmf.get_vray()
        vr.twoLevel_threshold = value

    def change_shadingRate(self, value):
        self.wg_vray.cBox_renderSettings.setCurrentText('Custom')
        vr = dmf.get_vray()
        vr.imageSampler_shadingRate = value

    def change_bucketSize(self, value):
        self.wg_vray.cBox_renderSettings.setCurrentText('Custom')
        vr = dmf.get_vray()
        vr.twoLevel_bucket_width = value

# RENDER SETTINGS - V-RAY GPU PARAMETERS ------------------------------------

    def change_samples(self, value):
        vr = dmf.get_vray_gpu()
        vr.max_paths_per_pixel = value

    def change_gpu_noise(self, value):
        vr = dmf.get_vray_gpu()
        vr.aa_threshold = value

    def change_engine(self, value):
        vr = dmf.get_vray_gpu()
        if value == 'CUDA':
            vr.engine_type = 2
        else:
            vr.engine_type = 3
        rt.renderSceneDialog.update()

    def toggle_gpu_displacement(self, value):
        vr = dmf.get_vray_gpu()
        vr.V_Ray_settings.options_displacement = value

# RENDER SETTINGS - GLOBAL SWITCHES ---------------------------------------

    def toggle_lights(self, value):
        vr = dmf.get_vray()
        vr.options_lights = value

    def toggle_gi(self, value):
        vr = dmf.get_vray()
        vr.gi_on = value

    def toggle_shadows(self, value):
        vr = dmf.get_vray()
        vr.options_shadows = value

    def toggle_displacement(self, value):
        vr = dmf.get_vray()
        vr.options_displacement = value

    def change_colorspace(self, colorspace):
        vr = dmf.get_vray()
        if 'sRGB' in colorspace:
            if 'GPU' in dmf.get_current_render():
                vr.V_Ray_settings.options_rgbColorSpace = 1
            else:
                vr.options_rgbColorSpace = 1

            rt.vfbControl(rt.Name("srgb"), True)
            self.toggle_colorspace_ocio(False)

        elif 'ACES' in colorspace:
            if 'GPU' in dmf.get_current_render():
                vr.V_Ray_settings.options_rgbColorSpace = 2
            else:
                vr.options_rgbColorSpace = 2

            rt.vfbControl(rt.Name("ocio"), True)
            self.toggle_colorspace_ocio(True)
            self.check_ocio_env_variable()

    def toggle_colorspace_ocio(self, condition):
        self.wg_rs.label_ocio.setEnabled(condition)
        self.wg_rs.line_ocio.setEnabled(condition)
        self.wg_rs.btn_ocio.setEnabled(condition)

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

# RENDER SETTINGS - REFRESH --------------------------------------------

    def refresh_render_settings(self):
        vr = dmf.get_vray()
        vr.output_saveRawFile = True
        rt.rendTimeType = 3

        self.wg_rs.sBox_width.setValue(rt.renderWidth)
        self.wg_rs.sBox_height.setValue(rt.renderHeight)
        self.wg_rs.sBox_startFrame.setValue(dmf.get_start_frame())
        self.wg_rs.sBox_endFrame.setValue(dmf.get_end_frame())
        self.wg_rs.sBox_nth.setValue(rt.rendNThFrame)
        self.wg_rs.cBox_colorspace.setCurrentIndex(self.set_colorspace())
        self.check_ocio_env_variable()
        self.get_ground_plane()

    def refresh_vray_settings(self):
        vr = dmf.get_vray()
        self.wg_vray.sBox_minSubdiv.setValue(vr.twoLevel_baseSubdivs)
        self.wg_vray.sBox_maxSubdiv.setValue(vr.twoLevel_fineSubdivs)
        self.wg_vray.dsBox_noise.setValue(vr.twoLevel_threshold)
        self.wg_vray.sBox_shading.setValue(int(vr.imageSampler_shadingRate))
        self.wg_vray.sBox_bucket.setValue(vr.twoLevel_bucket_width)
        self.wg_vray.cBox_lights.setChecked(vr.options_lights)
        self.wg_vray.cBox_gi.setChecked(vr.gi_on)
        self.wg_vray.cBox_shadows.setChecked(vr.options_shadows)
        self.wg_vray.cBox_displacement.setChecked(vr.options_displacement)

    def refresh_vray_gpu_settings(self):
        vr = dmf.get_vray()
        self.wg_vray_gpu.sBox_gpu_samples.setValue(vr.max_paths_per_pixel)
        self.wg_vray_gpu.dsBox_gpu_noise.setValue(vr.aa_threshold)
        self.wg_vray_gpu.cBox_displacement.setChecked(vr.options_displacement)
        if vr.engine_type == 2:
            self.wg_vray_gpu.cBox_engine.setCurrentText('CUDA')
        else:
            self.wg_vray_gpu.cBox_engine.setCurrentText('RTX')

    def check_ocio_env_variable(self):
        if 'OCIO' in os.environ:
            self.wg_rs.line_ocio.setText(os.environ['OCIO'])
            self.set_ocio_path()
            self.toggle_colorspace_ocio(False)

    def set_colorspace(self):
        vr = dmf.get_vray()
        if 'GPU' in dmf.get_current_render():
            index = vr.V_Ray_settings.options_rgbColorSpace - 1
        else:
            index = vr.options_rgbColorSpace - 1

        self.toggle_colorspace_ocio(index)
        return index

    def choose_ocio_file(self):
        ocio_path = QFileDialog.getOpenFileName(None, 'Import Object', 'C:\\', 
              'OCIO File (*.ocio)')
        self.wg_rs.line_ocio.setText(ocio_path[0])

    def set_ocio_path(self):
        rt.vfbControl(rt.Name("ocio"), True)
        rt.vfbControl(rt.Name("loadocio"), self.wg_rs.line_ocio.text())
        rt.vfbControl(rt.Name("ocioinputcolorspace"), 'ACES - ACEScg')
        rt.vfbControl(rt.Name("ociodisplaydevice"), 'ACES')
        rt.vfbControl(rt.Name("ocioviewtransform"), 'srgb')

# AOVS  ----------------------------------------------------------------------------------------------------------------------------------------------------

    def show_aovs(self, parent):
        self.wg_util = parent
        self.wg_aov = QtUiTools.QUiLoader().load(AOV_UI_PATH)
        self.wg_aov.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout_aov = self.wg_util.findChild(QVBoxLayout, 'layout_aov')
        layout_aov.insertWidget(1, self.wg_aov)

        self.get_aovs()
        self.connect_aov_checkbox()

    def hide_aovs(self, parent):
        self.wg_util = parent
        layout_aov = self.wg_util.findChild(QWidget, 'wg_aov')
        layout_aov.deleteLater()

    def connect_aov_checkbox(self):
        self.wg_aov.cBox_Lighting.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Lighting.objectName()))
        self.wg_aov.cBox_GlobalIllumination.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_GlobalIllumination.objectName()))
        self.wg_aov.cBox_Reflection.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Reflection.objectName()))
        self.wg_aov.cBox_CoatReflection.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_CoatReflection.objectName()))
        self.wg_aov.cBox_Refraction.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Refraction.objectName()))
        self.wg_aov.cBox_Specular.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Specular.objectName()))
        self.wg_aov.cBox_CoatSpecular.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_CoatSpecular.objectName()))
        self.wg_aov.cBox_SSS2.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_SSS2.objectName()))
        self.wg_aov.cBox_SelfIllumination.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_SelfIllumination.objectName()))
        self.wg_aov.cBox_Atmosphere.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Atmosphere.objectName()))
        self.wg_aov.cBox_Background.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Background.objectName()))
        self.wg_aov.cBox_DiffuseFilter.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_DiffuseFilter.objectName()))
        self.wg_aov.cBox_ReflectionFilter.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_ReflectionFilter.objectName()))
        self.wg_aov.cBox_ReflectGlossiness.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_ReflectGlossiness.objectName()))
        self.wg_aov.cBox_CoatFilter.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_CoatFilter.objectName()))
        self.wg_aov.cBox_CoatGlossiness.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_CoatGlossiness.objectName()))
        self.wg_aov.cBox_RefractionFilter.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_RefractionFilter.objectName()))
        self.wg_aov.cBox_Shadows.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Shadows.objectName()))
        self.wg_aov.cBox_BumpNormals.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_BumpNormals.objectName()))
        self.wg_aov.cBox_Normals.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Normals.objectName()))
        self.wg_aov.cBox_ZDepth.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_ZDepth.objectName()))
        self.wg_aov.cBox_Wireframe.clicked.connect(lambda: self.set_aovs(self.wg_aov.cBox_Wireframe.objectName()))

    def get_aovs(self):
        re = rt.MaxOps.GetCurRenderElementMgr()
        re_amount = re.NumRenderElements()
        for re_index in range(0, re_amount):
            aov = re.GetRenderElement(re_index)
            if aov.elementname != 'Alpha':
                object_name = 'cBox_' + str(aov.elementname)
                check_box = self.wg_aov.findChild(QCheckBox, object_name)
                check_box.setChecked(aov.vrayVFB)

    def set_aovs(self, aov_name):
        re = rt.MaxOps.GetCurRenderElementMgr()
        re_amount = re.NumRenderElements()
        aov_name = aov_name.replace('cBox_', '')
        for re_index in range(0, re_amount):
            aov = re.GetRenderElement(re_index)
            if aov.elementname == aov_name:
                check_box = self.wg_aov.findChild(QCheckBox, 'cBox_' + aov_name)
                aov.vrayVFB = check_box.isChecked()

# DOCKABLE V-RAY FRAMEBUFFER ----------------------------------------------------------------------------------------------------------------------------------------

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

