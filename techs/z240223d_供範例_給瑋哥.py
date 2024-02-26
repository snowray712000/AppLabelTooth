"""
評估可行。產生範例給瑋哥。
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

path = "./../CrownSegmentationNew_SrcDataLObj/142_Template12_upper_Stage2_step4_14191_Tarek, Steiner_fixed_2.lobj"
lobj = LabeledObject().read(path)

mesh = easyo3d.toMesh(lobj[0], lobj[5], None, isDoSop=True)
easyo3d.render(mesh)

# 產生 point cloud
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(lobj[0])
pc.colors = TpO3d.Vector3dVector(labels_to_colors_crown(lobj[3]))
easyo3d.render(pc)

# 結果
mesh = easyo3d.toMesh2(lobj, isDoSop=True)
easyo3d.render(mesh)