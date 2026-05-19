import bpy
import bmesh
import math
from mathutils import Vector, Euler

# =====================================================
# FULL SCENE WIPE (objects + datablocks)
# =====================================================
def full_wipe_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    for col in list(bpy.data.collections):
        try:
            bpy.data.collections.remove(col)
        except:
            pass

    for block in (
        bpy.data.meshes,
        bpy.data.materials,
        bpy.data.textures,
        bpy.data.images,
        bpy.data.lights,
        bpy.data.cameras,
        bpy.data.curves,
        bpy.data.worlds,
    ):
        for datablock in list(block):
            try:
                block.remove(datablock)
            except:
                pass

    for _ in range(5):
        try:
            bpy.ops.outliner.orphans_purge(do_recursive=True, do_local_ids=True, do_linked_ids=True)
        except:
            try:
                bpy.ops.outliner.orphans_purge(do_recursive=True)
            except:
                break


# =====================================================
# CONFIG
# =====================================================
GRID_X = 200
GRID_Y = 200
CELL_SIZE = 1.0

CENTER_GRID = True

TERRAIN_NAME = "Terrain"
TERRAIN_COLLECTION = "Terrain"

SEA_LEVEL = 0.0
WATER_MARGIN = 25.0

# Terrain displacement "look"
HEIGHT = 2.0           # Displace strength
NOISE_SCALE = 0.035    # Equivalent-ish scale (we invert into musgrave scale below)
OCTAVES = 6
LACUNARITY = 2.0
GAIN = 0.5

SUBSURF_LEVEL = 1

# Fly-through speed (units per frame)
FLY_SPEED = 0.40  # sube/baja según necesidad

# Camera (como tu ejemplo)
CAM_LOC = (100.0, 0.0, 1.5)
CAM_ROT_DEG = (90.0, 0.0, 90.0)  # XYZ Euler degrees

# Color bands (RGBA)
COLOR_DEEP_WATER  = (0.02, 0.08, 0.25, 1.0)
COLOR_SHALLOW     = (0.08, 0.25, 0.55, 1.0)
COLOR_SAND        = (0.78, 0.72, 0.52, 1.0)
COLOR_MOUNTAIN    = (0.22, 0.28, 0.20, 1.0)
COLOR_SNOW        = (0.95, 0.95, 0.95, 1.0)


# =====================================================
# WORLD
# =====================================================
def setup_world_sky(strength=0.1):
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True

    nt = world.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputWorld")
    out.location = (400, 0)

    bg = nodes.new("ShaderNodeBackground")
    bg.location = (150, 0)
    bg.inputs["Strength"].default_value = strength

    sky = nodes.new("ShaderNodeTexSky")
    sky.location = (-150, 0)

    for candidate in ("MULTIPLE_SCATTERING", "PREETHAM", "HOSEK_WILKIE", "SINGLE_SCATTERING"):
        try:
            sky.sky_type = candidate
            break
        except:
            continue

    links.new(sky.outputs["Color"], bg.inputs["Color"])
    links.new(bg.outputs["Background"], out.inputs["Surface"])


