from __future__ import annotations # Menu 使用 Menu ，當然，也可以直接使用 Self
# -*- coding: utf-8 -*-
"""
Created on 2023/8/9
@author: User
"""

#%% 讀  .lobj 檔
import numpy as np
import numpy.typing as npt
from typing import List, Union, Tuple, Optional
import typing as t
      
class LabeledObject:
  """vertexs, normals, colors, vertex_labels, tex2d, triangles, texId
  """
  _s: LabeledObject = None
  
  def __new__(cls, *args, **kwargs):
      if cls._s is None:
          cls._s = super().__new__(cls)
      return cls._s
  def __init__(self):
    if hasattr(self, 'isInit'):
      return
    self.isInit = True
    
  def read(self, path:str)-> t.Tuple[npt.NDArray[np.float32], # vertexs (:,3)
                    Optional[npt.NDArray[np.float32]], # normals (:,3)
                    Optional[npt.NDArray[np.float32]], # colors (:,3)
                    Optional[npt.NDArray[np.int8]], # labels (3)
                    Optional[npt.NDArray[np.float32]], # tex2D (:,2)
                    npt.NDArray[np.int32], # triangles (:,3)
                    Optional[npt.NDArray[np.int32]], # texId (:,3)              
                ]:
    ''' [0] vertexs [3] labels [5] triangles 最可能用到 '''
    with open(path,'rb') as file:
      counts = np.frombuffer(file.read(28), dtype=np.int32)

      isVertex = counts[0] != 0
      isNormal = counts[1] != 0
      isColor = counts[2] != 0
      isVertexLabel = counts[3] != 0
      isTextureCoordinate = counts[4] != 0
      isTriangle = counts[5] != 0
      isTextureCoordinateIndex = counts[6] != 0

      if not isVertex or not isTriangle:
          raise Exception('assert False')
          
      vertexs, normals, colors, vertex_labels, tex2d, triangles, texId = None, None, None, None, None, None, None

      vertexs = np.array( np.frombuffer(file.read( counts[0] * 3 * 4 ), dtype=np.float32).reshape(-1,3) )
      if isNormal: # normal
          normals = np.array( np.frombuffer(file.read( counts[1] * 3 * 4 ), dtype=np.float32).reshape(-1,3) )
      if isColor: # color
          colors = np.array( np.frombuffer(file.read( counts[2] * 3 * 4 ), dtype=np.float32).reshape(-1,3) )
      if isVertexLabel: # labels
          vertex_labels = np.array( np.frombuffer(file.read( counts[3] * 1 * 1 ), dtype=np.int8) )
      if isTextureCoordinate: # [[0.0,0.0],[0.5,0.0],[1.0,0.0]]
          tex2d = np.array( np.frombuffer(file.read( counts[4] * 3 * 4 ), dtype=np.float32).reshape(-1,3) )      
      if isTriangle:# triangles
          triangles = np.array( np.frombuffer(file.read( counts[5] * 3 * 4 ), dtype=np.uint32).reshape(-1,3) )
      if isTextureCoordinateIndex:
          texId = np.array( np.frombuffer(file.read( counts[6] * 3 * 4 ), dtype=np.uint32).reshape(-1,3) )
          
    cntv = len(vertexs)
    cntt = len(triangles)    
    assert normals is None or len(normals) == cntv
    assert colors is None or len(colors) == cntv
    assert vertex_labels is None or len(vertex_labels) == cntv    
    assert texId == None or len(texId) == cntt
          
    return vertexs, normals, colors, vertex_labels, tex2d, triangles, texId
  def save(self,path:str, 
           vertexs:npt.NDArray[np.float32],
           normals:Optional[npt.NDArray[np.float32]],
           colors:Optional[npt.NDArray[np.float32]], 
           vertex_labels:Optional[npt.NDArray[np.int8]],
           tex2d:Optional[npt.NDArray[np.float32]],
           triangles:npt.NDArray[np.int32], 
           texId:Optional[npt.NDArray[np.int32]])->None:     
    ''' save .lobj 檔
    labels is int8, -1: no labels, 0: label0, 1: label1
    triangles is int32, 0-based
    vertex is float32, x y z '''
      

    cntv = len(vertexs)
    cntt = len(triangles)    
    assert normals is None or len(normals) == cntv
    assert colors is None or len(colors) == cntv
    assert vertex_labels is None or len(vertex_labels) == cntv    
    assert texId == None or len(texId) == cntt


    with open(path, "wb") as file:
      counts = [cntv, # vertices count
            0 if normals is None else cntv, # normals ... 不要存，反正，open3d 算很快
            0 if colors is None else cntv, # vertex color
            0 if vertex_labels is None else cntv, # vertex label count
            0 if tex2d is None else len(tex2d), # texture coordinate count , vt ...
            cntt,
            0 if texId is None else cntt, # triangles texture coordinate index count , f 1/1 2/1 3/1 通常 = 上一個值
            ]
      file.write(np.array(counts, dtype=np.int32).tobytes())

      # vertices
      file.write( np.array(vertexs, dtype=np.float32 ).tobytes() )
      # normals
      if counts[1] != 0:
          file.write( np.array(normals, dtype=np.float32 ).tobytes() )
      # colors
      if counts[2] != 0:
          file.write( np.array(colors, dtype=np.float32 ).tobytes() )
      # vertex labels
      if counts[3] != 0:
          file.write( np.array(vertex_labels, dtype=np.int8 ).tobytes() )
      # vertex texture coordinate [[0,0],[0.5,0],[1,0]]
      if counts[4] != 0:
          file.write( np.array(tex2d, dtype=np.float32 ).tobytes() )
      # triangle indexs [[0,1,2],[1,2,4],...] f 1 2 3 (但卻是 0-based)
      if counts[5] != 0:
          file.write( np.array(triangles, dtype=np.int32 ).tobytes() )
      # texture coordinate index f 1/1 2/2 3/3 (但卻用 0-based)
      if counts[6] != 0:
          file.write( np.array(texId, dtype=np.int32 ).tobytes() )
      
  def saveVsLsTris(self, path: str,
                   vertexs: npt.NDArray[np.float32],
                   labels: Optional[npt.NDArray[np.float32]],
                   triangles: npt.NDArray[np.int32]):
    ''' alias save(path, vertex, None, None, labels, None, triangles, None)
    labels is int8, -1: no labels, 0: label0, 1: label1
    triangles is int32, 0-based
    vertex is float32, x y z '''
    self.save(path,vertexs, None, None, labels, None, triangles, None)

if __name__ == '__main__':
    # LabeledObject().read('./test.lobj')
    r1 = LabeledObject().read(path = './../crownsegmentation_230802/result/re_140_lower_farthest_505.lobj')    
    LabeledObject().saveVsLsTris('./../crownsegmentation_230802/result/re_140_lower_farthest_505_b.lobj', r1[0], r1[3], r1[5])
    r2 = LabeledObject().read(path = './../crownsegmentation_230802/result/re_140_lower_farthest_505_b.lobj')
    pass