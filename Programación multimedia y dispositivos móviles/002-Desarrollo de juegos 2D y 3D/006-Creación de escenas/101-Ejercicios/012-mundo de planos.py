import bpy
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

# =====================================================
# FULL SCENE WIPE (objects, data-blocks, everything)
# =====================================================

# Delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove orphan data-blocks
for block in (
    bpy.data.meshes,
    bpy.data.materials,
    bpy.data.textures,
    bpy.data.images,
    bpy.data.collections,
    bpy.data.worlds,
):
    for datablock in block:
        block.remove(datablock)

# Purge orphan data recursively (Blender 3.x+)
for _ in range(3):
    bpy.ops.outliner.orphans_purge(
        do_recursive=True,
        do_local_ids=True,
        do_linked_ids=True
    )

# Ensure clean world
bpy.context.scene.world = None


# =====================================================
# TERRAIN CONFIGURATION
# =====================================================
GRID_X = 120
GRID_Y = 120
CELL_SIZE = 1.0
PLANE_SIZE = 1.05

NOISE_SCALE = 0.06
HEIGHT = 8.0
OCTAVES = 5
LACUNARITY = 2.0
GAIN = 0.5

CENTER_GRID = True
COLLECTION_NAME = "Terrain"


# =====================================================
# FBM PERLIN FUNCTION
# =====================================================
def fbm(x, y):
    amp = 1.0
    freq = 1.0
    total = 0.0
    norm = 0.0

    for _ in range(OCTAVES):
        n = perlin_noise(Vector((x * NOISE_SCALE * freq,
                                 y * NOISE_SCALE * freq,
                                 0.0)))
        total += n * amp
        norm += amp
        amp *= GAIN
        freq *= LACUNARITY

    return total / norm if norm else 0.0


# =====================================================
# CREATE TERRAIN GRID
# =====================================================
collection = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(collection)

ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

for x in range(GRID_X):
    for y in range(GRID_Y):
        wx = ox + x * CELL_SIZE
        wy = oy + y * CELL_SIZE
        wz = fbm(x, y) * HEIGHT

        bpy.ops.mesh.primitive_plane_add(
            size=PLANE_SIZE,
            location=(wx, wy, wz)
        )

        obj = bpy.context.active_object
        obj.name = f"cell_{x}_{y}"

        # Move to terrain collection
        bpy.context.scene.collection.objects.unlink(obj)
        collection.objects.link(obj)

# Flat shading (consistent look)
for obj in collection.objects:
    obj.select_set(True)

bpy.ops.object.shade_flat()
bpy.ops.object.select_all(action='DESELECT')

