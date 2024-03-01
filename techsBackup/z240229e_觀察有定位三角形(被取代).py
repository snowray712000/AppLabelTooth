"""
觀察有中間物體的，原本 `自動腰斬高度` 演算法結果會如何
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

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
# pc.normals = mesh.vertex_normals
easyo3d.render(pc)

#%
# 取得計算標準差的頂點 index
def get_idx_of_vertex_for_calc_avg_std_z(lobj, upperlower, mesh:TpO3d.TriangleMesh):
    assert ( mesh.has_vertex_normals() )
    
    # 建相鄰，約1秒
    if mesh.has_adjacency_list() == False:
        mesh.compute_adjacency_list() 
    dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}
    
    # 2個算法，共用資料(提升效率，只作一次)
    z = lobj[0][:, 2]
    normals = np.array(mesh.vertex_normals)
    
    zlimit = np.min(z) if upperlower == 'lower' else np.max(z)
    
    def get_exclude_bottom_idx():
        idxs = z == zlimit
        idxs1 = np.arange(len(z))[idxs] # [T T F F T] -> [0 1 4]
        idxs2 = lq.linq(idxs1).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
        idxs13 = lq.linq(idxs2).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
        idxs123 = list(set(idxs13 + idxs2))
        re = np.full(len(z), True)
        re[idxs123] = False
        return re
    def get_normal_change_big_idx():
        min_dots: t.List[float] = []
        for i in range(len(lobj[0])):
            # 取得相鄰頂點的法向量
            normals2 = np.array([normals[i] for i in dict_adjacency[i]])
            # 計算 dot
            dots = np.dot(normals2, normals[i])
            # 取得最小的
            min_dot = np.min(dots)
            min_dots.append(min_dot)
        re = np.array(min_dots) < 0.95
        return re
    
    return get_exclude_bottom_idx() & get_normal_change_big_idx()

idxs = get_idx_of_vertex_for_calc_avg_std_z(lobj, upperlower, mesh)
#%
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(lobj[0][idxs])
easyo3d.render(pc)

#%
z = lobj[0][:, 2]
z2 = z[idxs]
avg, std = np.mean(z2), np.std(z2)
print(avg, std)
idxsExcludeOutlier = z > (avg - 3 * std) if upperlower == 'lower' else z < (avg + 3 * std)

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(lobj[0][idxsExcludeOutlier])
easyo3d.render(pc)