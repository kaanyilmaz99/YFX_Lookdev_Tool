# ADVANCED ***************************************************************************
# content = assignment
#
# date    = 2022-01-07
# email   = contact@alexanderrichtertd.com
#************************************************************************************

"""

CUBE CLASS

1. CREATE an abstract class "Cube" with the functions:
   translate(x, y, z), rotate(x, y, z), scale(x, y, z) and color(R, G, B)
   All functions store and print out the data in the cube (translate, rotate, scale and color).

2. ADD an __init__(name) and create 3 cube objects.

3. ADD the function print_status() which prints all the variables nicely formatted.

4. ADD the function update_transform(ttype, value).
   "ttype" can be "translate", "rotate" and "scale" while "value" is a list of 3 floats.
   This function should trigger either the translate, rotate or scale function.

   BONUS: Can you do it without using ifs?

5. CREATE a parent class "Object" which has a name, translate, rotate and scale.
   Use Object as the parent for your Cube class.
   Update the Cube class to not repeat the content of Object.

"""
class Object():

   def translate(self, x, y, z):
      self.current_position = [x, y, z]
      # print(self.current_position)

   def rotate(self, x, y, z):
      self.current_rotation = [x, y, z]
      # print(self.current_rotation)

   def scale(self, x, y, z):
         self.current_scale = [x, y, z]
      # print(self.current_scale)



class Cube(Object):

   def __init__(self, name, trans, rot, scale, color):
      self.object_name = name
      self.translate(trans[0], trans[1], trans[2])
      self.rotate(rot[0], rot[1], rot[2])
      self.scale(scale[0], scale[1], scale[2])
      self.color(color[0], color[1], color[2])
      self.print_status()
      
   def color(self, r, g, b):
      self.current_color = [r, g, b]
      # print(self.current_color)

   def update_transform(self, ttype, value):
      if ttype == 'translate':
         self.translate(value[0], value[1], value[2])

      elif ttype == 'rotate':
         self.rotate(value[0], value[1], value[2])

      elif ttype == 'scale':
         self.scale(value[0], value[1], value[2])

   def print_status(self):
      print(f' {self.object_name} has been created. It has the following parameters... \
            \n Position: {self.current_position} \n Rotation: {self.current_rotation} \
            \n Scale: {self.current_scale} \n Color: {self.current_color} \n')


redCube = Cube("Red_Cube", [10, 4, 0], [90, 10, 0], [1, 1, 1], [255, 0, 0])
redCube.update_transform('rotate', [0, 0, 0])
redCube.print_status()
greenCube = Cube("Green_Cube", [-20, 0, 0], [87, 180, 2], [3, 3, 3], [0, 255, 0])
blueCube = Cube("Blue_Cube", [50, 10, 0], [7, 0, 90], [1.5, 1.5, 1.5], [0, 0, 255])