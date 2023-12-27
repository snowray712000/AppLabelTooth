#%% easy colab
from typing import List, Union, Tuple, Optional

class easycolab:
  _s = None
  def __new__(cls, *args, **kwargs):
      if cls._s is None:
          cls._s = super().__new__(cls)
      return cls._s
  def __init__(self):
    if hasattr(self, 'isInit'):
      return

    import os #,內建的
    import pathlib
    from google.colab import drive
    globals().update(locals())

    self.isInit = None

  def getDir_Current()->str:
    '''
    example: /content/drive/MyDrive/Colab Notebooks/PointNetpp
    os.getcwd()
    '''
    return pathlib.Path().absolute() # 等同 os.getcwd()
    # return os.getcwd()
  def mountGoogleDriver():
    if not os.path.ismount('/content/drive'):
      from google.colab import drive
      drive.mount('/content/drive',force_remount=True)
  def changeDirAndReturnOld(path: str = '/Colab Notebooks/PointNetpp')->str:
    '''
    example: '/Colab Notebooks' ; you can use '/content/drive/MyDrive/Colab Notebooks' also
    '''
    prefix_to_remove = '/content/drive/MyDrive'
    path = path.removeprefix(prefix_to_remove)
    r1 = os.getcwd()
    os.chdir('/content/drive/MyDrive' + path)
    return r1
  class ChangeDirAutoRestore:
    '''
    with easycolab.ChangeDirAutoRestore(path = "/Colab Notebooks/ToothSegment/CrownSegmentation141") as chdir:
      print(os.getcwd())
    print(os.getcwd())
    '''
    def __init__(self, path: str = '/Colab Notebooks/PointNetpp'):
      self.old = easycolab.changeDirAndReturnOld(path)
    def __enter__(self):
        # 執行進入上下文時的操作，這裡可以打開檔案、建立連線等
        # print("進入上下文")
        return self  # 返回一個代表上下文的物件

    def __exit__(self, exc_type, exc_value, traceback):
        # 執行離開上下文時的操作，這裡可以關閉檔案、關閉連線等
        # print("離開上下文")
        easycolab.changeDirAndReturnOld(self.old)
        if exc_type is not None:
            # 處理例外情況，如果需要抑制例外，返回 True
            print(f"發生例外：{exc_type}, {exc_value}")
            return False