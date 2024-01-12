#%%
import numpy as np
import open3d as o3d
from Easy import TpO3d
import typing as t
import numpy.typing as npt
import linque as lq
import os
import glob
#%%
from enumSrcDataLObjSorted import enumSrcDataLObjSorted3
from Easy.ColorsForCrown import labels_to_colors_crown

path_idds_upper = enumSrcDataLObjSorted3(upperlower="upper")
path_idds_lower = enumSrcDataLObjSorted3(upperlower="lower")

#%% GlobalValue
class AppGlobals:
    pathlobj: str
    '''開啟的 pathlobj '''
    upper_lower: str
    '''開啟的 pathlobj ，是 upper 還是 lower ， 還是 other '''
    idd: int
    ver: int
    '''開啟的 id '''
    lobj: t.Tuple[
              npt.NDArray[np.float32], # vertexs (:,3)
              t.Optional[npt.NDArray[np.float32]], # normals (:,3)
              t.Optional[npt.NDArray[np.float32]], # colors (:,3)
              t.Optional[npt.NDArray[np.int8]], # labels (3)
              t.Optional[npt.NDArray[np.float32]], # tex2D (:,2)
              npt.NDArray[np.int32], # triangles (:,3)
              t.Optional[npt.NDArray[np.int32]], # texId (:,3)
            ]
    '''開啟的 lobj '''
    tpMethod: int = 1
    """ 0: radius, 1: knn """
    kdtree: t.Optional[TpO3d.KDTreeFlann]
    dict_adjacency: t.Optional[t.Dict[int, t.List[int]]]
    mesh: t.Optional[TpO3d.TriangleMesh]
    ''' 雖然最後只用到 kdtree，沒用到 mesh，但若 kdtree 的來源 mesh 沒存起來，呼叫 kdtree 時會當掉 '''
    lenMaxMesh: float = 10.0
    radius_percent: float = 1/40
    radius: float = 0.4
    count_recursive: int = 1 # knn 方法，遞迴的次數
    setValue: np.int8 = 1 
    dirFileDialog: str = os.getcwd()
    def enumFiles()->t.List[str]:
        """ 產生給  ListView 用的資料 """
        r1 = glob.glob(AppGlobals.dirFileDialog + '/*', recursive=False)
        r2 = lq.linque(r1).where(lambda a1: os.path.isdir(a1)).select(lambda a1: os.path.basename(a1)).to_list()
        # print(r2)

        # exts = ['.stl', '.lobj', '.xyz']
        # exts = ['.stl']
        exts = ['.lobj']
        r3 = lq.linque(r1).where(lambda a1: os.path.isfile(a1)).select(lambda a1: os.path.basename(a1)).where(lambda a1: os.path.splitext(a1)[1] in exts).to_list()
        # print(r3)
        
        items = ['..'] + r2 + r3
        return items
    """ other list 清單的 """
    ''' 右鍵點擊時，要設定的 label 值 '''
    data_undo: t.List[npt.NDArray[np.int8]] = []
    data_redo: t.List[npt.NDArray[np.int8]] = []
    isDragPick: bool = False # 右鍵點擊時，是否拖曳，決定 undo redo 用

#%%
# undo redo 
class UnDoReDo:
    @staticmethod
    def push_to_undo_and_clear_redo(labels: npt.NDArray[np.int8]):
        """ 滑鼠右鍵點擊，有變更時呼叫 """
        AppGlobals.data_undo.append(labels.copy())
        AppGlobals.data_redo.clear()
    
    @staticmethod
    def pop_from_undo_and_push_to_redo()-> t.Optional[npt.NDArray[np.int8]]:
        """ 按下 z 時，呼叫 """
        if len(AppGlobals.data_undo) == 0:
            return None
        
        labels = AppGlobals.data_undo.pop()
        AppGlobals.data_redo.append(labels.copy())
        return labels
    
    @staticmethod
    def pop_from_redo_and_push_to_undo()-> t.Optional[npt.NDArray[np.int8]]:
        """ 按下 y 時，呼叫 """
        if len(AppGlobals.data_redo) == 0:
            return None
        
        labels = AppGlobals.data_redo.pop()
        AppGlobals.data_undo.append(labels.copy())
        return labels    
    
    @staticmethod
    def clear_undo_and_redo():
        """ 重新開啟檔案時，呼叫 """
        AppGlobals.data_undo.clear()
        AppGlobals.data_redo.clear()
    

