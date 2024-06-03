# Description

The YFX - Lookdev Tool for 3dsMax and V-Ray helps you to create a Turntable setup with all the necessary functions in a quick and simple way. Easily setup your desired turntable scene and jump right into the fun Lookdev part of your asset.

# Asset Example
[![](https://pouch.jumpshare.com/preview/x6ZvJSdmp7wbmzE6SpdCvBBDeQqvoy58b8TkViqGB5Zw2qOZfE6tAVBIAoTccmWB3TA_CwPmw6qn_KvwVpx27OT13FYvCTNItZ0oPSkH8ts)](https://vimeo.com/951345783/7e94697cd7?share=copy)
[![](https://pouch.jumpshare.com/preview/01qXeLuE0p1dLL5Fo7fSQMBEMzPJ_jWX_Ybas9bbrwclukjB2GcHG4Q32BKmRAagcAi-YJbcNn0hYL1TKPKiRuNHVubqdj4gFwViQJUQHBg)](https://vimeo.com/951768034/231d72b232?share=copy)

# Features

 - [x] Works with 3dsMax 2022, 2023 and 2024
 - [x] Dynamic Turntable Creation
 - [x] Incremental Save options
 - [x] Asset Importer
 - [x] Texture Importer with UDIM support
 - [x] Create as many HDRIs as you want
 - [x] Multiple Background options and HDRI Ground Projection
 - [x] Create as many Cameras as you need
 - [x] MacBeth Charts/Reference Sphere creation
 - [x] Changing the Focal Length of the Camera will keep the Charts in the same position
 - [x] Changing the Frame Range will dynamically update the Turntable animations
 - [x] Vertical Asset Rotation support
 - [x] Exposed Render Settings
 - [x] AOV Creation
 - [x] V-Ray CPU and GPU render
 - [x] Dockable V-Ray FrameBuffer (experimental)
 

# How it works

1.) </br>
After downloading the tool, execute one of the 3dsMax.bat files inside the **YFX_Lookdev_Tool** folder. As soon as 3dsMax has launched you should see the **YFX** button in the top toolbar. Press the button and the YFX UI will show up.

2.) </br>
In the **Home Tab** choose an Asset by clicking the Folder button. Then press **Create Turntable** and your asset will be imported into your new Turntable scene. Now you can **Save** your scene.

3.) </br>
In the **Asset Tab** you will now scene your imported Asset. You can add more assets by pressing the **Folder Icon**. Clicking on the **Cube Icon** in your asset list will toggle the visibility. To change the name press the **Edit Icon**, type in a new name and apply the changes. You can also just delete the asset.

4.) </br>
In the **Texture Tab** you can specify and texture folder to import them into the Material Editor. You can also create a Base Material based on your available textures.

5.) </br>
In the **HDRI Tab** you can create as many HDRIs as you want. Just type in the desired name, press **Create HDRI** and choose a hdri map by clicking on the **Folder Icon**. Inside the **Edit Options** you can change a few exposed parameters of the HDRI and also edit the Background settings.

6.) </br>
Similar to the previous tab in the next one you can create *Cameras*. The camera will also come with macbeth charts and reference sphere, which will be parented to it. Clicking on the **Camera Icon** will hide the camera or enables it and also changes your view to that camera.
Changing the focal length will not affect the position of the charts/reference spheres. Inside the **Edit Options** you can change a few more camera settings and also hide the charts and spheres.

7.) </br>
In the **Render Tab** you can specify your output path and also change the render engine. Expose the **Render Settings** section and change a few exposed parameters. If you change the frame range, the whole turntable animation will update dynamically. You can also enable a vertical rotation for your asset.
Expose the **AOV** section to toggle the AOVs you want to render.
If you have set up everything you can just it the **Render** button and it will render out the turntable with the enabled camera.

# To do List

- Nuke slapcomp support
- Support for different render engines
- More Material options
- Add Asset Displacement Modifier
- More exposed parameters for HDRIs and Assets

# Author

Kaan Yilmaz | kaan.yilmaz99@t-online.de
