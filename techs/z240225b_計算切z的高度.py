""" 目的：當 stl 有底的時候，要切到哪裡
關鍵是判斷牙齒 Z 大概是多少

open3d 沒有曲率，而 TriangleMesh 只能自己算
這文件，嘗試算 TriangleMesh 的 相鄰，Normal，
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

# 列舉 141 筆資料
from enumSrcDataLObjSorted import enumSrcDataLObjSorted4
r1 = enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',
                            upperlower='lower',
                            isOnlyLastVersion=True)
r1b = enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',upperlower='upper',isOnlyLastVersion=True)
r1.extend(r1b)

#%%
# 前處理其中一筆作測試
r1a = lq.linq(r1).where(lambda x: x[3] == 'upper').to_list()
pathObj, _, _, upperlower = r1a[-1]
lobj = LabeledObject().read(pathObj)
points = lobj[0]
labels = lobj[3]
triangles = lobj[5]

mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj, isDoSop=True)
# easyo3d.render(mesh)

# 相鄰 函式 理解。 這裡相鄰，指的是 vertices 的
mesh.compute_adjacency_list() # mesh.adjacency_list
# 轉為 dict
dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}

# 計算每個頂點，與相鄰頂點的法向量 dot，並選出最小的 (表示變化最大)
min_dots: t.List[float] = []
for i in range(len(points)):
    # 取得相鄰頂點的法向量
    normals = np.array([mesh.vertex_normals[i] for i in dict_adjacency[i]])
    # 計算 dot
    dots = np.dot(normals, mesh.vertex_normals[i])
    
    # 取得最小的
    min_dot = np.min(dots)
    min_dots.append(min_dot)

#%%
# dot < 0.95，並且取得 z 的 avg std
idxs = np.array(min_dots) < 0.95
points2 = points[idxs]

## 觀察
# pc = TpO3d.PointCloud()
# pc.points = TpO3d.Vector3dVector(points2)
# easyo3d.render(pc)

# 不可等於 zmin zmax 
z = points[:, 2]
zmin = np.min(z)
zmax = np.max(z)
height = zmax - zmin

z = points2[:, 2]
if upperlower == 'upper':
    idxs2 = z < (zmax - 0.1 * height)
else:
    idxs2 = z > (zmin + 0.1 * height)

## 觀察
# pc = TpO3d.PointCloud()
# pc.points = TpO3d.Vector3dVector(points2[idxs2])
# easyo3d.render(pc)

# 計算 z 的 avg std
z = points2[idxs2, 2]
avg, std = np.mean(z), np.std(z)

#%
if upperlower == 'upper':
    idxs = points[:, 2] < avg + 3 * std
else:
    idxs = points[:, 2] > avg - 3 * std

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points[idxs])
easyo3d.render(pc)