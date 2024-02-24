from add_parent_dir_to_sys_path import add_parent_dir_to_sys_path
add_parent_dir_to_sys_path()

# 測試 
import Easy.TpO3d as TpO3d
from Easy.LabeledObject import LabeledObject
from Easy.ColorsForCrown import labels_to_colors_crown
from Easy.easyopen3d import easyo3d
path = "./../CrownSegmentationNew_SrcDataLObj/142_Template12_upper_Stage2_step4_14191_Tarek, Steiner_fixed_2.lobj"
lobj = LabeledObject().read(path)

pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector (  lobj[0]  )
pc.colors = TpO3d.Vector3dVector (  labels_to_colors_crown(lobj[3])  )
easyo3d.render(pc)

