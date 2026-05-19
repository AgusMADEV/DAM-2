import bpy
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

# =====================================================
# FULL SCENE WIPE (objects, data-blocks, everything)
# =====================================================

# Delete all objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Remove datablocks (safe removes)
def safe_remove(collection):
    for datablock in list(collection):
        try:
            collection.remove(datablock)
        except:
            pass

safe_remove(bpy.data.meshes)
safe_remove(bpy.data.materials)
safe_remove(bpy.data.textures)
safe_remove(bpy.data.images)
# NOTE: removing collections/worlds can be risky if scene still references them,
# but you asked "everything", so we do it cautiously.
for col in list(bpy.data.collections):
    try:
        bpy.data.collections.remove(col)
    except:
        pass
for w in list(bpy.data.worlds):
    try:
        bpy.data.worlds.remove(w)
    except:
        pass

# Purge orphans (Blender 3.x+)
for _ in range(3):
    try:
        bpy.ops.outliner.orphans_purge(do_recursive=True, do_local_ids=True, do_linked_ids=True)
    except:
        break

# Ensure clean world
try:
    bpy.context.scene.world = None
except:
    pass

# =====================================================
# TERRAIN CONFIGURATION
# =====================================================
GRID_X = 20
GRID_Y = 20
CELL_SIZE = 1.0
PLANE_SIZE = 1.05

NOISE_SCALE = 0.06
HEIGHT = 8.0
OCTAVES = 5
LACUNARITY = 2.0
GAIN = 0.5

CENTER_GRID = True
COLLECTION_NAME = "Terrain"

SEA_LEVEL = 0.0  # "sea level" reference

# Gradient colors (RGBA)
COL_WATER_DARK  = (0.02, 0.06, 0.25, 1.0)  # lowest point (dark blue)
COL_WATER_LIGHT = (0.25, 0.65, 0.95, 1.0)  # higher water (light blue)
COL_SAND        = (0.88, 0.82, 0.62, 1.0)  # around sea level
COL_MOUNTAIN    = (0.30, 0.36, 0.22, 1.0)  # mid/high (mountain)
COL_SNOW        = (0.96, 0.96, 0.98, 1.0)  # highest point (snow)

# =====================================================
# FBM PERLIN FUNCTION
# =====================================================
def fbm(x, y):
    amp = 1.0
    freq = 1.0
    total = 0.0
    norm = 0.0

    for _ in range(OCTAVES):
        n = perlin_noise(Vector((
            x * NOISE_SCALE * freq,
            y * NOISE_SCALE * freq,
            0.0
        )))
        total += n * amp
        norm += amp
        amp *= GAIN
        freq *= LACUNARITY

    return total / norm if norm else 0.0

# =====================================================
# UTIL: LERP COLOR
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

# =====================================================
# CREATE ONE MATERIAL THAT USES "OBJECT COLOR"
# =====================================================
def make_objectcolor_material(name="Terrain_ObjectColor"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    # Clear default nodes
    for n in list(nodes):
        nodes.remove(n)

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (150, 0)

    objinfo = nodes.new("ShaderNodeObjectInfo")
    objinfo.location = (-150, 0)

    links.new(objinfo.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    return mat

# =====================================================
# CREATE TERRAIN GRID (and track min/max height)
# =====================================================
collection = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(collection)

ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

# First pass: compute heights (so we can normalize and color nicely)
heights = []
for x in range(GRID_X):
    for y in range(GRID_Y):
        wz = fbm(x, y) * HEIGHT
        heights.append(wz)

min_z = min(heights) if heights else 0.0
max_z = max(heights) if heights else 1.0
if abs(max_z - min_z) < 1e-9:
    max_z = min_z + 1.0

# Define gradient thresholds based on your sea level
# Water range: [min_z .. SEA_LEVEL]
# Land range:  [SEA_LEVEL .. max_z]
water_depth = max(SEA_LEVEL - min_z, 1e-9)
land_height = max(max_z - SEA_LEVEL, 1e-9)

# Water: min -> dark, up towards sea -> light
# Land: sea -> sand, then mountain, then snow at top
# We place "sand band" close to sea level, and snow band close to top.
SAND_BAND = 0.12  # portion of land range (near sea)
SNOW_START = 0.78 # start snow at 78% of land height

def color_for_height(z):
    if z <= SEA_LEVEL:
        # 0 at min, 1 at sea
        t = (z - min_z) / water_depth
        return lerp(COL_WATER_DARK, COL_WATER_LIGHT, t)
    else:
        # 0 at sea, 1 at top
        t = (z - SEA_LEVEL) / land_height

        # sand near sea
        if t < SAND_BAND:
            # blend water-light -> sand across the shoreline
            tt = t / SAND_BAND
            return lerp(COL_WATER_LIGHT, COL_SAND, tt)

        # mountain zone until snow
        if t < SNOW_START:
            # blend sand -> mountain
            tt = (t - SAND_BAND) / (SNOW_START - SAND_BAND)
            return lerp(COL_SAND, COL_MOUNTAIN, tt)

        # snow zone
        tt = (t - SNOW_START) / (1.0 - SNOW_START)
        return lerp(COL_MOUNTAIN, COL_SNOW, tt)

# Create material once
terrain_mat = make_objectcolor_material()

# Second pass: build objects and color them
idx = 0
created = []

for x in range(GRID_X):
    for y in range(GRID_Y):
        wx = ox + x * CELL_SIZE
        wy = oy + y * CELL_SIZE
        wz = heights[idx]
        idx += 1

        bpy.ops.mesh.primitive_plane_add(
            size=PLANE_SIZE,
            location=(wx, wy, wz)
        )
        obj = bpy.context.active_object
        obj.name = f"cell_{x}_{y}"

        # Robust move: unlink from ALL current collections, then link to our target
        for col in list(obj.users_collection):
            try:
                col.objects.unlink(obj)
            except:
                pass
        if obj.name not in collection.objects:
            collection.objects.link(obj)

        # Assign shared material (once)
        if obj.data.materials:
            obj.data.materials[0] = terrain_mat
        else:
            obj.data.materials.append(terrain_mat)

        # Set per-object color (Object Info node reads this)
        obj.color = color_for_height(wz)

        created.append(obj)

# Flat shading (consistent look) without relying on selection state too much
for obj in created:
    obj.select_set(True)
bpy.context.view_layer.objects.active = created[0] if created else None
try:
    bpy.ops.object.shade_flat()
except:
    pass
bpy.ops.object.select_all(action='DESELECT')

print(f"Terrain done. min_z={min_z:.3f} max_z={max_z:.3f} sea={SEA_LEVEL:.3f}")

