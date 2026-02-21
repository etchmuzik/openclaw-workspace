#!/usr/bin/env python3
"""Blender CLI helper — run via: blender --background --python blender_cli.py -- <command> [args]"""

import sys
import argparse
import json
import math

import bpy  # type: ignore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _vec(values, default=(0, 0, 0)):
    return tuple(float(v) for v in values) if values else default


def _color(values, default=(0.8, 0.8, 0.8)):
    return tuple(float(v) for v in values) if values else default


def _save_if_requested(args):
    if getattr(args, "save", None):
        bpy.ops.wm.save_as_mainfile(filepath=args.save)
        print(f"Saved: {args.save}")


def _look_at(obj, target):
    """Point obj's -Z axis at target location."""
    from mathutils import Vector, Matrix  # type: ignore
    loc = obj.location
    direction = Vector(target) - loc
    rot_quat = direction.to_track_quat("-Z", "Y")
    obj.rotation_euler = rot_quat.to_euler()


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_info(args):
    scene = bpy.context.scene
    data = {
        "scene": scene.name,
        "frame": {"current": scene.frame_current, "start": scene.frame_start, "end": scene.frame_end},
        "render": {"engine": scene.render.engine, "resolution": [scene.render.resolution_x, scene.render.resolution_y]},
        "objects": [],
        "materials": [m.name for m in bpy.data.materials],
        "cameras": [c.name for c in bpy.data.cameras],
    }
    for obj in scene.objects:
        data["objects"].append({
            "name": obj.name,
            "type": obj.type,
            "location": list(obj.location),
        })
    print(json.dumps(data, indent=2))


def cmd_add_object(args):
    ops = {
        "cube": bpy.ops.mesh.primitive_cube_add,
        "sphere": bpy.ops.mesh.primitive_uv_sphere_add,
        "cylinder": bpy.ops.mesh.primitive_cylinder_add,
        "plane": bpy.ops.mesh.primitive_plane_add,
        "cone": bpy.ops.mesh.primitive_cone_add,
        "torus": bpy.ops.mesh.primitive_torus_add,
    }
    fn = ops.get(args.type)
    if not fn:
        print(f"Unknown type: {args.type}. Options: {list(ops.keys())}")
        sys.exit(1)
    loc = _vec(args.location)
    rot = tuple(math.radians(v) for v in _vec(args.rotation))
    fn(location=loc, rotation=rot)
    obj = bpy.context.active_object
    if args.scale:
        obj.scale = _vec(args.scale, (1, 1, 1))
    if args.name:
        obj.name = args.name
    print(f"Added {args.type}: {obj.name}")
    _save_if_requested(args)


def cmd_delete_object(args):
    obj = bpy.data.objects.get(args.name)
    if not obj:
        print(f"Object not found: {args.name}")
        sys.exit(1)
    bpy.data.objects.remove(obj, do_unlink=True)
    print(f"Deleted: {args.name}")
    _save_if_requested(args)


def cmd_set_material(args):
    obj = bpy.data.objects.get(args.object)
    if not obj:
        print(f"Object not found: {args.object}")
        sys.exit(1)
    mat_name = args.material or f"{args.object}_material"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        c = _color(args.color)
        bsdf.inputs["Base Color"].default_value = (c[0], c[1], c[2], 1.0)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)
    print(f"Material '{mat.name}' applied to '{obj.name}'")
    _save_if_requested(args)


def cmd_add_light(args):
    light_types = {"point": "POINT", "sun": "SUN", "spot": "SPOT", "area": "AREA"}
    lt = light_types.get(args.type)
    if not lt:
        print(f"Unknown light type: {args.type}. Options: {list(light_types.keys())}")
        sys.exit(1)
    name = args.name or f"{args.type.capitalize()}Light"
    light_data = bpy.data.lights.new(name=name, type=lt)
    light_data.energy = args.energy
    if args.color:
        light_data.color = _color(args.color)
    obj = bpy.data.objects.new(name=name, object_data=light_data)
    obj.location = _vec(args.location)
    bpy.context.collection.objects.link(obj)
    print(f"Added {args.type} light: {obj.name}")
    _save_if_requested(args)


def cmd_set_camera(args):
    cam = None
    if args.name:
        cam = bpy.data.objects.get(args.name)
    else:
        for obj in bpy.data.objects:
            if obj.type == "CAMERA":
                cam = obj
                break
    if not cam:
        cam_data = bpy.data.cameras.new(name="Camera")
        cam = bpy.data.objects.new(name="Camera", object_data=cam_data)
        bpy.context.collection.objects.link(cam)
        bpy.context.scene.camera = cam
    if args.location:
        cam.location = _vec(args.location)
    if args.target:
        _look_at(cam, _vec(args.target))
    print(f"Camera '{cam.name}' at {list(cam.location)}")
    _save_if_requested(args)


