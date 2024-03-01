
"""
141筆重複資料，將其移動到另一資料夾(實際上可以砍掉，但先留著一陣子)
"""
#%%
from add_parent_dir_to_sys_path import set_cwd_and_add_parent_dir_to_sys_path_callme_initially
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
import glob
import shutil # move file
dir1 = r'./../../Crown資料重複被丟在這'
paths = glob.glob(dir1 + '/*')
# ./../../Crown資料重複被丟在這\0_lower.lobj

# 分析檔名，得到 idd upperlower
import re
def get_idd_upperlower(path):
    name = os.path.basename(path)
    idd = int(re.search(r'(\d+)_', name).group(1))
    upperlower = re.search(r'_(lower|upper)', name).group(1)
    return idd, upperlower, path
infos = [get_idd_upperlower(path) for path in paths]

# 若 1000xx 存在，移過來
dir2 = r'./../../CrownSegmentationNew_SrcDataLObj'
for idd, upperlower, path in infos:
    name = f'{idd+10000}_{upperlower}.lobj'
    pathSrc = os.path.join(dir2, name)
    pathDst = os.path.join(dir1, name)
    if os.path.exists(pathSrc) == False:
        continue
    # move file path2 to path2b
    shutil.move(pathSrc, pathDst)
    print(f'moved {pathSrc} to ... \n {pathDst}')

