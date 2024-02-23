'''
231219 中當 Infer 後，也將 text 轉為 numpy，有 vertex, 有 labels 了
將現有的 mesh (從 stl 來的)，加入 labels 顏色


'''

path = './../Crown_Result/re_240103a_lower_40.lobj'
from Easy.LabeledObject import LabeledObject
lobj = LabeledObject().read(path)

pts = lobj[0]
normals = lobj[1]
labels = lobj[3]
triangles = lobj[5]

# 假設有 mesh，但還沒有 labels
import Easy.TpO3d as TpO3d
from Easy.easyopen3d import easyo3d
import numpy as np
mesh = easyo3d.toMesh(pts, triangles, None, isDoSop=True)
easyo3d.render(mesh)

# 假設得到 pts, labels

# 建 kdtree & 找最近點
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(pts)
kdtree = TpO3d.KDTreeFlann(pc)

idx3 = np.array([kdtree.search_knn_vector_3d(a1,1)[1][0] for a1 in mesh.vertices]) 

# new labelobject
ptsSTL = np.array(mesh.vertices)
triSTL = np.array(mesh.triangles)
mesh2 = easyo3d.toMesh(pts, triangles, labels[idx3], isDoSop=True)

easyo3d.render(mesh2)

# new lobj
lobj2 = (pts, None, None, labels[idx3], None, triangles, None)