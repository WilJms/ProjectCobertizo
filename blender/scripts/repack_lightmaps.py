"""Improve atlas utilization without rebuilding or changing authored geometry."""
import bpy, json, math, shutil
from pathlib import Path
R=Path(__file__).resolve().parents[2];master=R/'blender/patio_master.blend';shutil.copy2(master,R/'blender/history/patio_master_before_uv_repack.blend')
for name in json.loads(bpy.context.scene['receiver_ids']):
 o=bpy.data.objects[name];o.hide_set(False);bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;o.data.uv_layers.active_index=1
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(20 if 'FURNITURE' in name else 66),island_margin=.00025 if 'VEGETATION' in name else .001,margin_method='FRACTION',area_weight=.7,correct_aspect=True,scale_to_bounds=True);bpy.ops.object.mode_set(mode='OBJECT');o.data.uv_layers.active_index=0;o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=str(master))