# =====================================================
# MATERIALS (procedural bands, no vertex colors)
# =====================================================
def make_terrain_material(noise_empty=None, name="MAT_Terrain_Procedural"):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (650, 0)
    bsdf.inputs["Roughness"].default_value = 0.85
    # Blender 4.x naming differences:
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.15
    elif "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = 0.15

    # Coordinates (Object coords from an Empty) so we can "move the world"
    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, 0)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, 0)

    # Use Object coords driven by the Empty. If none, fallback to Object.
    if noise_empty is not None:
        texcoord.object = noise_empty

    # Noise used for micro bump (like water-ish) + to drive bands (approx height)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-450, 0)
    noise.inputs["Scale"].default_value = 10.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.55

    # Height proxy for bands
    maprange = nodes.new("ShaderNodeMapRange")
    maprange.location = (-200, 160)
    maprange.inputs["From Min"].default_value = 0.0
    maprange.inputs["From Max"].default_value = 1.0
    maprange.inputs["To Min"].default_value = -HEIGHT * 0.6
    maprange.inputs["To Max"].default_value = HEIGHT * 0.6

    # Convert height to 0..1 around SEA_LEVEL for color bands
    maprange2 = nodes.new("ShaderNodeMapRange")
    maprange2.location = (30, 160)
    maprange2.inputs["From Min"].default_value = -HEIGHT * 0.6
    maprange2.inputs["From Max"].default_value = HEIGHT * 0.6
    maprange2.inputs["To Min"].default_value = 0.0
    maprange2.inputs["To Max"].default_value = 1.0

    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (260, 160)

    # Set up band stops (you can tune)
    # 0.00 deep water -> 0.35 shallow -> 0.50 sand (sea) -> 0.78 mountain -> 1.00 snow
    ramp.color_ramp.elements[0].position = 0.00
    ramp.color_ramp.elements[0].color = COLOR_DEEP_WATER

    e1 = ramp.color_ramp.elements.new(0.35)
    e1.color = COLOR_SHALLOW
    e2 = ramp.color_ramp.elements.new(0.50)
    e2.color = COLOR_SAND
    e3 = ramp.color_ramp.elements.new(0.78)
    e3.color = COLOR_MOUNTAIN
    ramp.color_ramp.elements[1].position = 1.00
    ramp.color_ramp.elements[1].color = COLOR_SNOW

    # Bump for detail
    bump = nodes.new("ShaderNodeBump")
    bump.location = (350, -200)
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.2

    # Links
    links.new(texcoord.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], maprange.inputs["Value"])
    links.new(maprange.outputs["Result"], maprange2.inputs["Value"])
    links.new(maprange2.outputs["Result"], ramp.inputs["Fac"])

    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def make_water_material():
    mat = bpy.data.materials.new("MAT_Water")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (500, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (200, 0)

    # Base settings
    if "Base Color" in bsdf.inputs:
        bsdf.inputs["Base Color"].default_value = (0.03, 0.12, 0.20, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.02
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.333
    if "Transmission Weight" in bsdf.inputs:
        bsdf.inputs["Transmission Weight"].default_value = 1.0
    elif "Transmission" in bsdf.inputs:
        bsdf.inputs["Transmission"].default_value = 1.0

    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = 0.5
    elif "Specular" in bsdf.inputs:
        bsdf.inputs["Specular"].default_value = 0.5

    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, 0)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, 0)
    mapping.inputs["Scale"].default_value = (2.0, 2.0, 2.0)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-500, 0)
    noise.inputs["Scale"].default_value = 8.0
    noise.inputs["Detail"].default_value = 6.0
    noise.inputs["Roughness"].default_value = 0.5

    bump = nodes.new("ShaderNodeBump")
    bump.location = (-150, -200)
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.1

    links.new(texcoord.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    try:
        mat.use_screen_refraction = True
    except:
        pass
    try:
        mat.blend_method = 'BLEND'
    except:
        pass

    return mat


# =====================================================
# TERRAIN (fast static grid + modifiers)
# =====================================================
def create_terrain_grid():
    col = bpy.data.collections.new(TERRAIN_COLLECTION)
    bpy.context.scene.collection.children.link(col)

    mesh = bpy.data.meshes.new(TERRAIN_NAME)
    obj = bpy.data.objects.new(TERRAIN_NAME, mesh)
    col.objects.link(obj)

    bm = bmesh.new()

    ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
    oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

    verts = [[None] * GRID_Y for _ in range(GRID_X)]
    for x in range(GRID_X):
        for y in range(GRID_Y):
            wx = ox + x * CELL_SIZE
            wy = oy + y * CELL_SIZE
            verts[x][y] = bm.verts.new((wx, wy, 0.0))

    bm.verts.ensure_lookup_table()

    for x in range(GRID_X - 1):
        for y in range(GRID_Y - 1):
            v1 = verts[x][y]
            v2 = verts[x + 1][y]
            v3 = verts[x + 1][y + 1]
            v4 = verts[x][y + 1]
            try:
                bm.faces.new((v1, v2, v3, v4))
            except:
                pass

    bm.to_mesh(mesh)
    bm.free()

    for p in mesh.polygons:
        p.use_smooth = True

    # Modifiers: Subsurf (do NOT apply) + Displace
    subs = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subs.levels = SUBSURF_LEVEL
    subs.render_levels = SUBSURF_LEVEL
    subs.subdivision_type = 'CATMULL_CLARK'

    return obj, (ox, oy)


def create_noise_empty(name="NoiseSpace"):
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 2.0
    bpy.context.scene.collection.objects.link(empty)
    return empty


def add_displace_modifier(obj, noise_empty):
    # Legacy procedural texture (fast for Displace)
    tex = bpy.data.textures.new("TEX_TerrainMusgrave", type='MUSGRAVE')
    tex.musgrave_type = 'FBM'
    # Roughly map NOISE_SCALE to musgrave scale:
    # smaller NOISE_SCALE => larger features => lower musgrave.noise_scale
    tex.noise_scale = max(0.0001, NOISE_SCALE * 40.0)
    tex.octaves = OCTAVES
    tex.lacunarity = LACUNARITY
    tex.gain = GAIN

    disp = obj.modifiers.new(name="Displace", type='DISPLACE')
    disp.texture = tex
    disp.strength = HEIGHT
    disp.mid_level = 0.5  # musgrave outputs ~0..1, center at 0.5
    disp.texture_coords = 'OBJECT'
    disp.texture_coords_object = noise_empty
    return disp


# =====================================================
# WATER
# =====================================================
def create_water_plane(terrain_bounds, water_z=SEA_LEVEL, margin=WATER_MARGIN):
    (ox, oy) = terrain_bounds
    width = (GRID_X - 1) * CELL_SIZE + margin * 2.0
    depth = (GRID_Y - 1) * CELL_SIZE + margin * 2.0
    cx = ox + (GRID_X - 1) * CELL_SIZE * 0.5
    cy = oy + (GRID_Y - 1) * CELL_SIZE * 0.5

    mesh = bpy.data.meshes.new("Water")
    obj = bpy.data.objects.new("Water", mesh)
    bpy.context.scene.collection.objects.link(obj)

    bm = bmesh.new()
    v1 = bm.verts.new((cx - width * 0.5,  cy - depth * 0.5,  water_z))
    v2 = bm.verts.new((cx + width * 0.5,  cy - depth * 0.5,  water_z))
    v3 = bm.verts.new((cx + width * 0.5,  cy + depth * 0.5,  water_z))
    v4 = bm.verts.new((cx - width * 0.5,  cy + depth * 0.5,  water_z))
    bm.faces.new((v1, v2, v3, v4))
    bm.to_mesh(mesh)
    bm.free()

    for p in mesh.polygons:
        p.use_smooth = True

    obj.data.materials.append(make_water_material())

    try:
        ee = bpy.context.scene.eevee
        if hasattr(ee, "use_ssr"):
            ee.use_ssr = True
        if hasattr(ee, "use_ssr_refraction"):
            ee.use_ssr_refraction = True
        if hasattr(ee, "ssr_thickness"):
            ee.ssr_thickness = 2.0
    except:
        pass

    return obj


# =====================================================
# CAMERA
# =====================================================
def create_camera(loc=(0, 0, 0), rot_deg=(0, 0, 0), name="Camera"):
    cam_data = bpy.data.cameras.new(name)
    cam_obj = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)

    cam_obj.location = Vector(loc)
    cam_obj.rotation_mode = 'XYZ'
    cam_obj.rotation_euler = Euler(
        (math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2])),
        'XYZ'
    )

    bpy.context.scene.camera = cam_obj
    return cam_obj


