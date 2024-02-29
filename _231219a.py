#%%
from Easy import *
from Easy.search_label_from_nearest import search_label_from_nearest
import open3d as o3d
import glob
import requests

#%% GlobalValue
class AppGlobals:
    pathlobj: str
    '''開啟的 pathlobj '''
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
        exts = ['.lobj', '.stl']
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

# 預測
hstackInfer = TpO3d.Horiz()
vert1.add_child(hstackInfer)

btnInfer = TpO3d.Button("預測")
hstackInfer.add_child(btnInfer)

# method 選擇
tpInfer = TpO3d.RadioButton(TpO3d.RadioButton.Type.HORIZ)
hstackInfer.add_child(tpInfer)
tpInfer.set_items(["未知", "下顎", "上顎"]) # 0 1 2
tpInfer.selected_index = 0

# 使用 .pts
btnUsePtsFileLabel = TpO3d.Button("使用.pts")
hstackInfer.add_child(btnUsePtsFileLabel)

# 另存目前 lobj
btnSaveAs = TpO3d.Button("Save As")
vert1.add_child(btnSaveAs)

# label -1 設定為最接近顏色
btnAutoSetNoLabel = TpO3d.Button("Auto Set No Label")
vert1.add_child(btnAutoSetNoLabel)

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

listFiles = TpO3d.ListView()
vert1.add_child(listFiles)
listFiles.set_items(["" for _ in range(10)]) # 高度不再忽大忽小 (但最小化時，再放大會重算一次)
listFiles.set_max_visible_items(10)

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
app.post_to_main_thread(winSettings, lambda: (winSettings.post_redraw(),listFiles.set_items(AppGlobals.enumFiles()))) # 沒有 post_redraw 時，要滑鼠移過去才會顯示

#%% 
# callback functions 
from Easy.LabeledObject import LabeledObject
import os

def fn_clickHelp():
    winSettings.show_message_box("Help", """選取檔案：雙擊清單。
                                 滑鼠左鍵，旋轉。
                                 Ctrl+左滑鼠鍵，平移。
                                 滑鼠右鍵，設定 label。
                                 滑鼠滾輪，縮放。
                                 滑鼠滾輪+Shift，設定影響半徑。
                                 滑鼠滾輪+Ctrl，設定 label id。
                                 Z，undo。Y，redo。
                                 
                                 預測功能，是給 stl 檔案用的。
                                 """)
btnHelp.set_on_clicked(fn_clickHelp)

def filter_before_infer()->t.Optional[npt.NDArray[np.bool8]]:
    """ 回傳 null 表示不用過濾，用所有的 """
    # 確認 upperlower, 從 tpInfer
    assert( tpInfer.selected_index != 0 )
    
    upperlower = "lower"
    if tpInfer.selected_index == 2:
        upperlower = "upper"
    
    # 
    mesh = AppGlobals.mesh
    lobj = AppGlobals.lobj
    points = lobj[0]
    normals = np.array(mesh.vertex_normals)
    z = points[:, 2] # 加效率
    zlimit = np.min(z) if upperlower == 'lower' else np.max(z)
    
    # 確認是否有底
    def isHasBottom():
        count = np.sum( z == zlimit )
        return count > 20 # 通常 200 個以上
    
    if isHasBottom() == False:
        return None
    
    def get_idx_of_vertex_for_calc_avg_std_z(lobj, upperlower, mesh:TpO3d.TriangleMesh):
        assert ( mesh.has_vertex_normals() )
        
        # 建相鄰，約1秒
        if mesh.has_adjacency_list() == False:
            mesh.compute_adjacency_list() 
        dict_adjacency = {i: lst for i, lst in enumerate(mesh.adjacency_list)}
        
        # 外部也有，因此共用下3行
        ## 2個算法，共用資料(提升效率，只作一次)
        # z = lobj[0][:, 2] 
        # normals = np.array(mesh.vertex_normals)
       
        # 外部也有，因此共用下1行
        # zlimit = np.min(z) if upperlower == 'lower' else np.max(z)
        
        def get_exclude_bottom_idx():
            idxs = z == zlimit
            idxs1 = np.arange(len(z))[idxs] # [T T F F T] -> [0 1 4]
            idxs2 = lq.linq(idxs1).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
            idxs13 = lq.linq(idxs2).select_many(lambda x: dict_adjacency[x]).distinct().to_list()
            idxs123 = list(set(idxs13 + idxs2))
            re = np.full(len(z), True)
            re[idxs123] = False
            return re
        def get_normal_change_big_idx():
            min_dots: t.List[float] = []
            for i in range(len(lobj[0])):
                # 取得相鄰頂點的法向量
                normals2 = np.array([normals[i] for i in dict_adjacency[i]])
                # 計算 dot
                dots = np.dot(normals2, normals[i])
                # 取得最小的
                min_dot = np.min(dots)
                min_dots.append(min_dot)
            re = np.array(min_dots) < 0.95
            return re
        
        return get_exclude_bottom_idx() & get_normal_change_big_idx()        
    
    # 計算 std avg
    idxs = get_idx_of_vertex_for_calc_avg_std_z(lobj, upperlower, mesh)
    z2 = z[idxs]
    avg, std = np.mean(z2), np.std(z2)
    
    # filter
    idxsExcludeOutlier = z > (avg - 3 * std) if upperlower == 'lower' else z < (avg + 3 * std)
    return idxsExcludeOutlier
    
