import bpy
import random
# Antes de empezar lo elimino todo
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

bpy.ops.mesh.primitive_plane_add(
  size=60, 
  enter_editmode=False, 
  align='WORLD', 
  location=(25, 25, 0), 
  scale=(25, 25, 1)
)

for x in range(0,50,3):
    for y in range(0,50,3):
        xr = random.uniform(0,5)
        bpy.ops.mesh.primitive_cube_add(
            size=2, 
            enter_editmode=False, 
            align='WORLD', 
            location=(x, y, xr), 
            scale=(1, 1, xr)
        )
        bpy.ops.mesh.primitive_cube_add(
            size=2.3, 
            enter_editmode=False, 
            align='WORLD', 
            location=(x, y, 0), 
            scale=(1, 1, 0.01)
        )
