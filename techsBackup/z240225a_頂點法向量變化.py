""" 目的：當 stl 有底的時候，要切到哪裡
關鍵是判斷牙齒 Z 大概是多少

open3d 沒有曲率，而 TriangleMesh 只能自己算
這文件，嘗試算 TriangleMesh 的 相鄰，Normal，
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 列舉 141 筆資料
from Easy.enumSrcDataLObjSorted import enumSrcDataLObjSorted4
r1 = enumSrcDataLObjSorted4()
print(r1[0:2])

#%%
pathObj, _, _, _ = r1[-1]
lobj = LabeledObject().read(pathObj)
points = lobj[0]
labels = lobj[3]
triangles = lobj[5]

mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj, isDoSop=True)
# easyo3d.render(mesh)
#%%
# 相鄰 函式 理解。 這裡相鄰，指的是 vertices 的
mesh.compute_adjacency_list() # mesh.adjacency_list
# print( list(mesh.adjacency_list[0]) ) # [1, 2, 3, 7]

## 驗證理解
# 0 與 1, 2, 3, 7 相鄰 (當你取得[1]時，就會得到 0，取[4]，就不會有0)
# 驗證上述所而
# print( list(mesh.adjacency_list[1]) ) # [0, 2, 4, 7, 8, 9] ... 的確有 0
# print( list(mesh.adjacency_list[4]) ) # [1, 2, 5, 9, 12, 21] ... 的確沒有 0

# 轉為 dict
dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}

#%%
# 計算每個頂點，與相鄰頂點的法向量 dot，並選出最小的 (表示變化最大)
# 我嘗試平行處理了，但時間反而較久，從 3 秒多，變成 13秒多

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
# 畫出來看看，頂點的 min_dots 小於 0.5 的

idxs = np.array(min_dots) < 0.95

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points[idxs])

easyo3d.render(pc)

#%%