import bpy
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

# =====================================================
# FULL SCENE WIPE (objects + data-blocks)
# =====================================================
def full_wipe():
    # Ensure we're not in Edit Mode
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

    # Delete all objects
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

    # Remove collections (except the master Scene Collection)
    for col in list(bpy.data.collections):
        if col.users == 0:
            bpy.data.collections.remove(col)

    # Remove common datablocks
    for block in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.textures,
        bpy.data.images,
        bpy.data.node_groups,
        bpy.data.worlds,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.curves,
        bpy.data.metaballs,
        bpy.data.armatures,
        bpy.data.actions,
        bpy.data.particles,
    ):
        for datablock in list(block):
            try:
                block.remove(datablock)
            except Exception:
                pass

    # Orphans purge (Blender 3.x/4.x)
    for _ in range(3):
        try:
            bpy.ops.outliner.orphans_purge(do_recursive=True)
        except Exception:
            break

full_wipe()

# =====================================================
# TERRAIN CONFIG
# =====================================================
GRID_X = 200          # quads in X
GRID_Y = 200          # quads in Y
CELL_SIZE = 0.5       # spacing
CENTER_GRID = True

NOISE_SCALE = 0.06
HEIGHT = 8.0
OCTAVES = 5
LACUNARITY = 2.0
GAIN = 0.5

COLLECTION_NAME = "Terrain"
OBJECT_NAME = "terrain_mesh"

# Height thresholds for coloring (relative to positive range)
SAND_BAND_POS = 0.06      # from 0 to 6% of positive max => sand->green
MOUNTAIN_START = 0.55     # start brown/rock around 55% of positive max
SNOW_START = 0.88         # start snow around 88% of positive max

# Colors (RGBA)
COL_LOWEST_DARK_BLUE = (0.02, 0.08, 0.22, 1.0)  # lowest point (dark blue)
COL_NEG_LIGHT_BLUE   = (0.20, 0.55, 0.90, 1.0)  # near sea level (negative)
COL_SAND             = (0.86, 0.80, 0.55, 1.0)  # sea level (0)
COL_LOWLAND_GREEN    = (0.20, 0.55, 0.22, 1.0)  # low positive
COL_MOUNTAIN_BROWN   = (0.42, 0.28, 0.18, 1.0)  # mid/high
COL_ROCK_GREY        = (0.55, 0.55, 0.55, 1.0)  # near top
COL_SNOW             = (0.95, 0.95, 0.97, 1.0)  # highest

def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return (
        a[0] + (b[0] - a[0]) * t,
        a[1] + (b[1] - a[1]) * t,
        a[2] + (b[2] - a[2]) * t,
        a[3] + (b[3] - a[3]) * t,
    )

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
# BUILD SINGLE MESH GRID (FAST)
# =====================================================
# Create collection
terrain_col = bpy.data.collections.new(COLLECTION_NAME)
bpy.context.scene.collection.children.link(terrain_col)

# Mesh + object
mesh = bpy.data.meshes.new("TerrainMesh")
obj = bpy.data.objects.new(OBJECT_NAME, mesh)
terrain_col.objects.link(obj)

# Compute grid origin (centered or not)
ox = -(GRID_X * CELL_SIZE) * 0.5 if CENTER_GRID else 0.0
oy = -(GRID_Y * CELL_SIZE) * 0.5 if CENTER_GRID else 0.0

# Create vertices
verts = []
for y in range(GRID_Y + 1):
    wy = oy + y * CELL_SIZE
    for x in range(GRID_X + 1):
        wx = ox + x * CELL_SIZE
        z = fbm(wx, wy) * HEIGHT
        verts.append((wx, wy, z))

# Create faces (quads)
faces = []
row = GRID_X + 1
for y in range(GRID_Y):
    for x in range(GRID_X):
        v0 = y * row + x
        v1 = v0 + 1
        v2 = v0 + row + 1
        v3 = v0 + row
        faces.append((v0, v1, v2, v3))

mesh.from_pydata(verts, [], faces)
mesh.update(calc_edges=True)

# Flat shading
for p in mesh.polygons:
    p.use_smooth = False

# =====================================================
# VERTEX COLORS (height-based gradient)
# =====================================================
zs = [v[2] for v in verts]
zmin = min(zs)
zmax = max(zs)

pos_max = max(zmax, 0.000001)  # avoid zero divide
neg_min = min(zmin, -0.000001)

