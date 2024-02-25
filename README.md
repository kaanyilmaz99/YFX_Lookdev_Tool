# ky_pythonadvanced

A wip version of my turntable tool for 3dsmax. 

### How to use the tool
1. After downloading, launch the **3dsmax.bat** file which can be found inside the 01_app folder.
2. In the menu bar go to **KY-Tools** and select Turntable.
 <img width="334" alt="Launch_KYTools" src="https://github.com/kaanyilmaz99/ky_pythonadvanced/assets/52401788/f484f319-0e93-44d0-9a7e-55dd68e9c6bf">




3. Now the Turntable - Tool UI should appear. To create a Turntable, click on the folder Icon and select a 3d model of your choice. After that
   click the **Create Turntable** button and it will import your asset and build the setup. You also have the option to save your work or open
   any other file from the Home tab.
 <img width="359" alt="choose_asset" src="https://github.com/kaanyilmaz99/ky_pythonadvanced/assets/52401788/e118100c-90bd-46a1-9be7-fc3af37dafc2">




4. Now your turntable is set up except the missing environment light. To create one you need to go to the **Layers Tab**.
5. Type in any name for your first layer and press **Add Layer**
6. Now you can choose an HDRI map by pressing the folder icon. After confirming a dome light with your HDRI will be created.
   You can create as many layers as you want with different HDRI maps to test your textures/materials in different lighting scenarios.
7. Keep in mind that only one layer can be active at a time.
8. In the future you will be able to rename or edit a few more layer options [not functional at this point]
 <img width="343" alt="layers" src="https://github.com/kaanyilmaz99/ky_pythonadvanced/assets/52401788/8441e68c-f33f-4287-99b2-771ba931c29b">


 ### How it works

 There are 3 modules which are important (the 'create_menu.py' module can be ignored for now).
 
 The first one is the 'create_main_ui' which is basically the starting script. It creates a dockable window, assigns the main ui to it and
 then connects all the buttons.

 The second one is an additional UI creation module, but just for the Layers Tab. It is called once you press the 'Add Layer' button in the create_main_ui.py
 module. The created widget will be assigned to the main_ui.

 The third one is the actual turntable creation module, called create_turntable.py. It is called after you press the 'Create Turntable' button in the main ui and is responsible
 for creating/removing the objects, lights, cameras or in general modifying the 3dsmax scene.
