"""Configuration is now the canonical editable input. This command validates it.
The rejected initial seed generator is preserved only in outputs/spatial-analysis.
"""
from pathlib import Path
import json
p=json.loads((Path(__file__).resolve().parents[1]/'config/scene-parameters.json').read_text())
assert p['geometry']['site_width_m']>0 and p['geometry']['site_depth_m']>0
assert len(p['geometry']['pool_outline_xy_m'])>=16
assert len(p['comparison_cameras'])==5
print('Configuration valid:',p['spatial_revision'],'; all lengths remain estimates')
