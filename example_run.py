import json
import numpy as np
from vtk_tools import VTK_writer

with open('./test_data/example.json', 'r') as f:
    data = json.load(f)


nodes = np.array(data["nodes"])[:, 1:]
elements = np.array(data["elements"])
disp = np.array(data["displacement"])
vel = np.array(data["velocity"])
mat_id = np.array(data["material_ID"])
mat = np.array(data["material_value"])

for i in range(10):
    vtk = VTK_writer.Write('./output', file_name=f"data_{str(i)}", write_binary=True)
    vtk.add_mesh(nodes, elements, "hexa8")
    vtk.add_vector("displacement", disp)
    vtk.add_vector("velocity", vel, header=False)
    vtk.add_scalar("ID", mat_id)
    vtk.add_scalar("mat", mat, header=False)
    vtk.save()
