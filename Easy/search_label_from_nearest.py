#%%
import typing as t
import numpy as np
import numpy.typing as npt
import linque as lq
from . import TpO3d

def search_label_from_nearest(ptsLabel: npt.NDArray[np.float32], labels: npt.NDArray[np.int8], pts: npt.NDArray[np.float32], distanceLimit: t.Optional[float] = None)->npt.NDArray[np.int8]:
    """ 從 1 個現有的 point cloud with label 作參考，找出 pts 的 label 流程，漸漸常被使用，所以重構一下

    Args:
        ptsLabel (_type_): 被參考的點雲
        labels (_type_): 被參考的 labels (int8)
        pts (_type_): 還沒有 labels 的點雲
        distanceLimit (_type_, optional): 當被參考的點雲的點，與 pts 他們座標是完全一樣時，可以用這個. Defaults to None.

    Returns:
        _type_: labels of pts。
    """
    pc = TpO3d.PointCloud()
    pc.points = TpO3d.Vector3dVector(ptsLabel)

    kdtree = TpO3d.KDTreeFlann(pc)
    def search(isExportDistance):
        # kdtree 搜尋最近並距離
        knn_results = [kdtree.search_knn_vector_3d(a1,1) for a1 in pts]
        idx3 = np.array([a1[1][0] for a1 in knn_results]) # [1] 是 indexs, [0] 是因為我們只取第1個
        distanceResult = np.array( [a1[2][0] for a1 in knn_results] ) if isExportDistance else None # 距離
        return idx3, distanceResult

    # 方法1，沒有限制最近點距離 (直覺作法)，但是在 141 Rhino 加底那個必須限制，為了那個，才會有方法 2
    if distanceLimit == None:
        idx3, _ = search(False)
        labelsResult = labels[idx3]
    else:
        # 無法只用最近點，因為可能會有錯。(請看成果9報告)，因此若距離=0，才是，若不是，則設為0
        # 首先，先找一個為 0 的 index
        r1First = lq.linq( enumerate(labels) ).first(lambda a1: a1[1] == 0)
        idxFirstZero = r1First[0]

        # kdtree 搜尋最近並距離
        idx3, distanceResult = search(True)

        # 若距離 > 0 的 idx3 就設為 idxFirstZero
        idx3[distanceResult > distanceLimit] = idxFirstZero

        # 新 labels 就出來了
        labelsResult = labels[idx3]
    return labelsResult