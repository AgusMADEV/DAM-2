import bpy
import random

# ---------------------------------------------------------
# Limpieza inicial: objetos + materiales
# ---------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat, do_unlink=True)

# ---------------------------------------------------------
# Helpers: materiales
# ---------------------------------------------------------
def get_or_create_material(name, color, roughness=0.8):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True

        nodes = mat.node_tree.nodes
        bsdf = nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = roughness

    return mat

def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# ---------------------------------------------------------
# Materiales (colores pedidos)
# ---------------------------------------------------------
mat_asfalto = get_or_create_material(
    "asfalto",
    color=(0.05, 0.05, 0.05, 1),   # gris muy oscuro
    roughness=0.95
)

mat_aceras = get_or_create_material(
    "aceras",
    color=(0.4, 0.4, 0.4, 1),      # gris medio
    roughness=0.9
)

mat_edificios = get_or_create_material(
    "edificios",
    color=(0.75, 0.75, 0.75, 1),   # gris claro
    roughness=0.7
)

# ---------------------------------------------------------
# Asfalto (plano base)
# ---------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(
    size=60,
    align='WORLD',
    location=(25, 25, 0),
    scale=(25, 25, 1)
)
assign_material(bpy.context.active_object, mat_asfalto)

# ---------------------------------------------------------
# Edificios + aceras
# ---------------------------------------------------------
for x in range(0, 50, 3):
    for y in range(0, 50, 3):
        h = random.uniform(0.5, 5)

        # Edificio
        bpy.ops.mesh.primitive_cube_add(
            size=2,
            align='WORLD',
            location=(x, y, h),
            scale=(1, 1, h)
        )
        assign_material(bpy.context.active_object, mat_edificios)

        # Acera
        bpy.ops.mesh.primitive_cube_add(
            size=2.3,
            align='WORLD',
            location=(x, y, 0),
            scale=(1, 1, 0.01)
        )
        assign_material(bpy.context.active_object, mat_aceras)

# ---------------------------------------------------------
# Luz
# ---------------------------------------------------------
bpy.ops.object.light_add(
    type='SUN',
    align='WORLD',
    location=(0, 0, 0)
)

bpy.ops.transform.rotate(
    value=-0.253336,
    orient_axis='Z',
    orient_type='VIEW',
    orient_matrix=(
        (0.997053, -0.0767177, 0.0),
        (0.0149007, 0.193661, 0.980956),
        (-0.0752567, -0.978064, 0.194233)
    ),
    orient_matrix_type='VIEW'
)

