"""Cinematic 4-second 3D speaker shot for BRYAN.STL STUDIO.

Run with Blender 4.x: blender -b -t 2 --python blender/music_24h_speaker.py -- --preview
The render is real meshes, material lighting and moving camera. No sprites or still frames.
"""
import bpy
import math
import os
import random
import sys
from mathutils import Vector


FRAMES = 120
FPS = 30
ROOT = os.path.abspath(os.getcwd())
OUT = os.path.join(ROOT, "output", "music-24h-3d")
os.makedirs(OUT, exist_ok=True)
random.seed(24)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
s = bpy.context.scene
try:
    s.render.engine = "BLENDER_EEVEE_NEXT"
except (TypeError, ValueError):
    s.render.engine = "BLENDER_EEVEE"
s.render.resolution_x = 720
s.render.resolution_y = 1280
s.render.resolution_percentage = 100
s.render.fps = FPS
s.frame_start = 1
s.frame_end = FRAMES
s.render.image_settings.file_format = "PNG"
s.render.image_settings.color_mode = "RGB"
s.render.film_transparent = False
s.render.threads_mode = "FIXED"
s.render.threads = 2
s.view_settings.view_transform = "AgX"
s.camera = None


def material(name, rgb, metallic=0.0, rough=.45, emission=None, strength=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*rgb, 1)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = rough
    if emission:
        p.inputs["Emission Color"].default_value = (*emission, 1)
        p.inputs["Emission Strength"].default_value = strength
    return m


cabinet_mat = material("matte black cabinet", (.011, .014, .025), .12, .55)
edge_mat = material("brushed dark anodized edge", (.10, .12, .16), .78, .25)
rubber_mat = material("woofer rubber surround", (.014, .016, .024), .04, .83)
cone_mat = material("woven carbon cone", (.047, .055, .073), .32, .39)
cap_mat = material("central dustcap graphite", (.065, .07, .088), .54, .27)
violet = material("violet luminous trim", (.11, .025, .7), .15, .3, (.4, .16, 1), 5)
cyan = material("cool accent", (.015, .25, .55), .15, .3, (.045, .64, 1), 4)
floor_mat = material("dark reflective floor", (.01, .012, .019), .48, .18)


def beveled_box(name, loc, size, mat, bevel=.06):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    ob = bpy.context.object
    ob.name = name
    ob.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = ob.modifiers.new("machined soft edges", "BEVEL")
    mod.width = bevel
    mod.segments = 4
    ob.modifiers.new("weighted normals", "WEIGHTED_NORMAL")
    ob.data.materials.append(mat)
    return ob


def cyl(name, radius, depth, loc, mat, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc,
                                        rotation=(math.pi/2, 0, 0))
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    ob.modifiers.new("smooth weighted normals", "WEIGHTED_NORMAL")
    for f in ob.data.polygons:
        f.use_smooth = True
    return ob


def torus(name, radius, minor, loc, mat):
    bpy.ops.mesh.primitive_torus_add(major_segments=128, minor_segments=16,
                                    location=loc, rotation=(math.pi/2, 0, 0),
                                    major_radius=radius, minor_radius=minor)
    ob = bpy.context.object
    ob.name = name
    ob.data.materials.append(mat)
    for f in ob.data.polygons:
        f.use_smooth = True
    return ob


