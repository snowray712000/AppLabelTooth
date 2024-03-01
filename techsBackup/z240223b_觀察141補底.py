""" 為了，預備整合 1-141 筆資料 Rhino 加底。
觀察 Rhino 補底資料 
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

path = "./../Rhino補底/Rhino補底.stl"
with open(path,"rb") as file:
    mesh = readStlBinary_ToO3dMesh(file)

# easyo3d.render(mesh)
pathXYZL = "./../CrownSegmentationNew_SrcDataLObj/0_lower.lobj"
lobj = LabeledObject().read(pathXYZL)
points = lobj[0]
labels = lobj[3]
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points)
kdtree = TpO3d.KDTreeFlann(pc)
meshGround = easyo3d.toMesh2(lobj, isDoSop=True)
easyo3d.render(meshGround)

# 無法只用最近點，因為可能會有錯。(請看成果9報告)，因此若距離=0，才是，若不是，則設為0
# 首先，先找一個為 0 的 index
r1First = lq.linq( enumerate(labels) ).first(lambda a1: a1[1] == 0)
idxFirstZero = r1First[0]

# kdtree 搜尋最近並距離
knn_results = [kdtree.search_knn_vector_3d(a1,1) for a1 in mesh.vertices]
idx3 = np.array([a1[1][0] for a1 in knn_results]) # [1] 是 indexs, [0] 是因為我們只取第1個
distanceResult = np.array( [a1[2][0] for a1 in knn_results] ) # 距離

# 若距離 > 0 的 idx3 就設為 idxFirstZero
idx3[distanceResult > 0] = idxFirstZero

# 新 labels 就出來了
labelsResult = labels[idx3]

# 觀察看看
lobj2 = (np.array(mesh.vertices), None, None, labelsResult, None, np.array( mesh.triangles ), None)

mesh2 = easyo3d.toMesh(lobj2[0], lobj2[5], lobj2[3], isDoSop=True)
easyo3d.render(mesh2)

pc2 = TpO3d.PointCloud()
pc2.points = TpO3d.Vector3dVector(lobj2[0])
pc2.colors = TpO3d.Vector3dVector(labels_to_colors_crown(lobj2[3]))
easyo3d.render(pc2)