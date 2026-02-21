---
name: blender
description: Control Blender via Python API (bpy) and CLI for 3D modeling, rendering, animation, scene manipulation, mesh operations, materials, lighting, camera setup, and video editing. Run headless with `blender --background`.
---

# Blender Skill

Control Blender headless via the bundled CLI script.

## Prerequisites

Blender must be installed and `blender` in PATH.
- macOS: `brew install --cask blender` then symlink or add to PATH
- Or download from [blender.org](https://www.blender.org/download/)

Verify: `blender --version`

## Usage

All commands run headless:

```bash
blender --background --python skills/blender/scripts/blender_cli.py -- <command> [options]
```

To operate on an existing .blend file:

```bash
blender --background myfile.blend --python skills/blender/scripts/blender_cli.py -- <command> [options]
```

## Commands

| Command | Description | Key Args |
|---------|-------------|----------|
| `info` | Scene info (objects, materials, cameras) | |
| `add-object` | Add primitive | `--type cube/sphere/cylinder/plane/cone/torus --location X Y Z --rotation X Y Z --scale X Y Z --name NAME` |
| `delete-object` | Delete object by name | `--name NAME` |
| `set-material` | Create/assign material with color | `--object NAME --material NAME --color R G B` |
| `add-light` | Add light source | `--type point/sun/spot/area --energy N --color R G B --location X Y Z --name NAME` |
| `set-camera` | Position/aim camera | `--location X Y Z --target X Y Z --name NAME` |
| `render` | Render scene to file | `--output PATH --resolution X Y --engine CYCLES/EEVEE --format PNG/JPEG/EXR` |
| `import-file` | Import 3D file | `--path FILE --format obj/fbx/stl/gltf` |
| `export-file` | Export 3D file | `--path FILE --format obj/fbx/stl/gltf` |
| `run-script` | Execute arbitrary .py in Blender | `--path SCRIPT.py` |

## Tips

- Chain commands by running multiple blender invocations, saving between steps with `--save` flag
- For complex scenes, write a custom .py script and use `run-script`
- See `references/bpy-cheatsheet.md` for common bpy patterns
- Default scene has a cube, camera, and light — use `delete-object --name Cube` to clear it
