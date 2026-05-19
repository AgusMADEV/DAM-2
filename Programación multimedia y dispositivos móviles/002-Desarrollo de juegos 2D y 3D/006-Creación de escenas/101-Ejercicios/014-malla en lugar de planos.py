import bpy
import bmesh
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

# =====================================================
# FULL SCENE WIPE (objects, datablocks, orphans)
# =====================================================
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

for block in (
    bpy.data.meshes,
    bpy.data.materials,
    bpy.data.textures,
    bpy.data.images,
    bpy.data.collections,
    bpy.data.worlds,
    bpy.data.curves,
    bpy.data.cameras,
    bpy.data.lights,
):
    for datablock in list(block):
        try:
            block.remove(datablock)
        except:
            pass

for _ in range(3):
    try:
        bpy.ops.outliner.orphans_purge(do_recursive=True, do_local_ids=True, do_linked_ids=True)
    except:
        pass

bpy.context.scene.world = None

# =====================================================
# TERRAIN CONFIGURATION (FAST SINGLE MESH)
# =====================================================
GRID_X = 200          # vertices in X (increase for more detail)
GRID_Y = 200          # vertices in Y
CELL_SIZE = 1.0

NOISE_SCALE = 0.04
HEIGHT = 10.0
OCTAVES = 5
LACUNARITY = 2.0
GAIN = 0.5

CENTER_GRID = True

OBJ_NAME = "Terrain"
MESH_NAME = "TerrainMesh"
VCOL_NAME = "Col"     # vertex color attribute name

# Height bands (in world units) relative to sea level = 0
DEEP_LEVEL = -6.0     # lowest/deep water threshold
SHALLOW_LEVEL = 0.0   # sea level
MOUNTAIN_LEVEL = 5.0  # start of rocky mountain tones
SNOW_LEVEL = 8.0      # snow cap start

# Colors (RGBA)
C_DEEP    = (0.02, 0.08, 0.25, 1.0)  # dark blue (lowest)
C_WATER   = (0.20, 0.55, 0.85, 1.0)  # light blue (near sea level but below)
C_SAND    = (0.85, 0.80, 0.55, 1.0)  # sand at sea level
C_GRASS   = (0.18, 0.55, 0.25, 1.0)  # low land / mountain base
C_ROCK    = (0.45, 0.40, 0.35, 1.0)  # rocky mountain
C_SNOW    = (0.95, 0.95, 0.95, 1.0)  # snow

# =====================================================
# FBM PERLIN
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
# COLOR UTILITIES
# =====================================================
def clamp01(t):
    return 0.0 if t < 0.0 else (1.0 if t > 1.0 else t)

def lerp(a, b, t):
    t = clamp01(t)
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
        a[3] + (b[3] - a[3]) * t,
    )

def color_from_height(h):
    # Lowest -> deep water -> shallow water -> sand at 0 -> grass -> rock -> snow
    if h <= DEEP_LEVEL:
        return C_DEEP
    if h < SHALLOW_LEVEL:
        # Deep -> shallow blend (dark blue at lowest, light blue nearer sea)
        t = (h - DEEP_LEVEL) / (SHALLOW_LEVEL - DEEP_LEVEL)
        return lerp(C_DEEP, C_WATER, t)
    if h < 0.5:
        # Tight band around sea level feels sandy
        return C_SAND
    if h < MOUNTAIN_LEVEL:
        t = (h - 0.5) / (MOUNTAIN_LEVEL - 0.5)
        return lerp(C_GRASS, C_ROCK, t)
    if h < SNOW_LEVEL:
        t = (h - MOUNTAIN_LEVEL) / (SNOW_LEVEL - MOUNTAIN_LEVEL)
        return lerp(C_ROCK, C_SNOW, t)
    return C_SNOW

# =====================================================
# BUILD SINGLE GRID MESH
# =====================================================
mesh = bpy.data.meshes.new(MESH_NAME)
obj = bpy.data.objects.new(OBJ_NAME, mesh)
bpy.context.scene.collection.objects.link(obj)

bm = bmesh.new()

# Create vertices
verts = [[None for _ in range(GRID_Y)] for _ in range(GRID_X)]

ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

z_min = 1e9
z_max = -1e9

for x in range(GRID_X):
    for y in range(GRID_Y):
        wx = ox + x * CELL_SIZE
        wy = oy + y * CELL_SIZE
        wz = fbm(x, y) * HEIGHT
        v = bm.verts.new((wx, wy, wz))
        verts[x][y] = v
        if wz < z_min: z_min = wz
        if wz > z_max: z_max = wz

bm.verts.ensure_lookup_table()

# Create faces (quads)
for x in range(GRID_X - 1):
    for y in range(GRID_Y - 1):
        v1 = verts[x][y]
        v2 = verts[x + 1][y]
        v3 = verts[x + 1][y + 1]
        v4 = verts[x][y + 1]
        try:
            bm.faces.new((v1, v2, v3, v4))
        except ValueError:
            # face exists
            pass

bm.faces.ensure_lookup_table()

# Write bmesh to mesh datablock
bm.to_mesh(mesh)
bm.free()

# Shade flat

for p in mesh.polygons:
    p.use_smooth = False

# =====================================================
# VERTEX COLORS (FAST + RELIABLE)
# =====================================================
# Ensure color attribute exists (Blender 3.2+ prefers color_attributes)
try:
    color_layer = mesh.color_attributes.get(VCOL_NAME)
    if color_layer is None:
        color_layer = mesh.color_attributes.new(name=VCOL_NAME, type='BYTE_COLOR', domain='CORNER')
    active_color = color_layer
except:
    # Older Blender fallback
    vcol = mesh.vertex_colors.get(VCOL_NAME)
    if vcol is None:
        vcol = mesh.vertex_colors.new(name=VCOL_NAME)
    active_color = vcol

# Color per loop (corner) using vertex height
# (loop.vertex_index gives the vertex used by that polygon corner)
loops = mesh.loops
vtx = mesh.vertices

# Different APIs expose different data paths; handle both.
def set_loop_color(i, rgba):
    try:
        # color_attributes API: active_color.data[i].color = (r,g,b,a)
        active_color.data[i].color = rgba
    except:
        # vertex_colors API: active_color.data[i].color = (r,g,b,a)
        active_color.data[i].color = rgba

for i, loop in enumerate(loops):
    h = vtx[loop.vertex_index].co.z
    set_loop_color(i, color_from_height(h))

# =====================================================
# MATERIAL: show vertex colors
# =====================================================
mat = bpy.data.materials.new(name="TerrainMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links

for n in list(nodes):
    nodes.remove(n)

out = nodes.new(type="ShaderNodeOutputMaterial")
out.location = (300, 0)

bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
bsdf.location = (60, 0)

vcol = nodes.new(type="ShaderNodeVertexColor")
vcol.location = (-220, 0)
vcol.layer_name = VCOL_NAME

links.new(vcol.outputs["Color"], bsdf.inputs["Base Color"])
links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

obj.data.materials.append(mat)

# Nice viewport framing (optional)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)

