# bpy Cheatsheet

## Scene Basics
```python
import bpy

scene = bpy.context.scene
obj = bpy.context.active_object
selected = bpy.context.selected_objects
```

## Create Objects
```python
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 2))
bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2)
bpy.ops.mesh.primitive_plane_add(size=10)
bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2)
bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.25)

obj = bpy.context.active_object  # newly created object
obj.name = "MyCube"
```

## Select / Delete
```python
obj = bpy.data.objects["Cube"]
bpy.data.objects.remove(obj, do_unlink=True)

# Delete all mesh objects
for obj in [o for o in bpy.data.objects if o.type == "MESH"]:
    bpy.data.objects.remove(obj, do_unlink=True)
```

## Transform
```python
import math
obj.location = (1, 2, 3)
obj.rotation_euler = (math.radians(45), 0, 0)
obj.scale = (2, 2, 2)
```

## Materials
```python
mat = bpy.data.materials.new(name="Red")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (1, 0, 0, 1)  # RGBA
bsdf.inputs["Metallic"].default_value = 0.5
bsdf.inputs["Roughness"].default_value = 0.3

obj.data.materials.append(mat)
```

## Lighting
```python
light_data = bpy.data.lights.new(name="MyLight", type="POINT")  # POINT, SUN, SPOT, AREA
light_data.energy = 1000
light_data.color = (1, 0.9, 0.8)
light_obj = bpy.data.objects.new(name="MyLight", object_data=light_data)
light_obj.location = (5, 5, 5)
bpy.context.collection.objects.link(light_obj)
```

## Camera
```python
from mathutils import Vector

cam_data = bpy.data.cameras.new(name="Camera")
cam_data.lens = 50  # focal length mm
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
cam_obj.location = (7, -7, 5)
bpy.context.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Point at target
direction = Vector((0, 0, 0)) - cam_obj.location
cam_obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
```

## Rendering
```python
scene = bpy.context.scene
scene.render.engine = "CYCLES"  # or "BLENDER_EEVEE_NEXT"
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = "/tmp/render.png"
bpy.ops.render.render(write_still=True)
```

## Import / Export
```python
# OBJ
bpy.ops.wm.obj_import(filepath="model.obj")
bpy.ops.wm.obj_export(filepath="output.obj")

# FBX
bpy.ops.import_scene.fbx(filepath="model.fbx")
bpy.ops.export_scene.fbx(filepath="output.fbx")

# STL
bpy.ops.wm.stl_import(filepath="model.stl")
bpy.ops.wm.stl_export(filepath="output.stl")

# glTF
bpy.ops.import_scene.gltf(filepath="model.gltf")
bpy.ops.export_scene.gltf(filepath="output.glb", export_format="GLB")
```

## Modifiers
```python
obj = bpy.context.active_object
mod = obj.modifiers.new(name="Subsurf", type="SUBSURF")
mod.levels = 2
bpy.ops.object.modifier_apply(modifier="Subsurf")
```

## Keyframes / Animation
```python
obj.location = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)
obj.location = (5, 0, 0)
obj.keyframe_insert(data_path="location", frame=60)

scene.frame_start = 1
scene.frame_end = 60
```

## Collections
```python
col = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(col)
col.objects.link(obj)
```

## Clean Scene
```python
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
# Or remove all data
for c in bpy.data.collections:
    bpy.data.collections.remove(c)
```
