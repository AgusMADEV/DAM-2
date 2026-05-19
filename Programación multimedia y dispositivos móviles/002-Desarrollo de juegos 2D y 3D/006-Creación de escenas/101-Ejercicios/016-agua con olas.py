import bpy
import bmesh
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

# =====================================================
# FULL SCENE WIPE (objects + datablocks)
# =====================================================
def full_wipe_scene():
    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # Remove collections (except master Scene Collection)
    for col in list(bpy.data.collections):
        try:
            bpy.data.collections.remove(col)
        except:
            pass

    # Remove datablocks
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

    # Purge orphans (Blender 3.x/4.x)
    for _ in range(5):
        try:
            bpy.ops.outliner.orphans_purge(do_recursive=True, do_local_ids=True, do_linked_ids=True)
        except:
            try:
                bpy.ops.outliner.orphans_purge(do_recursive=True)
            except:
                break


# =====================================================
# TERRAIN CONFIG
# =====================================================
GRID_X = 200          # increase for more detail (single mesh, still fast)
GRID_Y = 200
CELL_SIZE = 1.0

NOISE_SCALE = 0.035
HEIGHT = 10.0
OCTAVES = 6
LACUNARITY = 2.0
GAIN = 0.5

CENTER_GRID = True

TERRAIN_NAME = "Terrain"
TERRAIN_COLLECTION = "Terrain"

SEA_LEVEL = 0.0

# Color bands (RGBA)
COLOR_DEEP_WATER  = (0.02, 0.08, 0.25, 1.0)  # lowest
COLOR_SHALLOW     = (0.08, 0.25, 0.55, 1.0)  # light-ish blue
COLOR_SAND        = (0.78, 0.72, 0.52, 1.0)  # at sea level
COLOR_MOUNTAIN    = (0.22, 0.28, 0.20, 1.0)  # higher
COLOR_SNOW        = (0.95, 0.95, 0.95, 1.0)  # highest


# =====================================================
# UTIL
# =====================================================
def lerp(a, b, t):
    return a + (b - a) * t

def lerp4(c1, c2, t):
    return (
        lerp(c1[0], c2[0], t),
        lerp(c1[1], c2[1], t),
        lerp(c1[2], c2[2], t),
        lerp(c1[3], c2[3], t),
    )

def clamp01(x):
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def safe_set_input(bsdf, key_candidates, value):
    """Set a Principled BSDF input handling Blender version naming differences."""
    keys = set(bsdf.inputs.keys())
    for k in key_candidates:
        if k in keys:
            bsdf.inputs[k].default_value = value
            return True
    return False

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
# HEIGHT -> COLOR (bands with smooth transitions)
# Order requested:
# highest snow -> mountain -> sand at sea -> light blue -> dark blue at lowest
# =====================================================
def color_from_height(h, hmin, hmax):
    # Define thresholds relative to range
    # Adjust these to taste
    t_sea   = SEA_LEVEL
    t_shal  = lerp(hmin, t_sea, 0.55)   # "not very shallow" zone (higher than deep)
    t_deep  = hmin                      # lowest
    t_mtn   = lerp(t_sea, hmax, 0.55)   # mountain
    t_snow  = lerp(t_sea, hmax, 0.82)   # snow top

    # Deep water -> Shallow(=light-ish) -> Sand(at sea) -> Mountain -> Snow
    if h <= t_shal:
        # deep -> shallow
        t = clamp01((h - t_deep) / (t_shal - t_deep + 1e-9))
        return lerp4(COLOR_DEEP_WATER, COLOR_SHALLOW, t)
    elif h <= t_sea:
        # shallow -> sand (approaching sea level)
        t = clamp01((h - t_shal) / (t_sea - t_shal + 1e-9))
        return lerp4(COLOR_SHALLOW, COLOR_SAND, t)
    elif h <= t_mtn:
        # sand -> mountain
        t = clamp01((h - t_sea) / (t_mtn - t_sea + 1e-9))
        return lerp4(COLOR_SAND, COLOR_MOUNTAIN, t)
    elif h <= t_snow:
        # mountain -> snow
        t = clamp01((h - t_mtn) / (t_snow - t_mtn + 1e-9))
        return lerp4(COLOR_MOUNTAIN, COLOR_SNOW, t)
    else:
        return COLOR_SNOW


