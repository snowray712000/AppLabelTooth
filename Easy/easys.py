# -*- coding: utf-8 -*-
"""
Created on 2023/8/9
@author: User
"""

from typing import List, Union, Tuple, Optional
import os #,內建的
import glob # 列舉用,內建的
import re # 文字處理用,內建的

class easy:
  _s = None
  def __new__(cls, *args, **kwargs):
      if cls._s is None:
          cls._s = super().__new__(cls)
      return cls._s
  def __init__(self):
    if hasattr(self, 'isInit'):
      return

    import os #,內建的
    import glob # 列舉用,內建的
    import re # 文字處理用,內建的
    globals().update(locals())

    self.isInit = None

  class io:
    def makeSureExistDir(dir:str):
      if not os.path.exists(dir):
          os.makedirs(dir)
    def getParentDir(pathFile:str)->str:
      return os.path.dirname(pathFile)
    def enumFiles(pattern: str = "./AfterFPS/*/FPS_points_*.xyz", isAbsoluteResult: bool = True)->List[str]:
      file_paths = glob.glob(pattern)
      if isAbsoluteResult:
        return [os.path.abspath(a1) for a1 in file_paths]
      return file_paths
    def toAbsPath(path:str)->str:
      return os.path.abspath(path)
    def writeAllLines(path:str, texts:List[str], encoding: str = "utf-8"):
      with open(path, 'w', encoding=encoding) as file:
        file.write("\n".join(texts))
    def readAllLines(path: str) -> List[str]:
        with open(path, 'r') as file:
            lines = [a1.strip() for a1 in file.readlines()] # 要去掉尾部的 \n
        return lines