# Description

The YFX - Lookdev Tool for 3dsMax helps you to create a Turntable setup with all the necessary functions in a quick and simple way.  You won't need to setup anything in your scene, but can jump right into the fun Lookdev of your desired asset with just a few clicks.  Furthermore you still have the options to customize your scene as you prefer with the most important options available in the UI.

# Asset Example
![](./gifs/Xerjoff_Turntable.gif)

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
 
</br>

# How it works

1.) </br>
After downloading the tool, execute the 3dsMax.bat file. After 3dsMax has launched you should see the **YFX** button in the top toolbar. Press the button and the YFX UI will show up.

2.) </br>
In the **Home Tab** choose an Asset by clicking the Folder button. Then press **Create Turntable** and your asset will be imported into your new Turntable scene. Now you can **Save** your scene.

3.) </br>
In the **Asset Tab** you will now scene your imported Asset. You can add more assets by pressing the **Folder Icon**. Clicking on the **Cube Icon** in you asset list will toggle the visibility. To change the name press the **Edit Icon**, type in a new name and apply the changes. You can also just delete the asset.

4.) </br>
In the **Texture Tab** you can specify and texture folder to import them into the Material Editor. You can also create a Base Material from your textures.

5.) </br>
In the **HDRI Tab** you can create as many HDRIs as you want. Just type in the desired name, press **Create HDRI** and choose a hdri map by clicking on the **Folder Icon**. Inside the **Edit Options** you can change a few exposed parameters of the HDRI and also edit the Background settings.

6.) </br>
Similar to the previous tab in the **Camera** one you can create cameras. Together with the camera the tool will create charts and reference spheres, which will be parented to the camera. Clicking on the **Camera Icon** will hide the camera or enables it and also changes your view to that camera.
Changing the focal length will not affect the position of the charts/reference spheres as long as you use the Tool for this. Inside the **Edit Options** you can change a few more camera settings and also hide the charts and spheres.

7.) </br>
In the **Render Tab** you can specify your output path and also change the render engine. Expose the **Render Settings** section and change a few exposed parameters. If you change the frame range, the whole turntable animation will update dynamically. You can also enable a vertical rotation for your asset.
Expose the **AOV** section to toggle the AOVs you want to render.
If you have set up everything you can just it the **Render** button and it will render out the turntable with the enabled camera.

# To do List

- Maya, Houdini support
- Nuke slapcomp support
- Support for different render engines
- More Material options
- Add Asset Displacement Modifier
- More exposed parameters for HDRIs and Assets

# Author

Kaan Yilmaz | kaan.yilmaz99@t-online.de