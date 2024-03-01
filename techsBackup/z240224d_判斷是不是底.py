""" 觀察 資料 height, z等於最大z個數 
目的：為了能夠知道，這個 stl 是不是 `有底的`
"""
#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 列舉 141 筆資料
from enumSrcDataLObjSorted import enumSrcDataLObjSorted4
r1 = enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',
                            upperlower='lower',
                            isOnlyLastVersion=True)
r1b = enumSrcDataLObjSorted4(dirSrc='./../../CrownSegmentationNew_SrcDataLObj',upperlower='upper',isOnlyLastVersion=True)
r1.extend(r1b)
print(r1)

#%%
# 輸出 id, upperlower, height, 極值個數(上顎取最大值，下顎取最小值)
def fn1(a1):
    path, idobj, version, upperlower = a1
    lobj = LabeledObject().read(path)
    pts = lobj[0]
    z = pts[:,2]
    zMax = np.max(z)
    zMin = np.min(z)
    height = zMax - zMin
    
    # 取極值個數
    if upperlower == 'upper':
        # z == ZMax 的個數
        count = np.sum(z == zMax)
    else:
        count = np.sum(z == zMin)
    return idobj, upperlower, height, count
r2 = lq.linq(r1).select(fn1).to_list()
print(r2)

#%%
# 輸出 .csv 檔
with open('z240224d.csv', 'w') as f:
    f.write('id,upperlower,height,count\n')
    for idobj, upperlower, height, count in r2:
        f.write(f'{idobj},{upperlower},{height},{count}\n')