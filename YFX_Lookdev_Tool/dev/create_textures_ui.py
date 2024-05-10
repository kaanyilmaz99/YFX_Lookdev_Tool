#******************************************************************************************************************
# content:        Creates the Textures UI and will be appended to the main ui dynamically.
#                 Also connects all the necessary buttons to its functions.

# dependencies:   PySide2/PyQt, 3dsmax API, main window (qtmax) and maxscript

# how to:         After selecting a texture folder in the MainUI Texture tab, open the Import Texture rollout.
#                 There you will have the option to select the textures files you want to import or instantly create
#                 a base Material

# todos:          More Material options (e.g.: SSS, Carpaint,...)

# author:         Kaan Yilmaz | kaan.yilmaz99@t-online.de
#******************************************************************************************************************

import os
import json
import importlib

import qtmax
from pymxs import runtime as rt

import default_max_functions as dmf

from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtGui, QtUiTools, QtCore
from PySide2.QtCore import Slot, Signal, QProcess, QObject

importlib.reload(dmf)

DIR_PATH = os.path.dirname(__file__)
TEX_UI_PATH = DIR_PATH + r'\UI\textures_UI.ui'

class Textures():
    def __init__(self, path):
        self.path = path

    def show_import_textures(self, parent):
        self.wg_util = parent
        self.wg_tex = QtUiTools.QUiLoader().load(TEX_UI_PATH)
        self.wg_tex.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        layout_tex = self.wg_util.findChild(QVBoxLayout, 'layout_tex')
        layout_tex.insertWidget(1, self.wg_tex)

        self.connect_texture_buttons()
        self.get_all_textures()
        self.add_texture_to_list()

    def hide_import_textures(self, parent):
        self.wg_util = parent
        layout_tex = self.wg_util.findChild(QWidget, 'wg_tex')
        layout_tex.deleteLater()

    def connect_texture_buttons(self):
        self.wg_tex.btn_import_textures.clicked.connect(lambda: self.import_textures())
        self.wg_tex.btn_create_material.clicked.connect(self.create_base_material)

    def reload_texture_list(self):
        self.get_all_textures()
        self.add_texture_to_list()

    def get_node_view(self):
        if rt.sme.GetViewByName('Working_Space') == 0:
            rt.sme.CreateView(rt.Name('Working_Space'))
        node_view = rt.sme.GetView(rt.sme.GetViewByName('Working_Space'))
        return node_view

# EXECUTE BUTTONS ----------------------------------------------------------------------------------------------------------------

    def import_textures(self):
        node_view = self.get_node_view()
        line_edit = self.wg_util.findChild(QtWidgets.QLineEdit, 'line_texture_path')

        y_pos = 0
        for item in self.wg_tex.list_textures.selectedItems():
            texture = self.create_texture(item.text())
            node_view.createNode(texture, rt.Point2(0, y_pos))
            y_pos = y_pos + 100

    def create_base_material(self):
        rt.sme.Open()
        node_view = self.get_node_view()
        material = dmf.create_vray_material()
        normal_node = rt.VRayNormalMap()

        if self.diffuse_map:
            material.texmap_diffuse = self.create_texture(self.diffuse_map)
        if self.rough_map:
            material.brdf_useRoughness = True
            material.texmap_reflectionGlossiness = self.create_texture(self.rough_map)
        if self.gloss_map:
            material.brdf_useRoughness = False
            material.texmap_reflectionGlossiness = self.create_texture(self.gloss_map)
        if self.spec_map:
            material.texmap_reflection = self.create_texture(self.spec_map)
        if self.metal_map:
            material.texmap_metalness = self.create_texture(self.metal_map)
        if self.bump_map:
            material.texmap_bump = normal_node
            normal_node.bump_map = self.create_texture(self.bump_map)
        if self.normal_map:
            material.texmap_bump = normal_node
            normal_node.normal_map = self.create_texture(self.normal_map)
        if self.opacity_map:
            material.texmap_opacity = self.create_texture(self.opacity_map)
        if self.emission_map:
            material.texmap_self_illumination = self.create_texture(self.emission_map)
        if self.refract_map:
            material.texmap_refraction = self.create_texture(self.refract_map)

        node_view.createNode(material, rt.Point2(0, 0))

    def create_texture(self, texture):
        tex_path = self.path + '/' + texture
        bitmap = dmf.create_bitmap_texture(tex_path)
        return bitmap

