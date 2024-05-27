# Description

The YFX - Lookdev Tool for 3dsMax helps you to create a Turntable setup with all the necessary functions in a quick and simple way.  You won't need to setup anything in your scene, but can jump right into the fun Lookdev of your desired asset with just a few clicks.  Furthermore you still have the options to customize your scene as you prefer with the most important options available in the UI.

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
 
Text |  Video
-|-
After downloading the tool, just execute the 3dsMax.bat file </br> and it launches the software with all the scripts. You should see a new button appearing in the top toolbar of your 3dsMax main window. After clicking the button, it will open up the Main UI of the tool. | <img src="./gifs/01_Start_3dsMax.gif" height="270" width="480" />
In the **Home Tab** press the folder button to search for your </br> desired 3D Asset. Then press the **Create Turntable** button to build the scene and import your file. Inside the **Asset Tab** you can choose more mesh files to import and also change the subdivisions of existing assets. | <img src="./gifs/01_Start_3dsMax.gif"/>


# How it works
1.) </br>
After downloading the tool, just execute the 3dsMax.bat file and it launches the software with all the scripts. You should see a new button appearing in the top toolbar of your 3dsMax main window. After clicking the button, it will open up the Main UI of the tool.

2.) </br>
In the **Home Tab** press the folder button to search for your desired 3D Asset. Then press the **Create Turntable** button to build the scene and import your file. Inside the **Asset Tab** you can choose more mesh files to import and also change the subdivisions of existing assets. 

3.) </br>
In the **Texture Tab** you can specify your texture folder and import your textures directly into the Material Editor. It will recognize **UDIM** files and will create a VRay Bitmap node per texture. You can also create a Base Material, which will connect all your textures automatically.

4.) </br>
In the **HDRI Tab** you can import any HDRI map of your choice into the scene. First type in a name and then press **Create HDRI**. Now you can choose a .HDRI file by clicking the **Folder Icon** button. After that your DomeLight is set up and animated. Clicking the **Edit Icon** button will let you change a few DomeLight properties and you can also change the background.

5.) </br>
To create a camera for the scene, go to the **Camera** tab, type in a name and press **Create Camera**.-- The camera will be created based on your perspective view. Together with the camera comes also the reference spheres with MacBeth Charts. You can simply change the focal length in the tab and the charts will stick with it.

6.)</br>
In the **Render Tab** you can specify the render location and simply hit **Render**. You can also open up the *Render Settings* rollout to tweak a few parameters. Changing the *Frame Range* will automatically update all the Turntable animations to the desired length. You can also enable **Vertical asset rotation**, however if you transform your asset you need to press **Update Vertical Rotator** to center the pivot for the vertical animation.
Further down in the VRay Settings you can choose between different **Quality Presets** or you tweak the parameters manually. Under **Global Switches** you can define the Colorspace and if you choose **ACES** you can set up an ocio path manually if you don't have it set up in the environment variable already.
In the **AOVs** rollout you can choose which Render Elements you want to use  *(all are enabled by default)*.

# To do List

- Maya, Houdini support
- Nuke slapcomp support
- Support for different render engines
- More Material options
- Add Asset Displacement Modifier
- More exposed parameters for HDRIs and Assets

# Author

Kaan Yilmaz | kaan.yilmaz99@t-online.de