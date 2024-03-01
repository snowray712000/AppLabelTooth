""" 實驗，預測目前是整個 STL，但會包含到底部，應該要把底部去掉，但有簡單的方法，就是
先取得STL整個的高度，然後再取全部高度的 0.05，以下，就拿掉 %"""

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
points = lobj[0]
labels = lobj[3]

# 判斷是 lower 還是 upper，首先，先取得，將 path 取出 filename，再判斷 name 中有 lower 或 upper 嗎
filename = os.path.basename(path)
isUpper = "upper" in filename

# 取得 vertex 最大最小值 lobj[0]
minMaxZ = (np.min(points[:,2]), np.max(points[:,2]))
height = minMaxZ[1] - minMaxZ[0]

# 取得 5% 的高度
h5 = height * 0.05

# 下顎，太低，不要；上顎，太高，不要
if isUpper:
    zLimit = minMaxZ[1] - h5
    idx = points[:,2] < zLimit
else:
    zLimit = minMaxZ[0] + h5
    idx = points[:,2] > zLimit

# 取出過濾後的點    
points2 = points[idx]
labels2 = labels[idx]

# 觀察
pcOriginal = TpO3d.PointCloud()
pcOriginal.points = TpO3d.Vector3dVector (  points  )
pcOriginal.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(labels)  )

pcLimit = TpO3d.PointCloud()
pcLimit.points = TpO3d.Vector3dVector (  points2  )
pcLimit.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(labels2)  )

easyo3d.render(pcOriginal)
easyo3d.render(pcLimit)