import bpy
import random

# ---------------------------------------------------------
# Limpieza inicial: objetos + materiales
# ---------------------------------------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Eliminar TODOS los materiales existentes del .blend
for mat in list(bpy.data.materials):
    bpy.data.materials.remove(mat, do_unlink=True)

# ---------------------------------------------------------
# Helpers: crear/obtener materiales y asignarlos
# ---------------------------------------------------------
def get_or_create_material(name):
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
    return mat

def assign_material(obj, mat):
    if obj.data is None:
        return
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

# Crear (si no existen) materiales requeridos
mat_asfalto   = get_or_create_material("asfalto")
mat_aceras    = get_or_create_material("aceras")
mat_edificios = get_or_create_material("edificios")

# ---------------------------------------------------------
# Escena: asfalto (plano) + edificios + aceras
# ---------------------------------------------------------
bpy.ops.mesh.primitive_plane_add(
    size=60,
    enter_editmode=False,
    align='WORLD',
    location=(25, 25, 0),
    scale=(25, 25, 1)
)
asfalto_obj = bpy.context.active_object
assign_material(asfalto_obj, mat_asfalto)

for x in range(0, 50, 3):
    for y in range(0, 50, 3):
        xr = random.uniform(0, 5)

        # Edificio (un solo material para todos)
        bpy.ops.mesh.primitive_cube_add(
            size=2,
            enter_editmode=False,
            align='WORLD',
            location=(x, y, xr),
            scale=(1, 1, xr)
        )
        edificio_obj = bpy.context.active_object
        assign_material(edificio_obj, mat_edificios)

        # Acera/pavimento (un solo material para todos)
        bpy.ops.mesh.primitive_cube_add(
            size=2.3,
            enter_editmode=False,
            align='WORLD',
            location=(x, y, 0),
            scale=(1, 1, 0.01)
        )
        acera_obj = bpy.context.active_object
        assign_material(acera_obj, mat_aceras)

# ---------------------------------------------------------
# Luz
# ---------------------------------------------------------
bpy.ops.object.light_add(
    type='SUN',
    radius=1,
    align='WORLD',
    location=(0, 0, 0),
    scale=(1, 1, 1)
)

bpy.ops.transform.rotate(
    value=-0.253336,
    orient_axis='Z',
    orient_type='VIEW',
    orient_matrix=(
        (0.997053, -0.0767177, 3.62284e-07),
        (0.0149007, 0.193661, 0.980956),
        (-0.0752567, -0.978064, 0.194233)
    ),
    orient_matrix_type='VIEW',
    mirror=False,
    use_proportional_edit=False,
    proportional_edit_falloff='SMOOTH',
    proportional_size=1,
    use_proportional_connected=False,
    use_proportional_projected=False,
    snap=False,
    snap_elements={'INCREMENT'},
    use_snap_project=False,
    snap_target='CLOSEST',
    use_snap_self=True,
    use_snap_edit=True,
    use_snap_nonedit=True,
    use_snap_selectable=False
)

