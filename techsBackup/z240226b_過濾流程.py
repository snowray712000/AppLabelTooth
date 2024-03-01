"""整合進 ui 前，先試作"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%
path1 = 'd:\\coding\\透明牙套\\CrownSegmentationNew_SrcDataLObj\\146_Template1-0_lower_Stage1_step0_1026_Demo2_fixed_5.lobj'
path2 = 'd:\\coding\\透明牙套\\CrownSegmentationNew_SrcDataLObj\\146_Template1-0_upper_Stage1_step0_1026_Demo2_fixed_3.lobj'
path3 = 'd:\\coding\\透明牙套\\CrownSegmentationNew_SrcDataLObj\\0_lower.lobj'
path4 = 'd:\\coding\\透明牙套\\CrownSegmentationNew_SrcDataLObj\\0_upper.lobj'
case = 3
if case == 0:
    pathlobj = path1
    upperlower = 'lower'
elif case == 1:
    pathlobj = path2
    upperlower = 'upper'
elif case == 2:
    pathlobj = path3
    upperlower = 'lower'
else:
    pathlobj = path4
    upperlower = 'upper'
    
lobj = LabeledObject().read(pathlobj)
points = lobj[0]
labels = lobj[3]
triangles = lobj[5]
mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj, isDoSop=True)
easyo3d.render(mesh)

#%%
# 先確定，是否含底部
z = points[:, 2]
zmin = np.min(z)
zmax = np.max(z)
height = zmax - zmin #

def isHasBottom():
    if upperlower == 'lower':
        return np.sum( z == zmin ) > 50 # 通常 200 個以上 
    else:
        return np.sum( z == zmax ) > 50
if isHasBottom() == False:
    # 產生一個 len(points) 長度的 True
    idxs = np.array([True] * len(points))
else:
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

#%
# 測試 idxs
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points[idxs])
pc.colors = TpO3d.Vector3dVector(labels_to_colors_crown(labels[idxs]))
easyo3d.render(pc)



