import bpy
import bmesh
from mathutils import Vector
from mathutils.noise import noise as perlin_noise

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
# TERRAIN CONFIG
# =====================================================
GRID_X = 200
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

# Subdivision (requested)
TERRAIN_SUBDIV_LEVEL = 1  # level 1

# Terrain bump/normal (requested: similar to water)
TERRAIN_BUMP_SCALE = 10.0
TERRAIN_BUMP_DETAIL = 6.0
TERRAIN_BUMP_ROUGHNESS = 0.5
TERRAIN_BUMP_STRENGTH = 0.35
TERRAIN_BUMP_DISTANCE = 0.15
TERRAIN_BUMP_MAPPING_SCALE = (2.0, 2.0, 2.0)

# Color bands (RGBA)
COLOR_DEEP_WATER  = (0.02, 0.08, 0.25, 1.0)
COLOR_SHALLOW     = (0.08, 0.25, 0.55, 1.0)
COLOR_SAND        = (0.78, 0.72, 0.52, 1.0)
COLOR_MOUNTAIN    = (0.22, 0.28, 0.20, 1.0)
COLOR_SNOW        = (0.95, 0.95, 0.95, 1.0)


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
# =====================================================
def color_from_height(h, hmin, hmax):
    t_sea   = SEA_LEVEL
    t_shal  = lerp(hmin, t_sea, 0.55)
    t_deep  = hmin
    t_mtn   = lerp(t_sea, hmax, 0.55)
    t_snow  = lerp(t_sea, hmax, 0.82)

    if h <= t_shal:
        t = clamp01((h - t_deep) / (t_shal - t_deep + 1e-9))
        return lerp4(COLOR_DEEP_WATER, COLOR_SHALLOW, t)
    elif h <= t_sea:
        t = clamp01((h - t_shal) / (t_sea - t_shal + 1e-9))
        return lerp4(COLOR_SHALLOW, COLOR_SAND, t)
    elif h <= t_mtn:
        t = clamp01((h - t_sea) / (t_mtn - t_sea + 1e-9))
        return lerp4(COLOR_SAND, COLOR_MOUNTAIN, t)
    elif h <= t_snow:
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
    out.location = (600, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (250, 0)

    # Color attribute (keeps height colors)
    attr = nodes.new("ShaderNodeAttribute")
    attr.location = (-450, 0)
    attr.attribute_name = color_attr_name
    links.new(attr.outputs.get("Color"), bsdf.inputs.get("Base Color"))

    # --- Terrain bump/normal (noise -> bump -> BSDF normal) ---
    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-900, -220)

    mapping = nodes.new("ShaderNodeMapping")
    mapping.location = (-700, -220)
    try:
        mapping.inputs["Scale"].default_value = TERRAIN_BUMP_MAPPING_SCALE
    except:
        pass

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-500, -220)
    try:
        noise.inputs["Scale"].default_value = TERRAIN_BUMP_SCALE
        noise.inputs["Detail"].default_value = TERRAIN_BUMP_DETAIL
        noise.inputs["Roughness"].default_value = TERRAIN_BUMP_ROUGHNESS
    except:
        pass

    bump = nodes.new("ShaderNodeBump")
    bump.location = (-150, -320)
    try:
        bump.inputs["Strength"].default_value = TERRAIN_BUMP_STRENGTH
        bump.inputs["Distance"].default_value = TERRAIN_BUMP_DISTANCE
    except:
        pass

    links.new(texcoord.outputs["Object"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    # Mild roughness
    safe_set_input(bsdf, ["Roughness"], 0.85)
    safe_set_input(bsdf, ["Specular", "Specular IOR Level"], 0.2)

    links.new(bsdf.outputs.get("BSDF"), out.inputs.get("Surface"))
    return mat


def setup_world_sky(strength=0.5):
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

    for candidate in ("MULTIPLE_SCATTERING","PREETHAM","HOSEK_WILKIE","SINGLE_SCATTERING"):
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

    safe_set_input(bsdf, ["Base Color"], (0.03, 0.12, 0.20, 1.0))
    safe_set_input(bsdf, ["Roughness"], 0.02)
    safe_set_input(bsdf, ["IOR"], 1.333)
    safe_set_input(bsdf, ["Transmission", "Transmission Weight"], 1.0)
    safe_set_input(bsdf, ["Specular", "Specular IOR Level"], 0.5)

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
# COLOR ATTRIBUTE HELPERS (keep colors after subdivision)
# =====================================================
def ensure_color_attribute(mesh, name="terrain_col"):
    try:
        if hasattr(mesh, "color_attributes"):
            if name in mesh.color_attributes:
                # keep it; we will overwrite data anyway
                return mesh.color_attributes[name]
            return mesh.color_attributes.new(name=name, type='BYTE_COLOR', domain='CORNER')
        else:
            if not mesh.vertex_colors:
                mesh.vertex_colors.new(name=name)
            return mesh.vertex_colors[name]
    except:
        return None

def recompute_height_colors(obj, color_attr_name="terrain_col"):
    mesh = obj.data
    # recompute hmin/hmax from current geometry
    hmin = 1e9
    hmax = -1e9
    for v in mesh.vertices:
        z = v.co.z
        if z < hmin: hmin = z
        if z > hmax: hmax = z

    color_attr = ensure_color_attribute(mesh, color_attr_name)
    if color_attr is None:
        return (hmin, hmax)

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
                data[li].color = (c[0], c[1], c[2], c[3])

    return (hmin, hmax)


# =====================================================
# TERRAIN MESH (single mesh, fast)
# =====================================================
def create_terrain_mesh():
    col = bpy.data.collections.new(TERRAIN_COLLECTION)
    bpy.context.scene.collection.children.link(col)

    mesh = bpy.data.meshes.new(TERRAIN_NAME)
    obj = bpy.data.objects.new(TERRAIN_NAME, mesh)
    col.objects.link(obj)

    bm = bmesh.new()

    ox = -(GRID_X - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0
    oy = -(GRID_Y - 1) * CELL_SIZE * 0.5 if CENTER_GRID else 0.0

    verts = [[None] * GRID_Y for _ in range(GRID_X)]
    hmin =  1e9
    hmax = -1e9

    for x in range(GRID_X):
        for y in range(GRID_Y):
            wx = ox + x * CELL_SIZE
            wy = oy + y * CELL_SIZE
            wz = fbm(x, y) * HEIGHT
            hmin = min(hmin, wz)
            hmax = max(hmax, wz)
            verts[x][y] = bm.verts.new((wx, wy, wz))

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

    bm.faces.ensure_lookup_table()
    bm.to_mesh(mesh)
    bm.free()

    # flat shading initial (kept)
    for p in mesh.polygons:
        p.use_smooth = False

    # Create & fill color attribute per-corner (by height)
    color_attr_name = "terrain_col"
    color_attr = ensure_color_attribute(mesh, color_attr_name)

    if color_attr is not None:
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
                    data[li].color = (c[0], c[1], c[2], c[3])

    # Material (reads attribute) + terrain bump
    mat = make_terrain_material(color_attr_name=color_attr_name)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    return obj, (hmin, hmax), (ox, oy), color_attr_name


# =====================================================
# SUBDIVIDE TERRAIN (apply level 1) + RECOLOR BY HEIGHT
# =====================================================
def apply_subdivision_and_recolor(obj, color_attr_name="terrain_col", level=1):
    # Add modifier
    mod = obj.modifiers.new(name="Subdiv", type='SUBSURF')
    mod.levels = int(level)
    mod.render_levels = int(level)
    try:
        mod.subdivision_type = 'CATMULL_CLARK'
    except:
        pass

    # Apply modifier (requested "apply")
    view_layer = bpy.context.view_layer
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    view_layer.objects.active = obj

    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        print("WARNING: Could not apply subdivision modifier:", e)

    # Recompute colors by height after topology change (keeps the scheme)
    hmin, hmax = recompute_height_colors(obj, color_attr_name=color_attr_name)

    # Restore flat shading if you want the lowpoly look even after subdiv
    # (if you prefer smooth after subdiv, set to True)
    for p in obj.data.polygons:
        p.use_smooth = False

    return (hmin, hmax)


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
terrain_obj, (hmin, hmax), (ox, oy), color_attr_name = create_terrain_mesh()

# 1) Apply subdivision surface level 1 + 3) keep colors by height (recomputed)
hmin2, hmax2 = apply_subdivision_and_recolor(
    terrain_obj,
    color_attr_name=color_attr_name,
    level=TERRAIN_SUBDIV_LEVEL
)

# World sky
setup_world_sky(strength=0.1)

# Water
water_obj = create_water_plane((ox, oy), water_z=SEA_LEVEL, margin=25.0)

print("Done.")
print("Terrain min/max before subdiv:", hmin, hmax)
print("Terrain min/max after subdiv :", hmin2, hmax2)

