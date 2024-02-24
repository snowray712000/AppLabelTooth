# %%
from Easy import *
import re
from Easy.easys import easy

def enumSrcDataLObjSorted(dirSrc='./../CrownSegmentationNew_SrcDataLObj/', upperlower='lower') -> t.List[str]:    
    r1 = enumSrcDataLObjSorted2(dirSrc, upperlower)
    return [a1[0] for a1 in r1]


def enumSrcDataLObjSorted2(dirSrc='./../CrownSegmentationNew_SrcDataLObj/', upperlower='lower') -> t.List[t.Tuple[str, int]]:
    lobjs = easy.io.enumFiles(f'{dirSrc}./*_{upperlower}.lobj')

    def parsingIdObj(pathLobj) -> int:
        '''f'{dirSrc}./*_{upperlower}.lobj'        
        '''
        try:
            match = re.findall(r'\d+', pathLobj)
            idcase = match[len(match)-1]  # in str
            return int(idcase)
        except:
            return -1
    r1 = [[a1, parsingIdObj(a1)] for a1 in lobjs]
    return sorted(r1, key=lambda x: x[1])

def enumSrcDataLObjSorted3(dirSrc='./../CrownSegmentationNew_SrcDataLObj/', upperlower='lower') -> t.List[t.Tuple[str, int,int]]:
    """ lobj 檔，開始有手動修正的版本，所以，要用這個函數

    Args:
        dirSrc (str, optional): _description_. Defaults to './../CrownSegmentationNew_SrcDataLObj/'.
        upperlower (str, optional): _description_. Defaults to 'lower'.

    Returns:
        t.List[t.Tuple[str, int,int]]: [0] path, [1] idobj, [2] version (1開始就是修正的)
    """
    
    lobjs: t.List[str] = easy.io.enumFiles(f'{dirSrc}./*_{upperlower}.lobj')
    lobjs2: t.List[str] = easy.io.enumFiles(f'{dirSrc}./*_{upperlower}_fixed_*.lobj')
    print(lobjs2)

    def parsing(pathLobj) -> int:
        '''f'{dirSrc}./*_{upperlower}*.lobj'        
        '''
        try:
            name = os.path.basename(pathLobj)
            match = re.findall(r'\d+', name)            
            
            if len(match) == 1:
                idcase = match[0]
                version = "0"
            else:
                idcase = match[0]
                version = match[1]            
            return pathLobj, int(idcase), int(version)
        except:
            return pathLobj, -1, 0
    
    lobjs.extend(lobjs2)
        
    r1 = [parsing(a1) for a1 in lobjs]
    
    return sorted(r1, key=lambda x: (x[1], x[2]))

def parse_path_to_id_version_upperlower(pathLobj: str) -> t.Tuple[str, int, int, t.Literal['lower','upper','unknown']]:
    basename = os.path.basename(pathLobj)
    # 為了取得 id。若沒有follow命名規則，就變成 -1
    r1 = r"(\d+)_"
    r2 = re.search(r1, basename)
    idobj = int(r2.group(1)) if r2 is not None else -1
    
    # 為了取得 lower|upper。若沒有follow命名規則，就變成 unknown
    r3 = r"_(lower|upper)"
    r4 = re.search(r3, basename)
    upperlower = r4.group(1) if r4 is not None else "unknown"
    
    # 為了取得 version。若沒有_fixed_1，表示是第 0 個版本
    r6 = r"_fixed_(\d+).lobj"
    r7 = re.search(r6, basename)
    version = int(r7.group(1)) if r7 is not None else 0
    
    return pathLobj, idobj, version, upperlower
    
def enumSrcDataLObjSorted4(dirSrc='./../CrownSegmentationNew_SrcDataLObj/', upperlower: t.Optional[t.Literal['lower','upper']] = 'lower', isOnlyLastVersion: bool = False) -> t.List[t.Tuple[str, int, int, t.Literal['lower','upper','unknown']]]:
    """ 141組以外的資料，命名規則很不一樣了，不再只有 idobj 與 lower 與 fixed 字眼了。

    ### Returns:
    - path, id, version, upperlower
    """
    paths = easy.io.enumFiles(f'{dirSrc}./*.lobj')
    
    re1 = [parse_path_to_id_version_upperlower(a1) for a1 in paths]
    
    # 產生 tuple of path, id, version, upperlower
    if upperlower is not None:
        re1 = [(a1, int(a2), int(a3), a4) for a1, a2, a3, a4 in re1 if a4 == upperlower]
    
    # sort by id, version
    re2 = sorted(re1, key=lambda x: (x[1], x[2]))
    
    # 只取最後一個版本
    if isOnlyLastVersion == False:
        return re2
    re3 = lq.linq(re2).group(lambda x: (x[1], x[3])).select(lambda x: x[1].last()).to_list()
    return re3
        
    
def findLobjWhereIdobj(lobjs: t.List[t.Tuple[str, int]], idobj: int) -> t.Optional[t.Tuple[str, int]]:
    for a1 in lobjs:
        if a1[1] == idobj:
            return a1
    return None

if __name__ == "__main__":
    #lobjs3 = enumSrcDataLObjSorted(upperlower='upper')
    #lobjs4 = enumSrcDataLObjSorted2(upperlower='upper')
    #lobjs5 = enumSrcDataLObjSorted3(upperlower='upper')
    lobj6 = enumSrcDataLObjSorted4(upperlower=None, isOnlyLastVersion=True)
    for a1 in lobj6:
        print(a1)
    pass