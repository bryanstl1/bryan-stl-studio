# Blender 3D cinematic festival scene (Blender 4.x)
# Render: blender -b -t 4 --python blender/festival_scene.py
# Full sequence: blender -b -t 4 --python blender/festival_scene.py -- --full
# No external models or textures; procedural geometry and PBR materials.
import bpy, math, random, os, sys
random.seed(42)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=24
s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.resolution_percentage=100
s.render.fps=30;s.frame_start=1;s.frame_end=240;s.render.image_settings.file_format='PNG'
s.world.color=(.006,.008,.015);s.view_settings.view_transform='AgX'
def mat(name,color,metal=0,rough=.4,emission=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=emission
 return m
black=mat('Obsidian stage',(.018,.019,.027),.45,.22)
steel=mat('Brushed metal',(.13,.15,.19),.8,.24)
cyan=mat('Cyan LEDs',(.015,.4,.95),.1,.25,7)
magenta=mat('Magenta LEDs',(.85,.025,.35),.1,.25,7)
skin=mat('Crowd skin',(.21,.13,.11),0,.8)
cloth=[mat('Cloth'+str(i),c,0,.85) for i,c in enumerate([(.04,.04,.06),(.1,.03,.08),(.03,.08,.1)])]
def cube(name,loc,scale,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);return o
cube('Festival ground',(0,0,-.2),(40,65,.4),black)
cube('Stage foundation',(0,13,1),(18,7,2),steel)
cube('Main LED wall',(0,16,6),(14,.3,8),black)
for x in [-7,7]:cube('Stage column',(x,15,6),(.55,1.2,11),steel)
for j in range(5):
 w=13-j*1.4
 cube('LED arch top '+str(j),(0,14-j*.6,10-j*.65),(w,.15,.18),cyan if j%2 else magenta)
 for x in [-w/2,w/2]:cube('LED arch upright',(x,14-j*.6,6-j*.32),(.18,.15,8-j*.7),cyan if j%2 else magenta)
cube('DJ console',(0,10,3),(4.5,1.4,1.3),black)
cube('DJ torso',(0,11,4.15),(.9,.55,1.4),cloth[0])
bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.38,location=(0,11,5.12))
bpy.context.object.name='DJ head';bpy.context.object.data.materials.append(skin)
arm=cube('DJ drop arm',(.65,10.8,4.5),(.22,.22,1.25),skin)
for f,angle in [(1,0),(105,-.85),(135,0)]:arm.rotation_euler[1]=angle;arm.keyframe_insert('rotation_euler',frame=f)
for i in range(140):
 x=random.uniform(-13,13);y=random.uniform(-24,6)
 if abs(x)<2 and y>4:continue
 body=cube('Crowd body %03d'%i,(x,y,.9),(.36,.3,1.2),random.choice(cloth))
 bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=6,radius=.2,location=(x,y,1.73))
 head=bpy.context.object;head.name='Crowd head %03d'%i;head.data.materials.append(skin)
 for o in (body,head):
  base=o.location.z
  for f in (1,16,31,46,61,76,91,106,121,151,181,211,240):
   o.location.z=base+(.075*math.sin(f*.22+i*.67) if f<=120 else .012*math.sin(f*.08+i))
   o.keyframe_insert('location',frame=f)
for i,(x,col) in enumerate([(-7,(.12,.3,1)),(7,(1,.08,.36)),(0,(.6,.5,1))]):
 ld=bpy.data.lights.new('Moving stage light '+str(i),'AREA');ld.energy=2100;ld.color=col;ld.shape='DISK';ld.size=6
 o=bpy.data.objects.new('Moving stage light '+str(i),ld);s.collection.objects.link(o);o.location=(x,6,13)
 for f,e in [(1,1800),(105,3500),(119,5200),(121,160),(240,160)]:ld.energy=e;ld.keyframe_insert('energy',frame=f)
bpy.ops.object.camera_add(location=(0,-26,10));camera=bpy.context.object;s.camera=camera
track=camera.constraints.new('TRACK_TO');track.target=bpy.data.objects['DJ console'];track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
for f,loc in [(1,(0,-28,10)),(60,(-4,-18,8)),(119,(2,-13,7)),(150,(7,-15,8)),(240,(0,-33,17))]:
 camera.location=loc;camera.keyframe_insert('location',frame=f)
camera.data.type='PERSP';camera.data.lens=31
fog=bpy.data.materials.new('Atmosphere');fog.use_nodes=True
nodes=fog.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');vol=nodes.new('ShaderNodeVolumePrincipled')
vol.inputs['Density'].default_value=.012;vol.inputs['Color'].default_value=(.2,.25,.4,1)
fog.node_tree.links.new(vol.outputs['Volume'],out.inputs['Volume'])
cube('Atmospheric volume',(0,0,9),(48,80,22),fog)
os.makedirs('output',exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('output/festival-v04.blend'))
if '--preview' in sys.argv:
 s.render.resolution_percentage=25
 s.cycles.samples=8
 s.frame_set(90)
 s.render.filepath=os.path.abspath('output/blender-preview.png')
 bpy.ops.render.render(write_still=True)
elif '--full' in sys.argv:
 os.makedirs('output/blender',exist_ok=True)
 s.render.filepath=os.path.abspath('output/blender/frame_');bpy.ops.render.render(animation=True)
else:
 s.frame_set(90);s.render.filepath=os.path.abspath('output/blender-preview.png');bpy.ops.render.render(write_still=True)
