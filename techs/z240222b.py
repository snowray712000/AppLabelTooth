# 231219 中，讀 stl 後，要轉成 mesh 用的。


#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

path = "./../CrownSegmentationNew/1/upper_mod.stl"
path = "./../庭凱測試結果/測試AI_20231020/case1_lower/Template1-0_lower_Stage1_step0_0629_Nicky.stl"
with open(path,"rb") as file:
    mesh = readStlBinary_ToO3dMesh(file)

easyo3d.render(mesh)