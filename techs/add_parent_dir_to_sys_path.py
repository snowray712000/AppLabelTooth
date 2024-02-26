import inspect
import os
import sys

def get_this_py_file_dir()->str:
    """ 因為有 set_cwd_to_this_py_file_dir 而重構的 """
    r1 = inspect.currentframe()
    r2 = inspect.getfile(r1) # fullpath, e.g. D:\xxxxx\xxx\xxxx.py
    r3 = os.path.split(r2) # ('D:\\xxxxx\\xxx', 'xxxx.py')
    return os.path.realpath( os.path.abspath(r3[0]) )

def set_cwd_to_this_py_file_dir():
    """ 將當前工作目錄，設定為這個 py 檔的目錄 
    - Notes:
        - 因為 F5 與 Ctrl + M 的 CWD 不同，所以通常這個函式是一程式一開始就呼叫
    """
    os.chdir( get_this_py_file_dir() )

def add_parent_dir_to_sys_path():
    """ 將上一層 dir 加入 sys.path 
    - Notes:
        - Easy 工具整理在一個資料夾，但要用它，就必須是 Easy 的 parent 資料夾，不能是平行資料夾。如果 parent 資料夾就會一大堆 測試程式碼 造成混亂。
    """
    dir = get_this_py_file_dir()
    parent = os.path.split(dir)[0]
    if parent not in sys.path:
        sys.path.insert(0, parent)
        
def set_cwd_and_add_parent_dir_to_sys_path_callme_initially():
    """ 一開始就呼叫，設定 CWD 與加入 parent dir 到 sys.path """
    set_cwd_to_this_py_file_dir()
    add_parent_dir_to_sys_path()
    