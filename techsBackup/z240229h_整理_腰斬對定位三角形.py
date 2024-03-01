"""
觀察有中間物體的，原本 `自動腰斬高度` 演算法結果會如何

這是要用在 InferBefore 的
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *
from Easy.FilterOfOutlier import FilterOfOutlier

#%%
pathSTL = './../../有底_且有中間的.stl'
with open(pathSTL, 'rb') as fp:
    mesh = readStlBinary_ToO3dMesh(fp)
upperlower = "lower"
points = np.array(mesh.vertices)
triangles = np.array(mesh.triangles)
lobj = toLobjTupleVTL(points, triangles)

easyo3d.render(mesh)

pc = TpO3d.PointCloud()
pc.points = mesh.vertices
easyo3d.render(pc)

#%%
idx = FilterOfOutlier().main(lobj, upperlower, mesh)
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(lobj[0][~idx])
easyo3d.render(pc)

pc.points = TpO3d.Vector3dVector(lobj[0][idx])
easyo3d.render(pc)
