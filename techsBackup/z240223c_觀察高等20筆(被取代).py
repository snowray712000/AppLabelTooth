"""
評估可行。藉觀察 20 筆資料 (馬等)，是否這樣輸出可行
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

pathSTL = r"D:\coding\透明牙套\瑋歌試轉20筆OutputData\001_case1\2024-02-22-1520[Import]\2023-04-10-14-06\Template1-0_lower_Stage1_step0_001_case1.stl"
# path label 是 .stl 換成 .mgn
pathLabel = pathSTL.replace(".stl", ".mgn")

# 讀 text x,y,z,l
with open(pathLabel, "r") as file:
    lines = file.readlines()
    points = np.array( [[float(a) for a in line.split(",")[:3]] for line in lines], dtype=np.float32 )
    labels = np.array( [float(line.split(",")[-1]) for line in lines] ,dtype=np.int8 )

# 驗證讀檔
pc = TpO3d.PointCloud()
pc.points = TpO3d.Vector3dVector(points)
pc.colors = TpO3d.Vector3dVector(labels_to_colors_crown(labels))
easyo3d.render(pc)

# 讀 stl
with open(pathSTL,"rb") as file:
    mesh = readStlBinary_ToO3dMesh(file)

# 驗證讀檔    
easyo3d.render(mesh)
    
# 用 kdtree 將 label 資料對應到 stl
kdtree = TpO3d.KDTreeFlann(pc)
idx3 = np.array([kdtree.search_knn_vector_3d(a1,1)[1][0] for a1 in mesh.vertices])

# 結果 mesh
lobj2 = (np.array(mesh.vertices), None, None, labels[idx3], None, np.array( mesh.triangles ), None)
mesh2 = easyo3d.toMesh(lobj2[0], lobj2[5], lobj2[3], isDoSop=True)
easyo3d.render(mesh2)