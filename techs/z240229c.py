"""
重構

為了加入新功能 _ label 從現有 .pts 檔案讀取
這裡先試作流程
"""
#%%
# import 並 載入資料路徑
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *
from Easy.search_label_from_nearest import search_label_from_nearest

#%%
# 假設已經有 .pts 同檔名, 不同副檔名
dir = r"D:\coding\透明牙套\瑋哥_試轉資料b"
path = os.path.join(dir, "Template1-0_upper_Stage1_step0_0629_Nicky.stl")

with open(path, 'rb') as f:
    mesh = readStlBinary_ToO3dMesh(f)

points = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)
lobj = (points, None, None, None, None, triangles, None)

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
        
        labelsResult = search_label_from_nearest(xyzs, labels, points, None)
        
        lobj = (points, None, None, labelsResult, None, triangles, None)
        mesh = easyo3d.toMesh2(lobj)
        easyo3d.render(mesh)
        