def fn_clickInfer():
    # try except
    try:
        # 檢查 tpInfer
        assert ( AppGlobals.mesh != None and AppGlobals.lobj != None )
        if tpInfer.selected_index == 0:
            winSettings.show_message_box("中斷", "檔名沒有upper 或 lower 字眼，請手動選擇上顎或下顎。")
            return
        # popup 訊息
        # winSettings.show_message_box("預測", "大約需要 10 秒，請耐心等待，按下確定後開始。")，沒用，這是最後才跳出來
        
        # 使用文件上傳方式發送POST請求
        url = 'http://140.123.121.21:443/toothgum_seg-api/infer/lower_tooth/point_cloud/'
        if tpInfer.selected_index == 2:
            url = 'http://140.123.121.21:443/toothgum_seg-api/infer/upper_tooth/point_cloud/'
        def inferAndreturnResponse():
            mesh = AppGlobals.mesh
            lobj = AppGlobals.lobj
            idxsFilter = filter_before_infer()
            if idxsFilter is None:
                vertexs = lobj[0]
                normals = np.array( mesh.vertex_normals, dtype=np.float32 )
            else:
                vertexs = np.array( lobj[0][idxsFilter] , dtype=np.float32 )
                normals = np.array( np.array(mesh.vertex_normals)[idxsFilter], dtype=np.float32 )
            xyznnnUpload = np.hstack([vertexs,normals]) # pc upload 測試用
            files = {'stl_file': xyznnnUpload.tobytes()}
            datas = {'mode': 'lower'} # 其實沒用到
            response = requests.post(url, files=files, data=datas)
            return response
        response = inferAndreturnResponse()
        
        # 檢查響應狀態碼
        if response.status_code == 200:
            print('請求成功！')
        else:
            print(f'請求失敗，狀態碼：{response.status_code}')
            winSettings.show_message_box("Error", f"請求失敗，狀態碼：{response.status_code}")
            return 
        print(response.headers)
        print(response.text[:256])
    except Exception as ex:
        winSettings.show_message_box("Error", f"Error: {ex}")
        return 
    
    # text 是 x y z label 一行，所以要 parse
    def text_to_data(text: str)->t.Tuple[npt.NDArray[np.float32], npt.NDArray[np.int8]]:
        r1 = text.split("\n")
        pts = np.array( [[float(a2) for a2 in x.split(",")[:3]] for x in r1], dtype=np.float32)
        labels = np.array( [float(x.split(",")[-1]) for x in r1], dtype=np.int8 )
        return pts, labels
    pts, labels = text_to_data(response.text)
    
    # 更新目前 mesh 的 labels ， 用 pts 與 labels  建 kdtree & 找最近點。
    lobj = AppGlobals.lobj
    labels2 = search_label_from_nearest(pts,labels, lobj[0], 1.0)
    
    # 更新 lobj
    AppGlobals.lobj = (lobj[0], lobj[1], lobj[2], labels2, lobj[4], lobj[5], lobj[6])
    
    # 更新 mesh
    update_labels_and_colors([])
    
    
btnInfer.set_on_clicked(fn_clickInfer)

def fn_labelUsePtsFile():
    path = AppGlobals.pathlobj
    
    # 替換副檔名 .stl -> .pts
    pathPts = os.path.splitext(path)[0] + ".pts"
    
    # 確認檔案存在嗎
    if os.path.exists(pathPts) == False:
        # 檔案不存在, msgbox
        winSettings.show_message_box("Error", f"{pathPts} 不存在。")
    else:
        with open(pathPts, 'r') as f:
            lines = f.readlines()
            
            # , 隔開, x,y,z,label
            xyzs = np.array( [[float(a2) for a2 in a1.split(",")[:3]] for a1 in lines] )
            labels = np.array( [float(a1.split(",")[-1]) for a1 in lines] , dtype=np.int8 )
            
            labels[labels == -1] = 0
            
            lobj = AppGlobals.lobj
            labelsResult = search_label_from_nearest(xyzs, labels, lobj[0], None)
            
            lobj = (lobj[0], None, None, labelsResult, None, lobj[5], None)
            AppGlobals.lobj = lobj
            AppGlobals.mesh.vertex_colors = TpO3d.Vector3dVector(labels_to_colors_crown(lobj[3]))
            
            # 更新 mesh
            update_labels_and_colors([])
            


