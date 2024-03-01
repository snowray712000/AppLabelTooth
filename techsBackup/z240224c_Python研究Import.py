""" 研究 Python 的 import 機制, Import Parent Dir """

#%%
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

# 測試 
path = "./../CrownSegmentationNew_SrcDataLObj/142_Template12_upper_Stage2_step4_14191_Tarek, Steiner_fixed_2.lobj"
lobj = LabeledObject().read(path)
# 注意! 路徑仍然可以相對於 Parent 上一層，加了第2行後

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector (  lobj[0]  )
pc.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(lobj[3])  )
easyo3d.render(pc)