def cmd_render(args):
    scene = bpy.context.scene
    if args.engine:
        scene.render.engine = {"cycles": "CYCLES", "eevee": "BLENDER_EEVEE_NEXT"}.get(args.engine.lower(), args.engine.upper())
    if args.resolution:
        scene.render.resolution_x = int(args.resolution[0])
        scene.render.resolution_y = int(args.resolution[1])
    fmt = (args.format or "PNG").upper()
    scene.render.image_settings.file_format = fmt
    output = args.output or "/tmp/render.png"
    scene.render.filepath = output
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {output}")


def cmd_import_file(args):
    ext = args.format or args.path.rsplit(".", 1)[-1].lower()
    importers = {
        "obj": lambda p: bpy.ops.wm.obj_import(filepath=p),
        "fbx": lambda p: bpy.ops.import_scene.fbx(filepath=p),
        "stl": lambda p: bpy.ops.wm.stl_import(filepath=p),
        "gltf": lambda p: bpy.ops.import_scene.gltf(filepath=p),
        "glb": lambda p: bpy.ops.import_scene.gltf(filepath=p),
    }
    fn = importers.get(ext)
    if not fn:
        print(f"Unsupported format: {ext}")
        sys.exit(1)
    fn(args.path)
    print(f"Imported: {args.path}")
    _save_if_requested(args)


def cmd_export_file(args):
    ext = args.format or args.path.rsplit(".", 1)[-1].lower()
    exporters = {
        "obj": lambda p: bpy.ops.wm.obj_export(filepath=p),
        "fbx": lambda p: bpy.ops.export_scene.fbx(filepath=p),
        "stl": lambda p: bpy.ops.wm.stl_export(filepath=p),
        "gltf": lambda p: bpy.ops.export_scene.gltf(filepath=p, export_format="GLTF_SEPARATE"),
        "glb": lambda p: bpy.ops.export_scene.gltf(filepath=p, export_format="GLB"),
    }
    fn = exporters.get(ext)
    if not fn:
        print(f"Unsupported format: {ext}")
        sys.exit(1)
    fn(args.path)
    print(f"Exported: {args.path}")


def cmd_run_script(args):
    exec(compile(open(args.path).read(), args.path, "exec"))
    print(f"Executed: {args.path}")
    _save_if_requested(args)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def main():
    # Blender passes everything after "--" to the script
    try:
        idx = sys.argv.index("--")
        argv = sys.argv[idx + 1:]
    except ValueError:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog="blender_cli", description="Blender CLI helper")
    sub = parser.add_subparsers(dest="command")

    # info
    sub.add_parser("info")

    # add-object
    p = sub.add_parser("add-object")
    p.add_argument("--type", required=True)
    p.add_argument("--location", nargs=3, type=float)
    p.add_argument("--rotation", nargs=3, type=float)
    p.add_argument("--scale", nargs=3, type=float)
    p.add_argument("--name")
    p.add_argument("--save")

    # delete-object
    p = sub.add_parser("delete-object")
    p.add_argument("--name", required=True)
    p.add_argument("--save")

    # set-material
    p = sub.add_parser("set-material")
    p.add_argument("--object", required=True)
    p.add_argument("--material")
    p.add_argument("--color", nargs=3, type=float)
    p.add_argument("--save")

    # add-light
    p = sub.add_parser("add-light")
    p.add_argument("--type", required=True)
    p.add_argument("--energy", type=float, default=1000)
    p.add_argument("--color", nargs=3, type=float)
    p.add_argument("--location", nargs=3, type=float)
    p.add_argument("--name")
    p.add_argument("--save")

    # set-camera
    p = sub.add_parser("set-camera")
    p.add_argument("--location", nargs=3, type=float)
    p.add_argument("--target", nargs=3, type=float)
    p.add_argument("--name")
    p.add_argument("--save")

    # render
    p = sub.add_parser("render")
    p.add_argument("--output")
    p.add_argument("--resolution", nargs=2, type=int)
    p.add_argument("--engine")
    p.add_argument("--format")

    # import-file
    p = sub.add_parser("import-file")
    p.add_argument("--path", required=True)
    p.add_argument("--format")
    p.add_argument("--save")

    # export-file
    p = sub.add_parser("export-file")
    p.add_argument("--path", required=True)
    p.add_argument("--format")

    # run-script
    p = sub.add_parser("run-script")
    p.add_argument("--path", required=True)
    p.add_argument("--save")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "info": cmd_info,
        "add-object": cmd_add_object,
        "delete-object": cmd_delete_object,
        "set-material": cmd_set_material,
        "add-light": cmd_add_light,
        "set-camera": cmd_set_camera,
        "render": cmd_render,
        "import-file": cmd_import_file,
        "export-file": cmd_export_file,
        "run-script": cmd_run_script,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
