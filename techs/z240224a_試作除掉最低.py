""" 實驗，預測目前是整個 STL，但會包含到底部，應該要把底部去掉，但有簡單的方法，就是 != 最高或最低"""

#%%
# 必須先加入，不然會找不到套件，放在最下面
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

# 載入一個含底的作為測試
path = "./../CrownSegmentationNew_SrcDataLObj/142_Template12_upper_Stage2_step4_14191_Tarek, Steiner_fixed_2.lobj"
path = r"./../CrownSegmentationNew_SrcDataLObj/143_Template1-0_lower_Stage1_step0_14191_Tarek, Steiner_fixed_1.lobj"
# path = "./../CrownSegmentationNew_SrcDataLObj/0_upper.lobj"
# path = "./../CrownSegmentationNew_SrcDataLObj/0_lower.lobj"
lobj = LabeledObject().read(path)
mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj)
points = lobj[0]
labels = lobj[3]
normals= np.array( mesh.vertex_normals )


# 判斷是 lower 還是 upper，首先，先取得，將 path 取出 filename，再判斷 name 中有 lower 或 upper 嗎
filename = os.path.basename(path)
isUpper = "upper" in filename

# 取得 vertex 最大最小值 lobj[0]
minMaxZ = (np.min(points[:,2]), np.max(points[:,2]))
height = minMaxZ[1] - minMaxZ[0]

# 取得 5% 的高度
h5 = height * 0.05

# 下顎，z 必須 > 最小 z；上顎，z 必須 < 最大 z
if isUpper:
    idx = points[:,2] < minMaxZ[1]
else:
    idx = points[:,2] > minMaxZ[0]

# 取出過濾後的點    
points2 = points[idx]
labels2 = labels[idx]
normals2 = normals[idx]

# 觀察
pcOriginal = TpO3d.PointCloud()
pcOriginal.points = TpO3d.Vector3dVector (  points  )
pcOriginal.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(labels)  )
pcOriginal.normals = TpO3d.Vector3dVector (  normals  )

pcLimit = TpO3d.PointCloud()
pcLimit.points = TpO3d.Vector3dVector (  points2  )
pcLimit.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(labels2)  )
pcLimit.normals = TpO3d.Vector3dVector (  normals2  )

easyo3d.render(pcOriginal)
easyo3d.render(pcLimit)