# %%
from Easy.easys import easy
import re
import typing as t
import os

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



def findLobjWhereIdobj(lobjs: t.List[t.Tuple[str, int]], idobj: int) -> t.Optional[t.Tuple[str, int]]:
    for a1 in lobjs:
        if a1[1] == idobj:
            return a1
    return None


if __name__ == "__main__":
    lobjs3 = enumSrcDataLObjSorted(upperlower='upper')
    lobjs4 = enumSrcDataLObjSorted2(upperlower='upper')
    lobjs5 = enumSrcDataLObjSorted3(upperlower='upper')
    print(lobjs5)
