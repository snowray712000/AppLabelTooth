'''
將 231219 主程式，加入這個功能前，先以小程式來測試，確認後再加入。
'''
#%%
import numpy as np
import numpy.typing as npt
import Easy.TpO3d as TpO3d
def set_nolabel_to_nearest_label(lobj):
    v1: npt.NDArray[np.float32] = lobj[0]
    l1: npt.NDArray[np.int8]  = lobj[3]
    
    # 取得有標籤的點雲，並建立KDTree
    idx1 = l1 != -1
    v2 = v1[idx1]
    l2 = l1[idx1] # 後面會用到
    pc = TpO3d.PointCloud()
    pc.points = TpO3d.Vector3dVector(v2)
    kdtree = TpO3d.KDTreeFlann(pc) # 後面會用到
    
    # 取得沒有標籤的點雲，並找出最近的標籤
    idx2 = l1 == -1
    v3 = v1[idx2]
    if len(v3) != 0:
        idx3 = np.array([kdtree.search_knn_vector_3d(a1,1)[1][0] for a1 in v3])        
        l1[idx2] = l2[idx3] # 完成
    
    # 驗證
    # from Easy.easyopen3d import easyo3d
    # easyo3d.render(easyo3d.toMesh2(lobj))

path = 'I:/透明牙套_熱壓成型_後處理/Crown_Result/re_240103a_lower_104.lobj'
from Easy.LabeledObject import LabeledObject
lobj = LabeledObject().read(path)
set_nolabel_to_nearest_label(lobj)