# 確認資料用 STL 
from Easy.readSTL import readStlBinary_ToO3dMesh
from Easy.easyopen3d import easyo3d
import Easy.TpO3d as TpO3d
path = "./../CrownSegmentationNew/1/upper_mod.stl"
path = "./../Rhino補底/Rhino補底.stl"
with open(path,"rb") as file:
    mesh = readStlBinary_ToO3dMesh(file)

# easyo3d.render(mesh)

pc = TpO3d.PointCloud()
pc.points = mesh.vertices
pc.normals = mesh.vertex_normals
easyo3d.render(pc)