#%%
app = TpO3d.Application()
app.initialize()

font = TpO3d.FontDescription("c:/windows/fonts/mingliu.ttc")
font.add_typeface_for_language("c:/windows/fonts/mingliu.ttc", "zh_all")
app.set_font(0, font)

# settings
winSettings = app.create_window("Settings", 300, 600)

vert1 = TpO3d.Vert()
winSettings.add_child(vert1)

# 操作說明
btnHelp = TpO3d.Button("Help")
vert1.add_child(btnHelp)

# 另存目前 lobj
btnSaveAs = TpO3d.Button("Save As")
vert1.add_child(btnSaveAs)

# method 選擇
methods = TpO3d.RadioButton(TpO3d.RadioButton.Type.HORIZ)
vert1.add_child(methods)
methods.set_items(["指定半徑", "指定相鄰層數"])
methods.selected_index = 1

sliderCountRecursive = TpO3d.Slider(TpO3d.Slider.Type.INT)
vert1.add_child(sliderCountRecursive)
sliderCountRecursive.set_limits(1, 30)
sliderCountRecursive.int_value = AppGlobals.count_recursive

# 滑鼠右鍵點擊，所影響的半徑 Slider
sliderRadius = TpO3d.Slider(TpO3d.Slider.Type.DOUBLE)
sliderRadius.enabled = False
sliderRadius.set_limits(1/200, 1/20)
sliderRadius.double_value = 1/40
vert1.add_child(sliderRadius)

# 要設定的 lable 值 Slider
sliderSetValue = TpO3d.Slider(TpO3d.Slider.Type.INT)
sliderSetValue.enabled = False
sliderSetValue.set_limits(0, 16)
sliderSetValue.int_value = AppGlobals.setValue
sliderSetValue.tooltip = "要設定的 lable 值，0 是牙齦，1 是智齒 ... "
vert1.add_child(sliderSetValue)

# label 顯示
colorsLabel = labels_to_colors_crown( np.arange(17, dtype=np.int8))
hstack1 = TpO3d.Horiz()
vert1.add_child(hstack1)
hstack2 = TpO3d.Horiz()
vert1.add_child(hstack2)
hstack3 = TpO3d.Horiz()
vert1.add_child(hstack3)
hstack4 = TpO3d.Horiz()
vert1.add_child(hstack4)

# lableName = ["牙齦","智齒","大臼齒","大臼齒","前臼齒","前臼齒","犬齒","門齒","門齒",
#             "門齒","門齒","犬齒","前臼齒","前臼齒","大臼齒","大臼齒","智齒"]
lableName = ["牙齦","智","大臼","大臼","前臼","前臼","犬","門","門",
            "門","門","犬","前臼","前臼","大臼","大臼","智"]
btnColorLabels = [TpO3d.Button(f"{str(i)}{lableName[i]}") for i in range(17)]
for i in range(17):
    btnColorLabels[i].background_color = TpO3d.Color(colorsLabel[i][0], colorsLabel[i][1], colorsLabel[i][2])    
    if i <= 8:
        hstack1.add_child(btnColorLabels[i])
    else:
        hstack2.add_child(btnColorLabels[i])    

# list3
vertCollepse3 = TpO3d.CollapsableVert("other", 0, TpO3d.Margins.lazyMarginsEM(winSettings,0.5,0,0.5,0))
vert1.add_child(vertCollepse3)
vertCollepse3.set_is_open(True)

list3 = TpO3d.ListView()
vertCollepse3.add_child(list3)
list3.set_items(AppGlobals.enumFiles())
list3.set_max_visible_items(10)

# list1
vertCollepse1 = TpO3d.CollapsableVert("upper", 0, TpO3d.Margins.lazyMarginsEM(winSettings,0.5,0,0.5,0))
vert1.add_child(vertCollepse1)
vertCollepse1.set_is_open(False)

list1 = TpO3d.ListView()
vertCollepse1.add_child(list1)
list1.set_max_visible_items(10)
list1.set_items([f"id_{str(a1[1])}_ver_{str(a1[2])}" for a1 in path_idds_upper])

# list2
vertCollepse2 = TpO3d.CollapsableVert("lower", 0, TpO3d.Margins.lazyMarginsEM(winSettings,0.5,0,0.5,0))
vert1.add_child(vertCollepse2)
vertCollepse2.set_is_open(False)