# GET ALL TEXTURES ----------------------------------------------------------------------------------------------------------------

    def add_texture_to_list(self):
        for texture in self.textures:
            if texture != None:
                self.wg_tex.list_textures.addItem(texture)

    def get_all_textures(self):
        files = os.listdir(self.path)
        file_formats = ['.exr', '.tif', '.png', '.jpg']
        textures = []
        for file in files:
            for file_format in file_formats:
                if file_format in file:
                    textures.append(file)

        self.textures = []
        self.diffuse_map = self.get_diffuse_texture(textures)
        self.textures.append(self.diffuse_map)
        self.rough_map = self.get_rough_texture(textures)
        self.textures.append(self.rough_map)
        self.gloss_map = self.get_gloss_texture(textures)
        self.textures.append(self.gloss_map)
        self.spec_map = self.get_spec_texture(textures)
        self.textures.append(self.spec_map)
        self.metal_map = self.get_metal_texture(textures)
        self.textures.append(self.metal_map)
        self.bump_map = self.get_bump_texture(textures)
        self.textures.append(self.bump_map)
        self.normal_map = self.get_normal_texture(textures)
        self.textures.append(self.normal_map)
        self.opacity_map = self.get_opacity_texture(textures)
        self.textures.append(self.opacity_map)
        self.disp_map = self.get_disp_texture(textures)
        self.textures.append(self.disp_map)
        self.emission_map = self.get_emission_texture(textures)
        self.textures.append(self.emission_map)
        self.refract_map = self.get_refract_texture(textures)
        self.textures.append(self.refract_map)

    def get_diffuse_texture(self, textures):
        diffuse_names = ['base', 'Base', 'color', 'Color', 'diffuse', 'Diffuse', 'diff', 'Diff']
        for texture in textures:
            for diffuse_name in diffuse_names:
                if diffuse_name in texture:
                    diffuse_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    diffuse_texture = texture[0] + '.<UDIM>.' + diffuse_format
                    return diffuse_texture

    def get_rough_texture(self, textures):
        rough_names = ['roughness', 'Roughness', 'rough', 'Rough']
        for texture in textures:
            for rough_name in rough_names:
                if rough_name in texture:
                    rough_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    rough_texture = texture[0] + '.<UDIM>.' + rough_format
                    return rough_texture

    def get_gloss_texture(self, textures):
        gloss_names = ['glossiness', 'Glossiness', 'gloss', 'Gloss']
        for texture in textures:
            for gloss_name in gloss_names:
                if gloss_name in texture:
                    gloss_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    gloss_texture = texture[0] + '.<UDIM>.' + gloss_format
                    return gloss_texture

    def get_spec_texture(self, textures):
        spec_names = ['specular', 'Specular', 'spec', 'Spec']
        for texture in textures:
            for spec_name in spec_names:
                if spec_name in texture:
                    spec_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    spec_texture = texture[0] + '.<UDIM>.' + spec_format
                    return spec_texture

    def get_metal_texture(self, textures):
        metal_names = ['metalness', 'Metalness', 'metal', 'Metal']
        for texture in textures:
            for metal_name in metal_names:
                if metal_name in texture:
                    metal_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    metal_texture = texture[0] + '.<UDIM>.' + metal_format
                    return metal_texture

    def get_bump_texture(self, textures):
        bump_names = ['bump', 'Bump', 'bmp', 'Bmp']
        for texture in textures:
            for bump_name in bump_names:
                if bump_name in texture:
                    bump_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    bump_texture = texture[0] + '.<UDIM>.' + bump_format
                    return bump_texture

    def get_normal_texture(self, textures):
        normal_names = ['normal', 'Normal', 'nrml', 'Nrml']
        for texture in textures:
            for normal_name in normal_names:
                if normal_name in texture:
                    normal_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    normal_texture = texture[0] + '.<UDIM>.' + normal_format
                    return normal_texture

    def get_opacity_texture(self, textures):
        opacity_names = ['opacity', 'Opacity']
        for texture in textures:
            for opacity_name in opacity_names:
                if opacity_name in texture:
                    opacity_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    opacity_texture = texture[0] + '.<UDIM>.' + opacity_format
                    return opacity_texture

    def get_disp_texture(self, textures):
        disp_names = ['displacement', 'Displacement', 'disp', 'Disp']
        for texture in textures:
            for disp_name in disp_names:
                if disp_name in texture:
                    disp_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    disp_texture = texture[0] + '.<UDIM>.' + disp_format
                    return disp_texture

    def get_refract_texture(self, textures):
        refract_names = ['refraction', 'Refraction', 'refract', 'Refract', 'transmission', 'Transmission']
        for texture in textures:
            for refract_name in refract_names:
                if refract_name in texture:
                    refract_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    refract_texture = texture[0] + '.<UDIM>.' + refract_format
                    return refract_texture

    def get_emission_texture(self, textures):
        emission_names = ['emission', 'Emission', 'selfIllum', 'SelfIllum', 'illum', 'Illum']
        for texture in textures:
            for emission_name in emission_names:
                if emission_name in texture:
                    emission_format = texture.split('.')[-1]
                    texture = texture.split('.')[:-1]
                    emission_texture = texture[0] + '.<UDIM>.' + emission_format
                    return emission_texture

