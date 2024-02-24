# 231219 中，取得 infer result 後的處理

#%%
from add_parent_dir_to_sys_path import add_parent_dir_to_sys_path
add_parent_dir_to_sys_path()
from Easy import *

text = """1.2,1.3,1.2,0.0
1.3,2.3,-12.2,1.0"""

r1 = text.split("\n")
pts = np.array( [[float(a2) for a2 in x.split(" ")[:3]] for x in r1], dtype=np.float32)
labels = np.array( [float(x.split(" ")[-1]) for x in r1], dtype=np.int8 )
print(pts)
print(labels)