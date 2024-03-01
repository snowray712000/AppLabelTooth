# 驗證 自動高度演算法，在有底的 Case，不會切到 label 不為 0 的地方
# 取得 [T T F F] Label [1 1 1 0] 為例，第3個，也就是 False 的 Index 一定都要是 0，否則就是錯的。
# T 若對應到 0，沒關係，但 F 若對應到 1，就是錯的。
# 結論: 原流程好很多，改過的

#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%
# 取得所有 lobj info
from Easy.enumSrcDataLObjSorted import enumSrcDataLObjSorted4

lobjinfos = enumSrcDataLObjSorted4()

#%%
# 實驗其中一個
path, idd, _, upperlower = lobjinfos[-1]
lobj = LabeledObject().read(path)
mesh = easyo3d.toMesh2(lobj)
# easyo3d.render(mesh)

def filter_before_infer(mesh: TpO3d.TriangleMesh, lobj)->t.Optional[npt.NDArray[np.int32]]:
    """ 回傳 null 表示不用過濾，用所有的 """
    points = lobj[0]
    z = points[:, 2]
    zmin = np.min(z)
    zmax = np.max(z)
    height = zmax - zmin

    # 確認是否有底
    def isHasBottom():
        if upperlower == 'lower':
            return np.sum( z <= zmin + 0.01 * height ) > 30 # 通常 200 個以上 
        else:
            return np.sum( z >= zmax - 0.01 * height ) > 30
    if isHasBottom() == False:
        return None
    
    # 相鄰資訊
    mesh.compute_adjacency_list()
    dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}
    # 最大的法向量變化值
    def calc_dots_min():
        """7萬多當，約4秒"""
        min_dots: t.List[float] = []
        for i in range(len(points)):
            # 取得相鄰頂點的法向量
            normals = np.array([mesh.vertex_normals[i] for i in dict_adjacency[i]])
            # 計算 dot
            dots = np.dot(normals, mesh.vertex_normals[i])
            
            # 取得最小的
            min_dot = np.min(dots)
            min_dots.append(min_dot)
        return min_dots
    dots_min = calc_dots_min()
    
    # dot < 0.95，並且取得 z 的 avg std
    idxsA = np.array(dots_min) < 0.95
    points2 = points[idxsA]
    
    # z 不可取接近底部的
    z2 = points2[:, 2]
    if upperlower == 'upper':
        idxsB = z2 < (zmax - 0.1 * height)
    else:
        idxsB = z2 > (zmin + 0.1 * height)
    # 計算 z 的 avg std
    z3 = points2[idxsB, 2] # 去除掉接近底部的
    avg, std = np.mean(z3), np.std(z3)
    
    # 依 avg std，取得 idxs， avg + 3 std
    if upperlower == 'upper':
        idxs = points[:, 2] < avg + 3 * std
    else:
        idxs = points[:, 2] > avg - 3 * std
    return idxs

idxs = filter_before_infer(mesh, lobj)
#%
labels2 = lobj[3][idxs == False]

# 計算幾個 labels2 中不為 0 的
count = np.sum(labels2 != 0)
print(count) # 0 

#%%
# 驗證所有
infos2 = lq.linq(lobjinfos).sort(lambda x: (x[3],x[1])).to_list()
for path, idd, _, upperlower in infos2:
    lobj = LabeledObject().read(path)
    mesh = easyo3d.toMesh2(lobj)
    idxs = filter_before_infer(mesh, lobj)
    if idxs is None:
        # idd, upperlower, result
        print(idd, upperlower, 'No Bottom')
        continue
    labels2 = lobj[3][idxs == False]
    count = np.sum(labels2 != 0)
    
    print(idd, upperlower, 'ok' if count == 0 else 'ng', count)
    
#%%
# 處理某一個
path, idd, _, upperlower = lq.linq(lobjinfos).first(lambda x: x[1] == 10091 and x[3] == 'lower')

lobj = LabeledObject().read(path)
mesh = easyo3d.toMesh2(lobj)
easyo3d.render(mesh)

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector( lobj[0] )
pc.colors = TpO3d.Vector3dVector( labels_to_colors_crown(lobj[3]) )
easyo3d.render(pc)

z = lobj[0][:, 2]
zmin, zmax = np.min(z), np.max(z)
height = zmax - zmin
# 確認是否有底

if upperlower == 'lower':
    print ( np.sum( z <= zmin + 0.01 *height ) ) # 通常 200 個以上
else:
    print ( np.sum( z >= zmax - 0.01 *height) )