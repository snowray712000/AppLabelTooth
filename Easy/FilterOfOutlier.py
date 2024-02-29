#%%
import typing as t
import numpy as np
import numpy.typing as npt
import linque as lq
from . import TpO3d

class FilterOfOutlier:
    """ 使用法向量變化大，作為牙齒的初步判斷，再依牙的高度，取合適的高度
    - Notes:
        - 法向量是垂直或水平的，會拿掉
        - 邊緣的頂點 3 層內，會拿掉
        - 法向量 dot 大於 0.95 (變化太少)，會拿掉
        - 用上面得到的少數點，計算 z 的 avg std。
        - 使用 z of p > avg - 3 * std, 作為最後的結果 (lower)
        - 使用 z of p < avg + 3 * std, 作為最後的結果 (upper)
    """
    def __init__(self):
        self._z = None # 算一次就夠了，提升效率
        self._zlimit = None
        self._normals = None
    def __del__(self):
        del self._z
        del self._zlimit
        del self._normals

    def main(self,lobj,upperlower: t.Literal['upper','lower'],mesh: TpO3d.TriangleMesh)->npt.NDArray[np.bool8]:
        self._z = lobj[0][:, 2]
        self._zlimit = np.min(self._z) if upperlower == 'lower' else np.max(self._z)
        self._normals = np.array(mesh.vertex_normals)

        idxs = self._get_idx_of_vertex_for_calc_avg_std_z(lobj, upperlower, mesh)
        idxs2 = self._get_filter_index(idxs, upperlower)
        
        return idxs2
    def _get_idx_of_vertex_for_calc_avg_std_z(self,lobj, upperlower, mesh:TpO3d.TriangleMesh):
        assert ( mesh.has_vertex_normals() )

        # 建相鄰，約1秒
        if mesh.has_adjacency_list() == False:
            mesh.compute_adjacency_list()
        dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}

        # 2個算法，共用資料(提升效率，只作一次)
        z = self._z
        zlimit = self._zlimit
        normals = self._normals
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
        def get_excludes_z_ortho():
            normalsPlane = np.array(mesh.triangle_normals)
            idxPlane1 = (normalsPlane[:, 2] == 0) | (normalsPlane[:, 2] == 1) | (normalsPlane[:, 2] == -1)
            triangles2 = np.array(mesh.triangles)[idxPlane1]

            # triangles2 is shape(N,3) int32, 將所有頂點 index 集合起來
            index3 = np.unique( triangles2.flatten() )
            # [1,2,4] -> [F T T F T F F F]
            indexResult = np.full(len(z), False)
            indexResult[index3] = True
            return ~indexResult

            # 直接用 vertex normals 是不足夠的 
            # return ~((normals[:,2] == 0) | (normals[:,2] == 1) | (normals[:,2] == -1))
        return get_exclude_bottom_idx() & get_normal_change_big_idx() & get_excludes_z_ortho()
        
    # 取得計算標準差的頂點 index
    def _get_filter_index(self, idxs, upperlower: t.Literal['upper','lower'] = 'lower'):
        #% 看圖, 用來計算的那些點
        # pc = TpO3d.PointCloud()
        # pc.points = TpO3d.Vector3dVector(lobj[0][idxs])
        # easyo3d.render(pc)

        #% 
        z = self._z
        z2 = z[idxs]
        avg, std = np.mean(z2), np.std(z2)
        # print(avg, std)

        idxsExcludeOutlier = z > (avg - 3 * std) if upperlower == 'lower' else z < (avg + 3 * std)

        # # 看結果，就是拿這些去預測
        # pc = TpO3d.PointCloud()
        # pc.points = TpO3d.Vector3dVector(lobj[0][idxsExcludeOutlier])
        # easyo3d.render(pc)

        # # 看結果，這些點是透過這個演算法，排除掉的
        # pc = TpO3d.PointCloud()
        # pc.points = TpO3d.Vector3dVector(lobj[0][~idxsExcludeOutlier])
        # easyo3d.render(pc)

        return idxsExcludeOutlier