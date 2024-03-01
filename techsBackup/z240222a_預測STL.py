# 在 231219 中，要作 Infer 的測試

#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

import requests
# %%
# url = 'http://127.0.0.1:5000/infer/lower'
url = 'http://127.0.0.1:5000/infer/lower/test_stl_upload/'
# url = 'http://140.123.121.34:443/infer/lower/test_stl_upload/'
# url = 'http://127.0.0.1:5000/infer/lower/test_reponse_16000_2/'
# url = 'http://127.0.0.1:5000/infer/lower/test_reponse_16000_2_gzip/'
# url = 'http://140.123.121.34:443/infer/lower/test_reponse_16000_2/'
# url = 'http://140.123.121.34:443/infer/lower/test_reponse_16000_2_gzip/'

# url = 'http://127.0.0.1:5000/infer/lower/test_infer_predict_randomly/'
url = 'http://140.123.121.21:443/toothgum_seg-api/infer/lower/'
url = 'http://140.123.121.21:443/toothgum_seg-api/infer/lower_tooth/'
stl_file_path = './../CrownSegmentationNew/1/lower_mod.stl'  #
stl_file_path = "D:/coding/透明牙套/庭凱測試結果/測試AI_20231020/case1_lower/Template1-0_lower_Stage1_step0_0629_Nicky.stl"

# 使用文件上傳方式發送POST請求
with open(stl_file_path, 'rb') as stl_file:
    files = {'stl_file': stl_file}
    datas = {'mode': 'lower'}
    response = requests.post(url, files=files, data=datas)

# 檢查響應狀態碼
if response.status_code == 200:
    print('請求成功！')
else:
    print(f'請求失敗，狀態碼：{response.status_code}')
print(response.headers)

print(response.text[:256])