btnUsePtsFileLabel.set_on_clicked(fn_labelUsePtsFile)

def enum_and_set_listFiles():
    """ 產生給  ListView 用的資料 
    - 使用 AppGlobals.dirFileDialog 路徑資料。
    """
    listFiles.set_items(AppGlobals.enumFiles())
    
def reload_and_update_listboxview():
    basename = os.path.basename(AppGlobals.pathlobj)
    names = AppGlobals.enumFiles()
    listFiles.set_items(names)
    
    def fn_first1(a1: t.Tuple[int,str]):
        return a1 == basename
    re: t.Tuple[int,str] = lq.linque( enumerate(names) ).first(fn_first1)
    listFiles.selected_index = re[0]
    
def generate_filename(path, dir):
    base_name = os.path.basename(path)  # 從路徑中提取檔名    
    name, ext = os.path.splitext(base_name)  # 分離檔名和副檔名
    
    # 如果是 .stl 取直接換副檔名，並且取代現有的 .lobj
    if ext == ".stl":
        return name + ".lobj"
    
    # .lobj 才有針對 fixed 的處理
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
        
        # 若是 stl, 要變更全域變數，下次存，才會是 fixed
        if path2.endswith(".lobj"):
            AppGlobals.pathlobj = dir + '/' + path2
        
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
    if len(idxs) != 0:
        idxs2 = np.array(idxs, dtype=np.int32)
        AppGlobals.lobj[3][idxs2] = AppGlobals.setValue
    AppGlobals.mesh.vertex_colors = TpO3d.Vector3dVector(labels_to_colors_crown(AppGlobals.lobj[3]))    
    scene3d.clear_geometry()
    scene3d.add_geometry("mesh", AppGlobals.mesh, material=TpO3d.MaterialRecord.lazyMaterialRecord())   
    app.post_to_main_thread(win3D, lambda: win3D.post_redraw()) 
        
def resetCamera():
    scene.setup_camera(60, AppGlobals.mesh.get_axis_aligned_bounding_box(), [0, 0, 0])

def set_nolabel_to_nearest_label(lobj):
    v1: npt.NDArray[np.float32] = lobj[0]
    l1: npt.NDArray[np.int8]  = lobj[3]
    
    # 取得有標籤的點雲，並建立KDTree
    idx1 = l1 != -1
    v2 = v1[idx1]
    l2 = l1[idx1] # 後面會用到
    pc = TpO3d.PointCloud()
    pc.points = TpO3d.Vector3dVector(v2)
    kdtree = TpO3d.KDTreeFlann(pc) # 後面會用到
    
    # 取得沒有標籤的點雲，並找出最近的標籤
    idx2 = l1 == -1
    v3 = v1[idx2]
    if len(v3) != 0:
        idx3 = np.array([kdtree.search_knn_vector_3d(a1,1)[1][0] for a1 in v3])        
        l1[idx2] = l2[idx3] # 完成
    
    # 驗證
    # from Easy.easyopen3d import easyo3d
    # easyo3d.render(easyo3d.toMesh2(lobj))
def fn_click_auto_set_no_label():
    if AppGlobals.lobj is not None:        
        set_nolabel_to_nearest_label(AppGlobals.lobj)
        update_labels_and_colors([])
btnAutoSetNoLabel.set_on_clicked(fn_click_auto_set_no_label)
    
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
def openBinarySTL(path)->TpO3d.TriangleMesh:   
    with open(path,'rb') as fp: 
        mesh = readStlBinary_ToO3dMesh(fp)
    
    lobj = (np.array(mesh.vertices), None, None, None, None, np.array(mesh.triangles), None)
    AppGlobals.lobj = lobj
    
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
    print("openBinarySTL", path)
    
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

def fn_listFiles_selected_changed(newvalue, isdb):
    if isdb:
        if newvalue == '..':
            AppGlobals.dirFileDialog = os.path.dirname(AppGlobals.dirFileDialog)
            enum_and_set_listFiles()
        else:
            path = AppGlobals.dirFileDialog + '/' + newvalue
            if os.path.isdir(path):
                AppGlobals.dirFileDialog = path
                enum_and_set_listFiles()
            else:
                print('file')
                AppGlobals.upper_lower = "other"                
                AppGlobals.pathlobj = path
                # 判斷 副檔名 .stl 或 .lobj
                if path.endswith('.stl'):
                    openBinarySTL(path)
                elif path.endswith('.lobj'):
                    openLObj(path)
                    
                # path 若有 lower 或 upper 字樣，就能判定 tpInfer
                # path 要先取得 filename
                filename = os.path.basename(path).lower()
                if "lower" in filename:
                    tpInfer.selected_index = 1
                elif "upper" in filename:
                    tpInfer.selected_index = 2
                else:
                    tpInfer.selected_index = 0
        
listFiles.set_on_selection_changed(fn_listFiles_selected_changed)    


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