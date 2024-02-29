"""
為了加入新功能 _ label 從現有 .pts 檔案讀取
這裡先試作流程
"""
#%%
# import 並 載入資料路徑
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 假設已經有 .pts 同檔名, 不同副檔名
dir = r"D:\coding\透明牙套\瑋哥_試轉資料b"
path = os.path.join(dir, "Template1-0_upper_Stage1_step0_0629_Nicky.stl")

with open(path, 'rb') as f:
    mesh = readStlBinary_ToO3dMesh(f)

points = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
lobj = (points, None, None, None, None, triangles, None)

#%%
# 模擬按下時的效果
pathPts = os.path.splitext(path)[0] + ".pts"

# 確認檔案存在嗎
if os.path.exists(pathPts) == False:
    # 檔案不存在
    pass
else:
    with open(pathPts, 'r') as f:
        lines = f.readlines()
        
        # , 隔開, x,y,z,label
        xyzs = np.array( [[float(a2) for a2 in a1.split(",")[:3]] for a1 in lines] )
        labels = np.array( [float(a1.split(",")[-1]) for a1 in lines] , dtype=np.int8 )
        
        labels[labels == -1] = 0
        
        # 搜尋最近點
        pc = TpO3d.PointCloud()
        pc.points = TpO3d.Vector3dVector(xyzs)
        
        kdtree = TpO3d.KDTreeFlann(pc)
        
        labels2 = labels
        points1 = lobj[0]
        # 無法只用最近點，因為可能會有錯。(請看成果9報告)，因此若距離=0，才是，若不是，則設為0
        # 首先，先找一個為 0 的 index
        r1First = lq.linq( enumerate(labels2) ).first(lambda a1: a1[1] == 0)
        idxFirstZero = r1First[0]

        # kdtree 搜尋最近並距離
        knn_results = [kdtree.search_knn_vector_3d(a1,1) for a1 in points1]
        idx3 = np.array([a1[1][0] for a1 in knn_results]) # [1] 是 indexs, [0] 是因為我們只取第1個
        distanceResult = np.array( [a1[2][0] for a1 in knn_results] ) # 距離

        # 若距離 > 0 的 idx3 就設為 idxFirstZero
        # idx3[distanceResult > 0] = idxFirstZero

        # 新 labels 就出來了
        labelsResult = labels2[idx3]
        
        lobj = (points, None, None, labelsResult, None, triangles, None)
        mesh = easyo3d.toMesh2(lobj)
        easyo3d.render(mesh)
        