import json
from techclappets.pressuredrop.line import roughness_material_list

allowed_materials = roughness_material_list()

print(json.dumps(allowed_materials))
