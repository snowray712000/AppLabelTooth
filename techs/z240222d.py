# 確認資料用 STL 
#%%
from add_parent_dir_to_sys_path import add_parent_dir_to_sys_path
add_parent_dir_to_sys_path()
from Easy import *

path = "./../CrownSegmentationNew/1/upper_mod.stl"
path = "./../Rhino補底/Rhino補底.stl"
with open(path,"rb") as file:
    mesh = readStlBinary_ToO3dMesh(file)

# easyo3d.render(mesh)

pc = TpO3d.PointCloud()
pc.points = mesh.vertices
pc.normals = mesh.vertex_normals
easyo3d.render(pc)