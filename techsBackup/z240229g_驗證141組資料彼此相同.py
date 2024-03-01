#%%
from add_parent_dir_to_sys_path import *
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
from Easy.enumSrcDataLObjSorted import enumSrcDataLObjSorted4

infos = enumSrcDataLObjSorted4(upperlower= 'lower')

#%%
infos2 = lq.linq(infos).where(lambda x: x[1] < 141).to_list()

#%%
def fn_select(a1):
    path, idd, ver, upperlower = a1
    lobj = LabeledObject().read(path)
    return len(lobj[0]), len(lobj[5]), idd, path
r1 = lq.linq(infos2).select(fn_select).to_list()

#%%
import open3d as o3d
import open3d.visualization as vis
for a1 in lq.group(r1, lambda x: (x[0], x[1])):
    if len(a1[1]) == 1:
        continue
    if len(a1[1]) == 2:
        path1 = a1[1][0][3]
        path2 = a1[1][1][3]
        lobj1 = LabeledObject().read(path1)
        lobj2 = LabeledObject().read(path2)
        idd1 = a1[1][0][2]
        idd2 = a1[1][1][2]
        
        
        if np.array_equal(lobj1[0], lobj2[0]) and np.array_equal(lobj1[5], lobj2[5]):
            if np.array_equal(lobj1[3], lobj2[3]):
                print('是一樣的, label 也是', idd1, idd2)
            else:
                print('是一樣的, 但 label 略有不同 ', idd1, idd2)
                mesh1 = easyo3d.toMesh2(lobj1)
                mesh2 = easyo3d.toMesh2(lobj2)
                pc1 = TpO3d.PointCloud()
                pc1.points = mesh1.vertices
                pc1.colors = mesh1.vertex_colors
                pc2 = TpO3d.PointCloud()
                pc2.points = mesh2.vertices
                pc2.colors = mesh2.vertex_colors
                
                vis.draw([{'name':f'{idd1}', 'geometry':mesh1},
                        {'name':f'{idd2}', 'geometry':mesh2},
                        {'name':f'{idd1} pc', 'geometry':pc1},
                        {'name':f'{idd2} pc', 'geometry':pc2}
                        ], show_ui = True, )
    else:
        print(a1[1], len(a1[1]))
            
            
        # print(a1[0], len(a1[1]))
        