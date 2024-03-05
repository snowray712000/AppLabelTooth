
#%%
from add_parent_dir_to_sys_path import set_cwd_and_add_parent_dir_to_sys_path_callme_initially
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 載入 infos
from Easy.enumSrcDataLObjSorted import enumSrcDataLObjSorted4

infos = enumSrcDataLObjSorted4(upperlower=None, isOnlyLastVersion=True)

def fnSelect(info):
    path, idd, ver, upperlower = info
    
    lobj = LabeledObject().read(path)
    points = lobj[0]
    z = points[:,2]
    zlimit = np.min(z) if upperlower == "lower" else np.max(z)
    
    hasBottom = np.sum(z == zlimit) > 25
    return (idd, upperlower, hasBottom, path)
infos2 = lq.linq(infos).select(fnSelect).to_list()

#%%
# prepare `../tf` dir ... if exist, remove it, 建立
tfDir = "./../../tf"
if os.path.exists(tfDir):
    shutil.rmtree(tfDir)
os.makedirs(tfDir)
os.makedirs(f"{tfDir}/lower")
os.makedirs(f"{tfDir}/upper")
os.makedirs(f"{tfDir}/lower/valid")
os.makedirs(f"{tfDir}/lower/train")
os.makedirs(f"{tfDir}/upper/valid")
os.makedirs(f"{tfDir}/upper/train")

#%%
# < 141 組的處理方式，與 > 141 組的處理方式不同

# 取得 < 141 組的
infos141 = lq.linq(infos2).where(lambda x: x[0] < 141).to_list()

# Group By upperlower
infos141Group = lq.linq(infos141).group(lambda x: x[1]).to_list()

# 分組到下面 4 種裡
infos141UpperTrain = []
infos141UpperValid = []
infos141LowerTrain = []
infos141LowerValid = []
for a1, a2 in infos141Group:
    kkey: t.Literal['lower','upper'] = a1
    values: lq.Linque = a2
    
    # 亂數排序
    itemsShuffle = values.shuffle().to_list()
    
    # 目前個數，採二成，作驗證
    n = len(itemsShuffle)
    nValid = n // 5
    itemValid = lq.linq(itemsShuffle).take(nValid).to_list()
    itemTrain = lq.linq(itemsShuffle).skip(nValid).to_list()
    
    if kkey == "upper":
        infos141UpperTrain.extend(itemTrain)
        infos141UpperValid.extend(itemValid)
    elif kkey == "lower":
        infos141LowerTrain.extend(itemTrain)
        infos141LowerValid.extend(itemValid)
    else:
        raise Exception("不可能")
    
    # 141 組有 10000 有底的, 若 path 存在, 就包含進去
    for aa1 in itemTrain:
        idd, upperlower, hasBottom, path = aa1
        name = f'{idd+10000}_{upperlower}.lobj'
        path10000 = os.path.join( os.path.split(path)[0], name )  
        if os.path.exists(path10000):
            if upperlower == "lower":
                infos141LowerTrain.append((idd+10000, upperlower, True, path10000))
            else:
                infos141UpperTrain.append((idd+10000, upperlower, True, path10000))
    for aa1 in itemValid:
        idd, upperlower, hasBottom, path = aa1
        name = f'{idd+10000}_{upperlower}.lobj'
        path10000 = os.path.join( os.path.split(path)[0], name )  
        if os.path.exists(path10000):
            if upperlower == "lower":
                infos141LowerValid.append((idd+10000, upperlower, True, path10000))
            else:
                infos141UpperValid.append((idd+10000, upperlower, True, path10000))           

#%%
# >= 141 組的處理方式，但要 < 10000
infosOver141 = lq.linq(infos2).where(lambda x: x[0] >= 141 and x[0]<10000).to_list()        

# group by upperlower
infosOver141Group = lq.linq(infosOver141).group(lambda x: x[1]).to_list()

# 分組到下面 4 種裡
infosOver141UpperTrain = []
infosOver141UpperValid = []
infosOver141LowerTrain = []
infosOver141LowerValid = []

for a1, a2 in infosOver141Group:
    kkey: t.Literal['lower','upper'] = a1
    values: lq.Linque = a2
    
    # 亂數排序
    itemsShuffle = values.shuffle().to_list()
    
    # 目前個數，採二成，作驗證
    n = len(itemsShuffle)
    nValid = n // 5
    itemValid = lq.linq(itemsShuffle).take(nValid).to_list()
    itemTrain = lq.linq(itemsShuffle).skip(nValid).to_list()
    
    if kkey == "upper":
        infosOver141UpperTrain.extend(itemTrain)
        infosOver141UpperValid.extend(itemValid)
    elif kkey == "lower":
        infosOver141LowerTrain.extend(itemTrain)
        infosOver141LowerValid.extend(itemValid)
    else:
        raise Exception("不可能")
    
    # 141 組有 10000 有底的, 若 path 存在, 就包含進去
    # > 141 不會有 10000 以上的。
#%%
# 將資訊寫在 infos.txt
texts: t.List[str] = []

# < 141 處理
texts.extend(lq.linq(infos141UpperTrain).select(lambda x: f"train, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infos141UpperValid).select(lambda x: f"valid, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infos141LowerTrain).select(lambda x: f"train, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infos141LowerValid).select(lambda x: f"valid, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
# > 141 處理
texts.extend(lq.linq(infosOver141UpperTrain).select(lambda x: f"train, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infosOver141UpperValid).select(lambda x: f"valid, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infosOver141LowerTrain).select(lambda x: f"train, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())
texts.extend(lq.linq(infosOver141LowerValid).select(lambda x: f"valid, {x[0]}, {x[1]}, {'bottom' if x[2] else 'nobottom'}, {x[3]}").to_list())

# write infos.txt
with open(f"{tfDir}/infos.txt", "w") as f:
    f.write("\n".join(texts))

#%%
# 將 lobj 檔案複製到對應的目錄

# < 141 處理
for a1 in infos141UpperTrain:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/upper/train")
    
for a1 in infos141UpperValid:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/upper/valid")
    
for a1 in infos141LowerTrain:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/lower/train")

for a1 in infos141LowerValid:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/lower/valid")
    
# > 141 處理
for a1 in infosOver141UpperTrain:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/upper/train")
    
for a1 in infosOver141UpperValid:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/upper/valid")
    
for a1 in infosOver141LowerTrain:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/lower/train")
    
for a1 in infosOver141LowerValid:
    idd, upperlower, hasBottom, path = a1
    shutil.copy(path, f"{tfDir}/lower/valid")
    
#%%

