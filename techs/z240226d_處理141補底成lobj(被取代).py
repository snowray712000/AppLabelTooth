"""
# 將庭凱產生的 141 底的資料，整理為 .lobj
# 關鍵演算法，已經實驗過，現在是串流程。
# 相關實驗 240223b_觀察141補底.py

# 被取代，由 `z240228b_處理141補底成lobj_底3層排除法`
"""

#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 庭凱_141資料補底, 列舉檔案 ./../../庭凱_141資料補底/*.stl

import glob
import os

path1 = glob.glob('./../../庭凱_141資料補底/*/*.stl',recursive=True)
# print(path1[0]) # ./../../庭凱_141資料補底\0\re_0_lower_model_230915_100_epoch.stl

# path, id, upperlower
def fnSelectPath(path:str)->t.Tuple[str,int,str]:
    # print(path)
    r1 = os.path.realpath( os.path.abspath(path) )
    r2 = os.path.split(r1)
    r3 = os.path.split(r2[0])
    
    # id
    idd = int(r3[1])
    
    # upperlower
    upperlower = 'upper' if 'upper' in r2[1] else 'lower'
    return r1, idd, upperlower

stlInfos = lq.linq(path1).select(fnSelectPath).to_list()

#%
# 取得產生過程，沒成功產生的。(就會與原始資料一樣，因此不要產生)

txt1 = glob.glob('./../../庭凱_141資料補底/*/*.txt',recursive=True)
errorInfos = lq.linq(txt1).select(fnSelectPath).to_list()

#%
# filter error
def fnIsCorrect(a1):
    path, idd, upperlower = a1
    return False == lq.linq(errorInfos).any(lambda x: x[1]==idd and x[2]==upperlower)
    
stlInfos2 = lq.linq(stlInfos).where(fnIsCorrect).to_list()

#%
# 取得 ground truth of 141
from enumSrcDataLObjSorted import enumSrcDataLObjSorted4
groundTruthInfos = enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',upperlower='upper', isOnlyLastVersion=True)
groundTruthInfos.extend(enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',upperlower='lower', isOnlyLastVersion=True))

#%
# 試作其中一個
path1, idd1, upperlower1 = stlInfos2[0]

# 讀取
with open(path1, 'rb') as f:
    mesh1 = readStlBinary_ToO3dMesh(f)

# ground truth
groundTruthInfo1 = lq.linq(groundTruthInfos).first(lambda x: x[1]==idd1 and x[3]==upperlower1, None)

if groundTruthInfo1 is not None:
    path2, idd2, _, upperlower2 = groundTruthInfo1
    lobj2 = LabeledObject().read(path2)
    
    # kdtree
    pc = TpO3d.PointCloud()
    pc.points = TpO3d.Vector3dVector(lobj2[0])
    kdtree = TpO3d.KDTreeFlann(pc)
    
    # vertex of mesh1 to nearest vertex of mesh2
    
    labels2 = lobj2[3]
    # 無法只用最近點，因為可能會有錯。(請看成果9報告)，因此若距離=0，才是，若不是，則設為0
    # 首先，先找一個為 0 的 index
    r1First = lq.linq( enumerate(labels2) ).first(lambda a1: a1[1] == 0)
    idxFirstZero = r1First[0]

    # kdtree 搜尋最近並距離
    knn_results = [kdtree.search_knn_vector_3d(a1,1) for a1 in mesh1.vertices]
    idx3 = np.array([a1[1][0] for a1 in knn_results]) # [1] 是 indexs, [0] 是因為我們只取第1個
    distanceResult = np.array( [a1[2][0] for a1 in knn_results] ) # 距離

    # 若距離 > 0 的 idx3 就設為 idxFirstZero
    idx3[distanceResult > 0] = idxFirstZero

    # 新 labels 就出來了
    labelsResult = labels2[idx3]
    
    # 檔名 ... idd + 10000, 以示區別
    filename = f'{idd1 + 10000}_{upperlower1}.lobj'
    pathOutput = os.path.join(os.path.split(path2)[0], filename)
    
    # 輸出 lobj1
    lobj1 = (np.array(mesh1.vertices), None, None, labelsResult, None, np.array( mesh1.triangles ), None)
    LabeledObject().saveVsLsTris(path=pathOutput, vertexs=lobj1[0], labels=lobj1[3], triangles=lobj1[5])
    
    # 試畫 okay
    # mesh1 = easyo3d.toMesh2(lobj1, isDoSop=True)
    # easyo3d.render(mesh1)
    # easyo3d.render(easyo3d.toMesh2(lobj2))

#%
# 試載入 output Path 並繪圖
lobj = LabeledObject().read(pathOutput)
mesh = easyo3d.toMesh2(lobj, isDoSop=True)
easyo3d.render(mesh)

#%%
# for loop 作所有

for path1, idd1, upperlower1 in stlInfos2:
    # 讀取
    with open(path1, 'rb') as f:
        mesh1 = readStlBinary_ToO3dMesh(f)

    # ground truth
    groundTruthInfo1 = lq.linq(groundTruthInfos).first(lambda x: x[1]==idd1 and x[3]==upperlower1, None)
    
    if groundTruthInfo1 is None:
        print(f'groundTruthInfo1 is None, idd1={idd1}, upperlower1={upperlower1}')
        continue
    else:
        path2, idd2, _, upperlower2 = groundTruthInfo1
        lobj2 = LabeledObject().read(path2)

        # kdtree
        pc = TpO3d.PointCloud()
        pc.points = TpO3d.Vector3dVector(lobj2[0])
        kdtree = TpO3d.KDTreeFlann(pc)

        # vertex of mesh1 to nearest vertex of mesh2

        labels2 = lobj2[3]
        # 無法只用最近點，因為可能會有錯。(請看成果9報告)，因此若距離=0，才是，若不是，則設為0
        # 首先，先找一個為 0 的 index
        r1First = lq.linq( enumerate(labels2) ).first(lambda a1: a1[1] == 0)
        idxFirstZero = r1First[0]

        # kdtree 搜尋最近並距離
        knn_results = [kdtree.search_knn_vector_3d(a1,1) for a1 in mesh1.vertices]
        idx3 = np.array([a1[1][0] for a1 in knn_results]) # [1] 是 indexs, [0] 是因為我們只取第1個
        distanceResult = np.array( [a1[2][0] for a1 in knn_results] ) # 距離

        # 若距離 > 0 的 idx3 就設為 idxFirstZero
        idx3[distanceResult > 0] = idxFirstZero

        # 新 labels 就出來了
        labelsResult = labels2[idx3]
        
        # 檔名 ... idd + 10000, 以示區別
        filename = f'{idd1 + 10000}_{upperlower1}.lobj'
        pathOutput = os.path.join(os.path.split(path2)[0], filename)
        
        # 輸出 lobj1
        lobj1 = (np.array(mesh1.vertices), None, None, labelsResult, None, np.array( mesh1.triangles ), None)
        LabeledObject().saveVsLsTris(path=pathOutput, vertexs=lobj1[0], labels=lobj1[3], triangles=lobj1[5])
        
        print(f'succee to {idd1} {upperlower1}')