# =====================================================
# FLY-THROUGH HANDLER (move noise space each frame)
# =====================================================
_HANDLER_KEY = "JV_FLY_HANDLER"

def remove_existing_handler():
    handlers = bpy.app.handlers.frame_change_pre
    to_remove = []
    for h in handlers:
        if getattr(h, "__name__", "") == _HANDLER_KEY:
            to_remove.append(h)
    for h in to_remove:
        try:
            handlers.remove(h)
        except:
            pass

def make_fly_handler(cam_obj, noise_empty, speed=FLY_SPEED):
    def _handler(scene):
        # Camera forward in world space: local -Z
        fwd = cam_obj.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -1.0))
        # Keep motion on XY plane (terrain plane)
        fwd_xy = Vector((fwd.x, fwd.y, 0.0))
        if fwd_xy.length < 1e-6:
            return
        fwd_xy.normalize()

        # Move noise space opposite to camera forward or towards camera?
        # If you want "terrain comes towards camera", move noise space towards camera (i.e., +fwd_xy).
        # If you want "camera moving forward", you'd usually move noise space backward (-fwd_xy).
        noise_empty.location += fwd_xy * speed

    _handler.__name__ = _HANDLER_KEY
    return _handler


# =====================================================
# RUN
# =====================================================
full_wipe_scene()

# Terrain base (static)
terrain_obj, (ox, oy) = create_terrain_grid()

# Noise space empty (we move this per frame)
noise_empty = create_noise_empty("NoiseSpace")
noise_empty.location = (0.0, 0.0, 0.0)

# Displace modifier (fast, evaluated by Blender)
add_displace_modifier(terrain_obj, noise_empty)

# Terrain material (procedural bands)
terrain_mat = make_terrain_material(noise_empty=noise_empty)
terrain_obj.data.materials.append(terrain_mat)

# World + water
setup_world_sky(strength=0.1)
water_obj = create_water_plane((ox, oy), water_z=SEA_LEVEL, margin=WATER_MARGIN)

# Camera
cam_obj = create_camera(loc=CAM_LOC, rot_deg=CAM_ROT_DEG, name="Camera")

# Install handler (remove previous, add new)
remove_existing_handler()
bpy.app.handlers.frame_change_pre.append(make_fly_handler(cam_obj, noise_empty, speed=FLY_SPEED))

print("Done. Fly-through enabled: NoiseSpace moves each frame.")

