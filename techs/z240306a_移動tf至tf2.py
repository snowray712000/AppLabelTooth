#%%
from add_parent_dir_to_sys_path import set_cwd_and_add_parent_dir_to_sys_path_callme_initially
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 列舉 tf 資料夾下的所有 .tfrecords 檔，並將其移動至 tf2
import glob
pathTFRecords = glob.glob('./../../tf/*/*/*.tfrecords')

# 建立 tf2 資料夾
tf2Dir = "./../../tf2"
os.makedirs(tf2Dir, exist_ok=True)
os.makedirs(f"{tf2Dir}/lower", exist_ok=True)
os.makedirs(f"{tf2Dir}/upper", exist_ok=True)
os.makedirs(f"{tf2Dir}/lower/valid", exist_ok=True)
os.makedirs(f"{tf2Dir}/lower/train", exist_ok=True)
os.makedirs(f"{tf2Dir}/upper/valid", exist_ok=True)
os.makedirs(f"{tf2Dir}/upper/train", exist_ok=True)

# 移動 .tfrecords 檔
pathTFRecords = lq.linq(pathTFRecords).select(lambda path: os.path.realpath(os.path.abspath(path))).to_list()
for pathTFRecord in pathTFRecords:
    pathSrc= pathTFRecord
    pathDst = pathSrc.replace('\\tf\\', '\\tf2\\')
    print(f'{pathSrc} -> {pathDst}')
    
    # move
    shutil.move(pathSrc, pathDst)