# =====================================================
# MATERIALS
# =====================================================
def make_terrain_material(color_attr_name="terrain_col"):
    mat = bpy.data.materials.new("MAT_Terrain")
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (400, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (150, 0)

    # Read color attribute (Blender 3/4 compatible)
    # Blender 4: ShaderNodeVertexColor was replaced; prefer ShaderNodeAttribute
    attr = nodes.new("ShaderNodeAttribute")
    attr.location = (-200, 0)
    attr.attribute_name = color_attr_name

    links.new(attr.outputs.get("Color"), bsdf.inputs.get("Base Color"))
    links.new(bsdf.outputs.get("BSDF"), out.inputs.get("Surface"))

    # Mild roughness
    safe_set_input(bsdf, ["Roughness"], 0.8)
    safe_set_input(bsdf, ["Specular", "Specular IOR Level"], 0.2)

    return mat


def setup_world_sky(strength=0.5):
    # Create world
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

    # Pick a sky model that exists in THIS Blender
    # Error you got shows available: ('SINGLE_SCATTERING','MULTIPLE_SCATTERING','PREETHAM','HOSEK_WILKIE')
    try:
        available = list(sky.sky_type_items) if hasattr(sky, "sky_type_items") else None
    except:
        available = None

    # Direct, robust selection:
    for candidate in ("MULTIPLE_SCATTERING","PREETHAM", "HOSEK_WILKIE",  "SINGLE_SCATTERING"):
        try:
            sky.sky_type = candidate
            break
        except:
            continue

    links.new(sky.outputs["Color"], bg.inputs["Color"])
    links.new(bg.outputs["Background"], out.inputs["Surface"])


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

    # Water look
    safe_set_input(bsdf, ["Base Color"], (0.03, 0.12, 0.20, 1.0))
    safe_set_input(bsdf, ["Roughness"], 0.02)
    safe_set_input(bsdf, ["IOR"], 1.333)

    # Transmission name differs across versions:
    # Blender 3.x: "Transmission"
    # Blender 4.x: "Transmission Weight"
    safe_set_input(bsdf, ["Transmission", "Transmission Weight"], 1.0)

    # Optional: Specular name differs:
    safe_set_input(bsdf, ["Specular", "Specular IOR Level"], 0.5)

    # Fake waves via normals (NO geometry waves)
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

    # Links
    links.new(texcoord.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])

    # Normal socket name is stable
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    # Eevee refraction/reflection options (if present)
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
# TERRAIN MESH (single mesh, fast)
# =====================================================
def create_terrain_mesh():
    # Collection
    col = bpy.data.collections.new(TERRAIN_COLLECTION)
    bpy.context.scene.collection.children.link(col)

    # Mesh + Object
    mesh = bpy.data.meshes.new(TERRAIN_NAME)
    obj = bpy.data.objects.new(TERRAIN_NAME, mesh)
    col.objects.link(obj)

    # Build geometry with bmesh
    bm = bmesh.new()

    ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
    oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

    verts = [[None] * GRID_Y for _ in range(GRID_X)]
    heights = [[0.0] * GRID_Y for _ in range(GRID_X)]

    hmin =  1e9
    hmax = -1e9

    # Create vertices
    for x in range(GRID_X):
        for y in range(GRID_Y):
            wx = ox + x * CELL_SIZE
            wy = oy + y * CELL_SIZE
            wz = fbm(x, y) * HEIGHT
            heights[x][y] = wz
            hmin = min(hmin, wz)
            hmax = max(hmax, wz)
            verts[x][y] = bm.verts.new((wx, wy, wz))

    bm.verts.ensure_lookup_table()

    # Faces (quads)
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

    bm.faces.ensure_lookup_table()

    # Write mesh
    bm.to_mesh(mesh)
    bm.free()

    # Flat shading for lowpoly look (optional)
    # Set polygon smooth = False for all
    for p in mesh.polygons:
        p.use_smooth = False

    # Create color attribute on mesh (Blender 3/4)
    color_attr_name = "terrain_col"
    try:
        # Blender 3.2+ / 4.x
        if hasattr(mesh, "color_attributes"):
            # Ensure exists
            if color_attr_name in mesh.color_attributes:
                mesh.color_attributes.remove(mesh.color_attributes[color_attr_name])
            color_attr = mesh.color_attributes.new(
                name=color_attr_name,
                type='BYTE_COLOR',
                domain='CORNER'
            )
        else:
            # Legacy (very old)
            if not mesh.vertex_colors:
                mesh.vertex_colors.new(name=color_attr_name)
            color_attr = mesh.vertex_colors[color_attr_name]
    except:
        color_attr = None

    # Fill per-corner colors based on vertex height
    if color_attr is not None:
        # We need corner colors -> loop domain
        # In Blender 4, color_attr.data is per-corner
        # We set each loop's color from its vertex height
        loops = mesh.loops
        polys = mesh.polygons

        data = color_attr.data
        for poly in polys:
            for li in poly.loop_indices:
                vi = loops[li].vertex_index
                z = mesh.vertices[vi].co.z
                c = color_from_height(z, hmin, hmax)
                try:
                    data[li].color = c
                except:
                    # Some versions want (r,g,b,a) but stored as 4 floats anyway
                    data[li].color = (c[0], c[1], c[2], c[3])

    # Material that reads the attribute
    mat = make_terrain_material(color_attr_name=color_attr_name)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return obj, (hmin, hmax), (ox, oy)


# =====================================================
# WATER PLANE
# =====================================================
def create_water_plane(terrain_bounds, water_z=SEA_LEVEL, margin=20.0):
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

    mat = make_water_material()
    obj.data.materials.append(mat)

    # Enable Eevee SSR/refraction if available (harmless if using Cycles)
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
# RUN
# =====================================================
full_wipe_scene()

# Terrain
terrain_obj, (hmin, hmax), (ox, oy) = create_terrain_mesh()

# World sky strength = 0.5 (your request)
setup_world_sky(strength=0.1)

# Water (bump-only waves)
water_obj = create_water_plane((ox, oy), water_z=SEA_LEVEL, margin=25.0)

# Optional: move camera/light later as needed
print("Done. Terrain min/max height:", hmin, hmax)