list2 = TpO3d.ListView()
vertCollepse2.add_child(list2)
list2.set_items([f"id_{str(a1[1])}_ver_{str(a1[2])}" for a1 in path_idds_lower])
list2.set_max_visible_items(10)

# win3D
win3D = app.create_window("3D", 768, 768)
scene = TpO3d.SceneWidget()
win3D.add_child(scene)
scene3d = TpO3d.Open3DScene(win3D.renderer)
scene.scene = scene3d
# scene3d.show_axes(True)
scene3d.show_ground_plane(True, TpO3d.Scene.GroundPlane.XY)

winSettings.size_to_fit()
app.post_to_main_thread(winSettings, lambda: winSettings.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示

winSettings.os_frame = TpO3d.Rect(win3D.os_frame.x  - winSettings.content_rect.width, winSettings.os_frame.y
                                  , winSettings.content_rect.width, winSettings.content_rect.height)

app.post_to_main_thread(win3D, lambda: win3D.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示
app.post_to_main_thread(winSettings, lambda: winSettings.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示
#%% 
# callback functions 
from Easy.LabeledObject import LabeledObject
import os

def fn_clickHelp():
    winSettings.show_message_box("Help", "選取檔案：雙擊清單。\n滑鼠左鍵，旋轉。\nCtrl+左滑鼠鍵，平移。\n滑鼠滾輪，縮放。\n右滑鼠鍵，設定 label。\nZ，undo。Y，redo。\n")
btnHelp.set_on_clicked(fn_clickHelp)

def enum_and_set_list3():
    """ 產生給  ListView 用的資料 
    - 使用 AppGlobals.dirFileDialog 路徑資料。
    """
    list3.set_items(AppGlobals.enumFiles())
    
def reload_and_update_listboxview():
    global path_idds_upper, path_idds_lower
    if AppGlobals.upper_lower == "upper":
        path_idds_upper = enumSrcDataLObjSorted3(upperlower="upper")
        list1.set_items([f"id_{str(a1[1])}_ver_{str(a1[2])}" for a1 in path_idds_upper])
        list1.selected_index = next((i for i, x in enumerate(path_idds_upper) if x[1] == AppGlobals.idd and x[2] == AppGlobals.ver), None)        
    elif AppGlobals.upper_lower == "lower":
        path_idds_lower = enumSrcDataLObjSorted3(upperlower="lower")
        list2.set_items([f"id_{str(a1[1])}_ver_{str(a1[2])}" for a1 in path_idds_lower])    
        list2.selected_index = next((i for i, x in enumerate(path_idds_lower) if x[1] == AppGlobals.idd and x[2] == AppGlobals.ver), None)
    elif AppGlobals.upper_lower == "other":
        basename = os.path.basename(AppGlobals.pathlobj)
        names = AppGlobals.enumFiles()
        list3.set_items(names)
        
        def fn_first1(a1: t.Tuple[int,str]):
            return a1 == basename
        re: t.Tuple[int,str] = lq.linque( enumerate(names) ).first(fn_first1)
        list3.selected_index = re[0]
    
def generate_filename(path, dir):
    base_name = os.path.basename(path)  # 從路徑中提取檔名    
    name, ext = os.path.splitext(base_name)  # 分離檔名和副檔名
    
    if "_fixed_" in name:
        name = name.rsplit("_fixed_", 1)[0]  # 移除最後一個_fixed_字串
        
    i = 1 # 1開始，0作為原始版本
    while True:
        new_name = f"{name}_fixed_{i}{ext}"  # 生成新的檔名
        new_path = os.path.join(dir, new_name)  # 生成新的路徑
        if not os.path.exists(new_path):  # 檢查檔案是否存在
            return new_name  # 如果檔案不存在，返回新的檔名
        i += 1  # 如果檔案存在，增加數字並再次檢查
def fn_btnSaveAs_clicked():
    try:        
        abs_path = os.path.abspath(AppGlobals.pathlobj)
        dir = os.path.dirname(abs_path)    
        path2 = generate_filename(AppGlobals.pathlobj, dir + '/')
        LabeledObject().saveVsLsTris(dir + '/' + path2, AppGlobals.lobj[0], AppGlobals.lobj[3], AppGlobals.lobj[5])
        
        reload_and_update_listboxview()
        
    except Exception as e:
        print(e)
    
    pass
btnSaveAs.set_on_clicked(fn_btnSaveAs_clicked)

def fn_slider_count_recursive_changed(value):
    AppGlobals.count_recursive = value
sliderCountRecursive.set_on_value_changed(fn_slider_count_recursive_changed)

def fn_sliderRadius_changed(value):
    AppGlobals.radius_percent = value
    AppGlobals.radius = AppGlobals.lenMaxMesh * AppGlobals.radius_percent         
sliderRadius.set_on_value_changed(fn_sliderRadius_changed)

def fn_clickLabel_0():
    sliderSetValue.int_value = 0
    AppGlobals.setValue = 0
def fn_clickLabel_1():
    sliderSetValue.int_value = 1
    AppGlobals.setValue = 1
def fn_clickLabel_2():
    sliderSetValue.int_value = 2
    AppGlobals.setValue = 2
def fn_clickLabel_3():
    sliderSetValue.int_value = 3
    AppGlobals.setValue = 3
def fn_clickLabel_4():
    sliderSetValue.int_value = 4
    AppGlobals.setValue = 4
def fn_clickLabel_5():
    sliderSetValue.int_value = 5
    AppGlobals.setValue = 5
def fn_clickLabel_6():
    sliderSetValue.int_value = 6
    AppGlobals.setValue = 6
def fn_clickLabel_7():
    sliderSetValue.int_value = 7
    AppGlobals.setValue = 7
def fn_clickLabel_8():
    sliderSetValue.int_value = 8
    AppGlobals.setValue = 8
def fn_clickLabel_9():
    sliderSetValue.int_value = 9
    AppGlobals.setValue = 9
def fn_clickLabel_10():
    sliderSetValue.int_value = 10
    AppGlobals.setValue = 10
def fn_clickLabel_11():
    sliderSetValue.int_value = 11
    AppGlobals.setValue = 11
def fn_clickLabel_12():
    sliderSetValue.int_value = 12
    AppGlobals.setValue = 12
def fn_clickLabel_13():
    sliderSetValue.int_value = 13
    AppGlobals.setValue = 13
def fn_clickLabel_14():
    sliderSetValue.int_value = 14
    AppGlobals.setValue = 14
def fn_clickLabel_15():
    sliderSetValue.int_value = 15
    AppGlobals.setValue = 15
def fn_clickLabel_16():
    sliderSetValue.int_value = 16
    AppGlobals.setValue = 16
fnClickLabels = [fn_clickLabel_0, fn_clickLabel_1, fn_clickLabel_2, fn_clickLabel_3, fn_clickLabel_4, fn_clickLabel_5, fn_clickLabel_6, fn_clickLabel_7, fn_clickLabel_8, fn_clickLabel_9, fn_clickLabel_10, fn_clickLabel_11, fn_clickLabel_12, fn_clickLabel_13, fn_clickLabel_14, fn_clickLabel_15, fn_clickLabel_16]
for i in range(17):
    btnColorLabels[i].set_on_clicked(fnClickLabels[i])

def fn_sliderSetValue_changed(value):
    AppGlobals.setValue = value
sliderSetValue.set_on_value_changed(fn_sliderSetValue_changed)


def update_labels_and_colors(idxs):
    idxs2 = np.array(idxs, dtype=np.int32)
    AppGlobals.lobj[3][idxs2] = AppGlobals.setValue
    AppGlobals.mesh.vertex_colors = TpO3d.Vector3dVector(labels_to_colors_crown(AppGlobals.lobj[3]))    
    scene3d.clear_geometry()
    scene3d.add_geometry("mesh", AppGlobals.mesh, material=TpO3d.MaterialRecord.lazyMaterialRecord())    
        
def resetCamera():
    scene.setup_camera(60, AppGlobals.mesh.get_axis_aligned_bounding_box(), [0, 0, 0])
    
# 雙擊時，開啟檔案
from Easy.LabeledObject import LabeledObject
from Easy.easyopen3d import easyo3d
def openLObj(path)->TpO3d.TriangleMesh:
    lobj = LabeledObject().read(path)
    AppGlobals.lobj = lobj
    
    mesh: TpO3d.TriangleMesh = easyo3d.toMesh2(lobj)
    easyo3d.doSop1ForMesh(mesh)
    
    mesh.compute_adjacency_list()
    AppGlobals.dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}
    
    kdtree = TpO3d.KDTreeFlann(mesh) # 兩種 sample都會用到
    AppGlobals.kdtree = kdtree
    AppGlobals.mesh = mesh
    
    # 計算，選取時要用的半徑，最大的 1/20
    r1 = np.max(mesh.vertices, axis=0)
    r2 = np.min(mesh.vertices, axis=0)
    AppGlobals.lenMaxMesh = np.max( r1-r2 )
    radius = AppGlobals.lenMaxMesh * AppGlobals.radius_percent # 約31個點
    AppGlobals.radius = radius
    
    sliderRadius.enabled = True
    sliderSetValue.enabled = True
    
    print("max min radius/40 ", r1, " " , r2 , " " , radius)
    
    UnDoReDo.clear_undo_and_redo()
    
    scene3d.clear_geometry()
    scene3d.add_geometry("mesh", mesh, material=TpO3d.MaterialRecord.lazyMaterialRecord())
    resetCamera()
    print("openLObj", path)
    
    app.post_to_main_thread(win3D, lambda: win3D.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示

def _listbox_changed_core(str:str, isDclick:bool, path_idds_ver:t.List[t.Tuple[str, int,int]], upperlower:str):
    if isDclick:
        ''' id_140_ver_12 '''
        strs = str.split('_')
        idd = int(strs[1])
        ver = int(strs[3])
        for path,idd2,ver2 in path_idds_ver:
            if idd2 == idd and ver2 == ver:
                AppGlobals.pathlobj = path
                AppGlobals.upper_lower = upperlower
                AppGlobals.idd = idd   
                AppGlobals.ver = ver                             
                
                openLObj(path)
                return

def fn_listbox_changed1(str:str, isDclick:bool):
    _listbox_changed_core(str, isDclick, path_idds_upper, "upper")
    
def fn_listbox_changed2(str:str, isDclick):
    _listbox_changed_core(str, isDclick, path_idds_lower, "lower")


    
def fn_list3_selected_changed(newvalue, isdb):
    if isdb:
        if newvalue == '..':
            AppGlobals.dirFileDialog = os.path.dirname(AppGlobals.dirFileDialog)
            enum_and_set_list3()
        else:
            path = AppGlobals.dirFileDialog + '/' + newvalue
            if os.path.isdir(path):
                AppGlobals.dirFileDialog = path
                enum_and_set_list3()
            else:
                print('file')
                AppGlobals.upper_lower = "other"                
                AppGlobals.pathlobj = path
                openLObj(path)
        
list1.set_on_selection_changed(fn_listbox_changed1)
list2.set_on_selection_changed(fn_listbox_changed2)
list3.set_on_selection_changed(fn_list3_selected_changed)    


def get_adjacencys(idxSeed: int, count_recursive: int, dict_adjacency: t.Dict[int, t.List[int]], already_search = None) -> t.List[int]:
    ''' 取得相鄰的點，包含自己
    '''
    if already_search is None:
        already_search = np.full(len(dict_adjacency), False)
        
    if count_recursive == 0:
        return [idxSeed]
    else:        
        lst = dict_adjacency[idxSeed]
        lst2 = [idxSeed]
        
        for idx in lst:            
            if already_search[idx] == False:
                already_search[idx] = True
                lst2.extend(get_adjacencys(idx, count_recursive-1, dict_adjacency, already_search))                    
        
        return list(set(lst2)) # 去除重複的


# 右鍵點擊，設定 label，並更新顏色
def fn_mouse_event(event: TpO3d.MouseEvent)->TpO3d.Widget.EventCallbackResult:
    if event.type == TpO3d.MouseEvent.Type.WHEEL:
        # 滾輪
        if event.is_modifier_down(TpO3d.KeyModifier.SHIFT):            
            if event.wheel_dy > 0:
                AppGlobals.count_recursive += 1
            elif event.wheel_dy < 0:
                AppGlobals.count_recursive -= 1
            
            if AppGlobals.count_recursive < 1:
                AppGlobals.count_recursive = 1
            elif AppGlobals.count_recursive > sliderCountRecursive.get_maximum_value:
                AppGlobals.count_recursive = sliderCountRecursive.get_maximum_value
            
            sliderCountRecursive.int_value = int(AppGlobals.count_recursive)
            app.post_to_main_thread(winSettings, lambda: winSettings.post_redraw())
            return TpO3d.Widget.EventCallbackResult.CONSUMED        
        elif event.is_modifier_down(TpO3d.KeyModifier.CTRL):
            if event.wheel_dy > 0:
                AppGlobals.setValue += 1
            elif event.wheel_dy < 0:
                AppGlobals.setValue -= 1
            
            if AppGlobals.setValue < 0:
                AppGlobals.setValue = 0
            elif AppGlobals.setValue > 16:
                AppGlobals.setValue = 16
                
            sliderSetValue.int_value = int(AppGlobals.setValue)
            app.post_to_main_thread(winSettings, lambda: winSettings.post_redraw())
            return TpO3d.Widget.EventCallbackResult.CONSUMED
            
    def fn_img(depth_image: TpO3d.Image):
        img = np.array(depth_image)
        u = event.x - scene.frame.x
        v = event.y - scene.frame.y
        z = img[v][u]
        
        if z == 1.0: # 沒找到
            print('no click anything u', u, ' v', v)
        else:
            if AppGlobals.isDragPick == False:                
                UnDoReDo.push_to_undo_and_clear_redo(AppGlobals.lobj[3])
            
            pt = scene3d.camera.unproject(u, v, z, scene.frame.width, scene.frame.height)
            print(f'u {u} v {v} z {z} pt:{pt[0]} {pt[1]} {pt[2]}')
                        
            # method 1
            if AppGlobals.tpMethod == 0:
                kdtree = AppGlobals.kdtree                    
                radius = AppGlobals.radius                                    
                re = kdtree.search_radius_vector_3d(pt, radius)                                       
                update_labels_and_colors(re[1])
            elif AppGlobals.tpMethod == 1:
                kdtree = AppGlobals.kdtree
                re = kdtree.search_knn_vector_3d(pt, 1)
                idxs = get_adjacencys(re[1][0], AppGlobals.count_recursive, AppGlobals.dict_adjacency)                
                update_labels_and_colors(idxs)        
    if event.type == TpO3d.MouseEvent.Type.BUTTON_DOWN and event.is_button_down(TpO3d.MouseButton.RIGHT):
        AppGlobals.isDragPick = False
        scene3d.scene.render_to_depth_image(fn_img)        
        return TpO3d.Widget.EventCallbackResult.CONSUMED
    if event.type == TpO3d.MouseEvent.Type.DRAG and event.is_button_down(TpO3d.MouseButton.RIGHT):
        AppGlobals.isDragPick = True
        scene3d.scene.render_to_depth_image(fn_img)     
        return TpO3d.Widget.EventCallbackResult.CONSUMED        
    return TpO3d.Widget.EventCallbackResult.IGNORED
scene.set_on_mouse(fn_mouse_event)


def fn_key_event(event: TpO3d.KeyEvent)->TpO3d.Widget.EventCallbackResult:    
    if event.type == TpO3d.KeyEvent.Type.DOWN:
        if event.key == TpO3d.KeyName.Y:
            # redo
            data = UnDoReDo.pop_from_redo_and_push_to_undo()
            if data is None:
                return TpO3d.Widget.EventCallbackResult.IGNORED
            
            AppGlobals.lobj[3][:] = data[:]
            AppGlobals.mesh.vertex_colors = TpO3d.Vector3dVector(labels_to_colors_crown(AppGlobals.lobj[3]))
            scene3d.clear_geometry()
            scene3d.add_geometry("mesh", AppGlobals.mesh, material=TpO3d.MaterialRecord.lazyMaterialRecord())    
            app.post_to_main_thread(win3D, lambda: win3D.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示
            
        if event.key == TpO3d.KeyName.Z:
            # undo
            data = UnDoReDo.pop_from_undo_and_push_to_redo()
            if data is None:
                return TpO3d.Widget.EventCallbackResult.IGNORED
            
            AppGlobals.lobj[3][:] = data[:]
            AppGlobals.mesh.vertex_colors = TpO3d.Vector3dVector(labels_to_colors_crown(AppGlobals.lobj[3]))    
            scene3d.clear_geometry()
            scene3d.add_geometry("mesh", AppGlobals.mesh, material=TpO3d.MaterialRecord.lazyMaterialRecord())    
            app.post_to_main_thread(win3D, lambda: win3D.post_redraw()) # 沒有 post_redraw 時，要滑鼠移過去才會顯示
        if event.key == TpO3d.KeyName.R:
            # reset camera
            if AppGlobals.mesh is not None:
                resetCamera()
                app.post_to_main_thread(win3D, lambda: win3D.post_redraw())
    
    return TpO3d.Widget.EventCallbackResult.IGNORED
scene.set_on_key(fn_key_event)

# 兩個視窗一起關
def fn_close():
    app.quit() 
win3D.set_on_close(fn_close)

app.run()