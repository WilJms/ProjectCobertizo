"""Run inside Blender; verifies bpy, a saved project, and a real Cycles render."""
import bpy, json, platform, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
out = ROOT / 'outputs/environment'
out.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 8
scene.render.resolution_x = 320
scene.render.resolution_y = 240
scene.render.resolution_percentage = 100
prefs = bpy.context.preferences.addons['cycles'].preferences
devices = []
try:
    prefs.compute_device_type = 'METAL'
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == 'METAL'
        devices.append({'name': device.name, 'type': device.type, 'use': bool(device.use)})
    scene.cycles.device = 'GPU' if any(d['use'] for d in devices) else 'CPU'
except Exception as error:
    devices.append({'error': str(error)})
    scene.cycles.device = 'CPU'
scene.render.filepath = str(out / 'cycles-test.png')
start = time.monotonic()
try:
    bpy.ops.render.render(write_still=True)
except RuntimeError:
    scene.cycles.device = 'CPU'
    bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out / 'bpy-test.blend'))
(out / 'blender.json').write_text(json.dumps({'version': bpy.app.version_string, 'platform': platform.platform(), 'devices': devices, 'render_device': scene.cycles.device, 'seconds': time.monotonic()-start, 'image': 'cycles-test.png', 'saved_blend': 'bpy-test.blend'}, indent=2))