def color_from_height(z):
    # Water: z < 0  (lowest = dark blue; nearer to 0 = light blue)
    if z < 0.0:
        t = (z - zmin) / (0.0 - zmin) if zmin < 0.0 else 1.0  # zmin->0 maps 0->1
        return lerp(COL_LOWEST_DARK_BLUE, COL_NEG_LIGHT_BLUE, t)

    # Land: z >= 0
    tpos = z / pos_max  # 0..1

    # 0..SAND_BAND_POS : sand -> green
    if tpos <= SAND_BAND_POS:
        t = tpos / max(SAND_BAND_POS, 1e-6)
        return lerp(COL_SAND, COL_LOWLAND_GREEN, t)

    # SAND_BAND_POS..MOUNTAIN_START : green -> brown
    if tpos <= MOUNTAIN_START:
        t = (tpos - SAND_BAND_POS) / max(MOUNTAIN_START - SAND_BAND_POS, 1e-6)
        return lerp(COL_LOWLAND_GREEN, COL_MOUNTAIN_BROWN, t)

    # MOUNTAIN_START..SNOW_START : brown -> rock grey
    if tpos <= SNOW_START:
        t = (tpos - MOUNTAIN_START) / max(SNOW_START - MOUNTAIN_START, 1e-6)
        return lerp(COL_MOUNTAIN_BROWN, COL_ROCK_GREY, t)

    # SNOW_START..1 : rock -> snow
    t = (tpos - SNOW_START) / max(1.0 - SNOW_START, 1e-6)
    return lerp(COL_ROCK_GREY, COL_SNOW, t)

# Create a color attribute compatible with Blender 3/4, fallback to vertex_colors
use_color_attributes = hasattr(mesh, "color_attributes")

if use_color_attributes:
    # POINT domain: one color per vertex
    col = mesh.color_attributes.new(name="Col", type='FLOAT_COLOR', domain='POINT')
    for i, v in enumerate(verts):
        col.data[i].color = color_from_height(v[2])
else:
    # Legacy: loop domain (per face corner)
    vcol = mesh.vertex_colors.new(name="Col")
    # Each polygon has loops; assign using vertex index
    for poly in mesh.polygons:
        for li in range(poly.loop_start, poly.loop_start + poly.loop_total):
            vi = mesh.loops[li].vertex_index
            vcol.data[li].color = color_from_height(verts[vi][2])

# =====================================================
# MATERIAL: use vertex color as base color
# =====================================================
mat = bpy.data.materials.new(name="TerrainMaterial")
mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links

# Clear default nodes
for n in list(nodes):
    nodes.remove(n)

out = nodes.new("ShaderNodeOutputMaterial")
bsdf = nodes.new("ShaderNodeBsdfPrincipled")
out.location = (400, 0)
bsdf.location = (120, 0)

# Vertex color node (Blender version differences)
try:
    vcol_node = nodes.new("ShaderNodeVertexColor")
    vcol_node.layer_name = "Col"
except Exception:
    # Fallback: Attribute node
    vcol_node = nodes.new("ShaderNodeAttribute")
    vcol_node.attribute_name = "Col"

vcol_node.location = (-140, 0)

links.new(vcol_node.outputs.get("Color"), bsdf.inputs.get("Base Color"))
links.new(bsdf.outputs.get("BSDF"), out.inputs.get("Surface"))

# Assign material
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)

# =====================================================
# WORLD: Sky Texture, strength 0.5
# =====================================================
world = bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
wnt = world.node_tree
wnodes = wnt.nodes
wlinks = wnt.links

# Clear existing world nodes
for n in list(wnodes):
    wnodes.remove(n)

w_out = wnodes.new("ShaderNodeOutputWorld")
w_bg  = wnodes.new("ShaderNodeBackground")
w_sky = wnodes.new("ShaderNodeTexSky")

w_sky.location = (-400, 0)
w_bg.location  = (-120, 0)
w_out.location = (180, 0)

w_bg.inputs["Strength"].default_value = 0.5

wlinks.new(w_sky.outputs["Color"], w_bg.inputs["Color"])
wlinks.new(w_bg.outputs["Background"], w_out.inputs["Surface"])

# =====================================================
# OPTIONAL: frame view on the new terrain
# =====================================================
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
try:
    bpy.ops.view3d.view_all(center=True)
except Exception:
    pass

