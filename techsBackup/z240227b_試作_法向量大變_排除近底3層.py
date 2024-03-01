""" 目的：當 stl 有底的時候，要切到哪裡
關鍵是判斷牙齒 Z 大概是多少

計算 法向量變化 要排除底蓋，然而，直接移除 zmin zmax 還不足，因為相鄰的的點， Normal 變化量也會很大，所以，要再多取一層相鄰的點，再計算法向量變化量。因為頂點法向量，是相鄰網格計算，所以實際上，相鄰的法向量，其實也受低蓋影響，所以，按理應該取三層最合適。

此文件，就是驗證上述是否可行。
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

# 列舉 141 筆資料
from Easy.enumSrcDataLObjSorted import enumSrcDataLObjSorted4
r1 = enumSrcDataLObjSorted4()
#%%
# 前處理其中一筆作測試
r1a = lq.linq(r1).where(lambda x: x[3] == 'lower').to_list()
pathObj, _, _, upperlower = r1a[-3]
lobj = LabeledObject().read(pathObj)
points = lobj[0]
labels = lobj[3]
triangles = lobj[5]

mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj, isDoSop=True)
easyo3d.render(mesh)

# 相鄰 函式 理解。 這裡相鄰，指的是 vertices 的
mesh.compute_adjacency_list() # mesh.adjacency_list
# 轉為 dict
dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}

#%%
# 取得頂點接近底的點 3 層相鄰
def get_adj_of_bottom():
    z = points[:, 2]
    zlimit = np.min(z) if upperlower == 'lower' else np.max(z)
    idxs = z == zlimit
    idxs1 = np.arange(len(z))[idxs] # [T T F F T] -> [0 1 4]
    idxs2 = lq.linq(idxs1).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
    idxs13 = lq.linq(idxs2).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
    # 或許會困惑，從2找，應該只會找到1 與 3層，怎麼會包含自己呢？因為2之間彼此相鄰造成的，但也會有特例，是找不到自己的，所以仍然要加自己較保險
    idxs123 = list(set(idxs13 + idxs2))
    return idxs123
idxs123 = get_adj_of_bottom()

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points[idxs123])
easyo3d.render(pc)

#%%

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

idxsNormalChangedBig = np.array(min_dots) < 0.95

# [1 2 4] -> [T T F T] for idxs123

# 全都是 True， len(points) 個，再將 idxs123 改為 False
idxsNoIncludeBottom = np.full(len(points), True)
idxsNoIncludeBottom[idxs123] = False


points2 = points[idxsNormalChangedBig & idxsNoIncludeBottom]

## 觀察
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points2)
easyo3d.render(pc)