def cone_mesh(name, z, front, radius):
    # Radial cross-section, genuinely curved and recessed, facing camera toward -Y.
    profile = [(0.0, front-.14), (.28, front-.14), (.40, front-.20),
               (.65, front-.38), (.89, front-.12), (1.0, front-.05)]
    rings = 96
    verts = []
    faces = []
    for r, y in profile:
        rr = max(.002, r*radius)
        for i in range(rings):
            a = 2*math.pi*i/rings
            verts.append((rr*math.cos(a), y, z+rr*math.sin(a)))
    for j in range(len(profile)-1):
        for i in range(rings):
            a, b = j*rings+i, j*rings+(i+1)%rings
            faces.append((a, b, b+rings, a+rings))
    mesh = bpy.data.meshes.new("woofer cone mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    s.collection.objects.link(ob)
    ob.data.materials.append(cone_mat)
    for f in ob.data.polygons:
        f.use_smooth = True
    ob.modifiers.new("subdivision", "SUBSURF").levels = 1
    return ob


beveled_box("full depth speaker enclosure", (0, .32, 2.55), (3.4, 1.24, 5.2), cabinet_mat, .14)
beveled_box("machined front baffle", (0, -.34, 2.55), (3.18, .08, 4.98), edge_mat, .08)
beveled_box("inset front fabric", (0, -.397, 2.55), (2.98, .035, 4.79), cabinet_mat, .045)
beveled_box("side port", (1.71, .12, 3.58), (.025, .8, 1.13), edge_mat, .01)

driver = cyl("woofer frame", 1.29, .09, (0, -.45, 2.16), edge_mat)
cyl("woofer surround", 1.15, .07, (0, -.515, 2.16), rubber_mat)
cone = cone_mesh("animated carbon woofer", 2.16, -.55, 1.08)
cap = cyl("woofer dust cap", .31, .14, (0, -.73, 2.16), cap_mat)
outer = torus("metal outer lip", 1.29, .025, (0, -.52, 2.16), edge_mat)
inner = torus("violet driver detail", 1.13, .012, (0, -.555, 2.16), violet)
for a in range(12):
    ang = 2*math.pi*a/12
    x, z = 1.22*math.cos(ang), 2.16+1.22*math.sin(ang)
    cyl("mounting screw %02d"%a, .025, .014, (x, -.565, z), cap_mat, 16)

# A second real driver establishes scale; it is not another copied sprite.
cyl("upper tweeter mount", .48, .08, (0, -.46, 4.18), edge_mat, 64)
cyl("upper tweeter dome", .32, .15, (0, -.59, 4.18), cap_mat, 64)
torus("tweeter detail", .43, .018, (0, -.55, 4.18), cyan)

for ob in (cone, cap):
    y = ob.location.y
    for f, displacement in [(1,0),(7,-.065),(13,.015),(21,-.08),(30,0),
                            (38,-.075),(46,.015),(55,-.095),(64,0),
                            (72,-.075),(80,.02),(88,-.10),(94,0),(96,0),(120,0)]:
        ob.location.y = y+displacement
        ob.keyframe_insert(data_path="location", frame=f)

# Radiating physical torus meshes move and fade, stopping at the missing drop.
for i in range(4):
    ring = torus("expanding sound ring %d"%i, 1.38, .013,
                 (0, -.84-i*.05, 2.16), cyan if i%2 else violet)
    for f in range(1, 121, 15):
        if f < 96:
            q = ((f+i*17) % 62)/62
            sc = .9+q*.68
        else:
            sc = 1.36
        ring.scale = (sc, sc, sc)
        ring.keyframe_insert(data_path="scale", frame=f)
    ring.hide_render = False
    ring.keyframe_insert(data_path="hide_render", frame=95)
    ring.hide_render = True
    ring.keyframe_insert(data_path="hide_render", frame=96)

beveled_box("floor", (0, 0, -.13), (100, 100, .2), floor_mat, .02)


def light(name, loc, color, power, size):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = power
    data.color = color
    data.shape = "DISK"
    data.size = size
    ob = bpy.data.objects.new(name, data)
    s.collection.objects.link(ob)
    ob.location = loc
    target = Vector((0, 0, 2.35))
    ob.rotation_euler = (target-ob.location).to_track_quat("-Z", "Y").to_euler()
    return data


key = light("white sculpting softbox", (-4, -5, 7), (0.8, .85, 1.0), 1250, 5)
light("violet rim on enclosure", (4, 1, 5), (.45, .15, 1), 1800, 3.5)
light("cyan edge light", (-3, 2, 2), (.09, .55, 1), 1350, 3)
for f, energy in [(1,1100),(75,1500),(92,2100),(96,70),(120,70)]:
    key.energy = energy
    key.keyframe_insert(data_path="energy", frame=f)

world = bpy.data.worlds.new("deep blue studio")
s.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (.005, .007, .016, 1)
bg.inputs["Strength"].default_value = .28

bpy.ops.object.empty_add(location=(0, 0, 2.4))
aim = bpy.context.object
aim.name = "camera aim"
bpy.ops.object.camera_add(location=(3.7, -10.2, 3.5))
cam = bpy.context.object
s.camera = cam
cam.data.lens = 37
cam.data.dof.use_dof = True
cam.data.dof.focus_object = aim
cam.data.dof.aperture_fstop = 5.6
track = cam.constraints.new("TRACK_TO")
track.target = aim
track.track_axis = "TRACK_NEGATIVE_Z"
track.up_axis = "UP_Y"
for f, pos in [(1,(3.7,-10.2,3.5)), (55,(2.3,-8.6,3.18)),
               (94,(.85,-7.5,2.9)), (120,(.6,-7.4,2.9))]:
    cam.location = pos
    cam.keyframe_insert(data_path="location", frame=f)

s.render.image_settings.file_format = "PNG"
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "speaker-shot.blend"))
if "--preview" in sys.argv:
    s.render.resolution_percentage = 65
    s.frame_set(78)
    s.render.filepath = os.path.join(OUT, "speaker-preview.png")
    bpy.ops.render.render(write_still=True)
elif "--full" in sys.argv:
    s.render.resolution_percentage = 100
    s.render.filepath = os.path.join(OUT, "frame_")
    bpy.ops.render.render(animation=True)
else:
    s.frame_set(78)
    s.render.filepath = os.path.join(OUT, "speaker-preview.png")
    bpy.ops.render.render(write_still=True)
