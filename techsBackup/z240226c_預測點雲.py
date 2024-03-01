# 在 231219 中，要作 Infer 點雲 的測試

#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

import requests
# %%
url = 'http://140.123.121.21:443/toothgum_seg-api/infer/lower_tooth/point_cloud/'
stl_file_path = './../CrownSegmentationNew/1/lower_mod.stl'  #
stl_file_path = "D:/coding/透明牙套/庭凱測試結果/測試AI_20231020/case1_lower/Template1-0_lower_Stage1_step0_0629_Nicky.stl"

# 使用文件上傳方式發送POST請求
with open(stl_file_path, 'rb') as fp:
    mesh = readStlBinary_ToO3dMesh(fp)
    vertexs = np.array( mesh.vertices , dtype=np.float32 )
    normals = np.array( mesh.vertex_normals, dtype=np.float32 )
    xyznnnUpload = np.hstack([vertexs,normals]) # pc upload 測試用
    files = {'stl_file': xyznnnUpload.tobytes()}
    datas = {'mode': 'lower'} # 其實沒用到
    response = requests.post(url, files=files, data=datas)

# 檢查響應狀態碼
if response.status_code == 200:
    print('請求成功！')
else:
    print(f'請求失敗，狀態碼：{response.status_code}')
print(response.headers)

print(response.text[:256])