import inspect
import os
import sys

def add_parent_dir_to_sys_path():
    r1 = inspect.currentframe()
    r2 = inspect.getfile(r1) # fullpath, e.g. D:\xxxxx\xxx\xxxx.py
    r3 = os.path.split(r2) # ('D:\\xxxxx\\xxx', 'xxxx.py')
    r4 = os.path.abspath(r3[0]) # D:\xxxxx\xxx
    r5 = os.path.split(r4) # ('D:\\xxxxx', 'xxx')
    r6 = os.path.realpath(r5[0]) # D:\xxxxx\xxx ... 這個優點是， symlink 也可以用
    if r6 not in sys.path:
        sys.path.insert(0, r6)