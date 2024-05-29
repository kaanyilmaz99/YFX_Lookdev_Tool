# Description

<<<<<<< HEAD
The YFX - Lookdev Tool helps you to create a Turntable setup with all the necessary functions in a quick and simple way.  You won't need to setup anything in your scene, but can jump right into the fun Lookdev of your desired asset with just a few clicks.  Furthermore you still have the options to customize your scene as you prefer with the most important options available in the UI.

# Features

=======
The YFX - Lookdev Tool for 3dsMax helps you to create a Turntable setup with all the necessary functions in a quick and simple way.  You won't need to setup anything in your scene, but can jump right into the fun Lookdev of your desired asset with just a few clicks.  Furthermore you still have the options to customize your scene as you prefer with the most important options available in the UI.

# Asset Example
![](./gifs/Xerjoff_Turntable.gif)

![](./gifs/Xerjoff_Tutorial.gif)

# Features

 - [x] Works with 3dsMax 2022, 2023 and 2024
>>>>>>> develop
 - [x] Dynamic Turntable Creation
 - [x] Incremental Save options
 - [x] Asset Importer
 - [x] Texture Importer with UDIM support
<<<<<<< HEAD
 - [x] Create as many HDRIs as you need
=======
 - [x] Create as many HDRIs as you want
>>>>>>> develop
 - [x] Multiple Background options and HDRI Ground Projection
 - [x] Create as many Cameras as you need
 - [x] MacBeth Charts/Reference Sphere creation
 - [x] Changing the Focal Length of the Camera will keep the Charts in the same position
 - [x] Changing the Frame Range will dynamically update the Turntable animations
 - [x] Vertical Asset Rotation support
 - [x] Exposed Render Settings
 - [x] AOV Creation
<<<<<<< HEAD
 - [x] Dockable V-Ray FrameBuffer
=======
 - [x] V-Ray CPU and GPU render
 - [x] Dockable V-Ray FrameBuffer (experimental)
 
</br>
>>>>>>> develop

# How it works

1.) </br>
<<<<<<< HEAD
After downloading the tool, just execute the 3dsMax.bat file and it launches the software with all the scripts. You should see a new button appearing in the top toolbar of your 3dsMax main window. After clicking the button, it will open up the Main UI of the tool, which can be docked anywhere in the software.

2.) </br>
Next in the tool press the folder button to search for your desired 3D Model. Then press the **Create Turntable** button to build the scene and import your file. Inside the **Asset Tab** you can choose more mesh files to import and also change the subdivisions of existing assets. 

3.) </br>
In the **Texture Tab** you can specify your texture folder and import your textures directly into the Material Editor. It will recognize **UDIM** files and will create a VRay Bitmap node per texture. You can also create a Base Material, which will connect all your textures automatically.

4.) </br>
In the **HDRI Tab** you can import any HDRI map of your choice into the scene. First type in a name and then press **Create HDRI**. Now you can choose a .HDRI file by clicking the **Folder Icon** button. After that your DomeLight is set up your scene lit. Clicking the **Edit Icon** button will let you change a few DomeLight properties and also has a few different Background options.

5.) </br>
To create a camera for the scene, go to the **Camera** tab, type in a name and press **Create Camera**. The camera will be created based on your perspective view. Together with the camera comes also the reference spheres with MacBeth Charts. You can simply change the focal length in the tab and the charts will stick with it.

6.)</br>
In the **Render Tab** you can specify the render location and simply hit **Render**. You can also open up the *Render Settings* rollout to tweak a few parameters. Changing the *Frame Range* will automatically update all the Turntable animations to the desired length. You can also enable **Vertical asset rotation**, however if you transform your asset you need to press **Update Vertical Rotator** to center the pivot for the vertical animation.
Further down in the VRay Settings you can choose between different **Quality Presets** or you tweak the parameters manually. Under **Global Switches** you can define the Colorspace and if you choose **ACES** you can set up an ocio path manually if you don't have it set up in the environment variable already.
In the **AOVs** rollout you can choose which Render Elements you want to use  *(all are enabled by default)*.
=======
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
>>>>>>> develop

# To do List

- Maya, Houdini support
- Nuke slapcomp support
<<<<<<< HEAD
- Support for different Render Engines
=======
- Support for different render engines
>>>>>>> develop
- More Material options
- Add Asset Displacement Modifier
- More exposed parameters for HDRIs and Assets

# Author

Kaan Yilmaz | kaan.yilmaz99@t-online.de