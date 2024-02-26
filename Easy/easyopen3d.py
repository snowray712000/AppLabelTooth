import numpy as np
import numpy.typing as npt
import open3d
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
from .ColorsForCrown import labels_to_colors_crown
from .LabeledObject import LabeledObject
import platform # 判定是不是 Mac ， 對 gui 的 menu 來說是很重要的

from . import TpO3d

# 這個方法好，可以成功，且可以有自動完成，並且不能寫在函式中，一定要寫成全域
import typing as t
TpGui = open3d.cpu.pybind.visualization.gui
TpWindow = TpGui.Window
TpSceneWidget = TpGui.SceneWidget
TpOpen3DScene = open3d.cpu.pybind.visualization.rendering.Open3DScene
TpScene = open3d.cpu.pybind.visualization.rendering.Scene # demo 4 會用
TpMouseEvent = TpGui.MouseEvent
TpCamera = open3d.cpu.pybind.visualization.rendering.Camera # demo 4 會用
TpImage = open3d.cpu.pybind.geometry.Image # 深度取得時會用
TpMenu = TpGui.Menu
    
def _farthest_point_down_sample(vertexs,count) -> np.array:
    ''' 雖然，最遠點採樣本質是用 PointCloud，但為了讓 Mesh 也能用，所以 input 設計為 vertexs'''
    def search_nearest_indexs_from_mesh(points, kdtree):
        ''' 從 mesh 中找對應的 index, 才能找到對應的 labels '''
        return np.array( [kdtree.search_knn_vector_3d(a1,1)[1][0] for a1 in points] , dtype = np.int32)

    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector( vertexs )

    pc2 = pc.farthest_point_down_sample(count)
    kdtree = o3d.geometry.KDTreeFlann(pc) # 兩種 sample都會用到
    index_sample = search_nearest_indexs_from_mesh(pc2.points, kdtree)
    return index_sample

def _doSop1ForPointCloud(pc: o3d.geometry.PointCloud):
    ''' remove duplicated vertices, nan vertices '''
    pc.remove_duplicated_points()
    pc.remove_non_finite_points()

def _doSop1ForMesh(mesh: o3d.geometry.TriangleMesh):
    ''' remove duplicated vertices, degenerate triangles, computer normals
    '''
    mesh.remove_duplicated_vertices()
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()


def _toMesh(vertexs, triangles, labels=None, isDoSop: bool = True)->TpO3d.TriangleMesh:
    mesh = TpO3d.TriangleMesh()
    mesh.vertices = TpO3d.Vector3dVector(vertexs)
    mesh.triangles = TpO3d.Vector3iVector(triangles)
    # mesh.vertices = o3d.utility.Vector3dVector(vertexs)
    # mesh.triangles = o3d.utility.Vector3iVector(triangles)
    if labels is not None:
        mesh.vertex_colors = TpO3d.Vector3dVector(
            labels_to_colors_crown(labels))
    if isDoSop:
        _doSop1ForMesh(mesh)
    return mesh


def _render(obj):
    axis = o3d.geometry.TriangleMesh.create_coordinate_frame(
        min(obj.get_max_bound() - obj.get_min_bound()))
    o3d.visualization.draw_geometries(
        [axis, obj], mesh_show_back_face=True, point_show_normal=True, mesh_show_wireframe=False)


def _rotate180x(obj):
    # 创建一个单位矩阵
    transformation = np.identity(4)
    # 在x轴上旋转180度（弧度）
    angle = np.pi
    rotation_matrix = np.array([[1, 0, 0, 0],
                                [0, np.cos(angle), -np.sin(angle), 0],
                                [0, np.sin(angle), np.cos(angle), 0],
                                [0, 0, 0, 1]])
    transformation[:3, :3] = rotation_matrix[:3, :3]

    # 应用变换到几何体
    obj.transform(transformation)
    return obj

def _easyGuiInitial(fnLoad: t.Callable[[TpO3d.Window,TpO3d.SceneWidget,TpO3d.Open3DScene], t.NoReturn]):
  ''' 由 _231129b.py demo1 demo2 重構而來，留簡單版本的，方便學弟看程式演化 
  - 可使用 patter `def _onload(window:TpWindow,widget3d: TpSceneWidget, scene3d: TpOpen3DScene)`:
  '''
  app = TpO3d.Application()
  app.initialize()
  window = app.create_window("Add Spheres Example", 1024, 768)
  
  widgetScene = TpO3d.SceneWidget()
  window.add_child(widgetScene)
  
  scene3d = TpO3d.Open3DScene(window.renderer)
  widgetScene.scene = scene3d
  
  fnLoad(window, widgetScene, scene3d)

  app.run()  

def _isMacOs()->bool:
  ''' gui 的 menu, mac 是 global, 所有視窗都共用一個 '''
  return (platform.system() == "Darwin")


class EasyGUI:
  ''' 要同時自訂 keyboard mouse ，還要自訂 menu ui，就必需使用這個，並且還不能用 jupyter 的 ctrl+M 模式 
  - 當初為了要 Label 3D 的資料，因為找不到合適的工具，就想自己作一個。也同時練習 open3d 的介面開發。
  '''
  def __init__(self):
    self._window: TpO3d.Window = None
    self._widget3d: TpO3d.SceneWidget = None
    self._scene3d: TpO3d.Open3DScene = None    
    ''' 本質就是 widget3d.scene。 '''
    self._scene: TpO3d.Scene = None
    ''' 重點函式 render_to_depth_image render_to_image '''
    self._camera: TpO3d.Camera = None
    ''' 從 u,v,d 轉為 x,y,z 會用到它的 unproject '''
    pass
  def or_generate_menu_when_on_load(self):
    ''' 初始化 menu 可用這個
    - 會用到 gui.Menu() 並且 add_item add_menu 兩個函式 來描述
    - 最後要有一個設定為 self._menubar
    - 設對應的 callback，要用 self._window set_on_menu_item_activated
    - 可使用 EasyGUIMenu 來作
    '''
    print('overrider or_generate_menu_when_on_load')

  def or_add_data_when_on_load(self):
    ''' override this. or: override
    通常，載入 資料 很適合。
    '''    
    print('overrider or_add_data_when_on_load')
  def or_when_right_click_pick(self, pt: npt.NDArray[np.float32]):
    ''' or: override    
    - 滑鼠右鍵，當有點擊到物體時，才會觸發此函式
    - 通常，你會建立 kdtree，搜尋所點擊到的點
    '''
    print(pt) # np.array
    print('overrider or_when_right_click_pick')  

  def main(self):
    self._initial()
  @property
  def _menubar(self)->TpO3d.Menu:
      return TpO3d.Application().menubar
  @_menubar.setter
  def _menubar(self,new_value: TpMenu):
      if self._menubar is not None:
          print('menubar asseert is none')
      TpO3d.Application().menubar = new_value    
  def _on_mouse(self, event: TpO3d.MouseEvent):
    def _on_depth_callback(depth_image: TpImage):
      # http://www.open3d.org/docs/release/python_example/visualization/index.html?highlight=draw_geometries_with_editing#mouse-and-point-coord-py 
      # print(type(depth_image)) # open3d.cpu.pybind.geometry.Image
      widget3d = self._widget3d

      # print(depth_image)  
      img = np.array(depth_image)
      
      # print(img.shape)
      u = event.x - widget3d.frame.x
      v = event.y - widget3d.frame.y
      z = img[v][u]
      if z == 1.0: # 沒找到
        print('no click anything u', u, ' v', v)
      else:
        pt = self._camera.unproject(u, v, z, widget3d.frame.width, widget3d.frame.height)
        self.or_when_right_click_pick(pt)
        print(f'u {u} v {v} z {z} pt:{pt[0]} {pt[1]} {pt[2]}')
    isButtonDown = event.type == gui.MouseEvent.Type.BUTTON_DOWN # 只有一瞬間，若按著移動，那叫作 Drag
    isRightButton = event.is_button_down(gui.MouseButton.RIGHT)      
    if isButtonDown and isRightButton:        
      self._scene.render_to_depth_image(_on_depth_callback)
      return gui.Widget.EventCallbackResult.CONSUMED
    return gui.Widget.EventCallbackResult.IGNORED

  def _on_load(self, window: TpO3d.Window, widget3d: TpO3d.SceneWidget, scene3d: TpO3d.Open3DScene): 
    self._window = window
    self._widget3d = widget3d
    self._scene3d = scene3d
    self._scene = self._scene3d.scene
    self._camera = self._scene3d.camera
    
    self._widget3d.set_on_mouse(self._on_mouse)
    
    self.or_generate_menu_when_on_load()
    self.or_add_data_when_on_load()

  def _initial(self):
    _easyGuiInitial(self._on_load)


class EasyGUIMenu:
    """
    產生 menu 。
    ```python=
        def fn1_filedialog():
            print('fn1')
            pass
        def fn2_dialog():
            print('fn2')
            pass
        menus = [{'na': 'file', 'sub':[
            {'na':'file dialog', 'fn': fn1_filedialog},
            {'na':'dialog', 'fn': fn2_dialog}
        ]}]
        
        EasyGUIMenu.main(self, menus)      
    ```
    
    """
    menu_id = 0
    map_id_fn = {}

    def __init__(self):
        pass

    @staticmethod
    def main(easyGui: EasyGUI, menu_description):
        ''' 產生並設定callback，static method
        - parameters
          - easyGui: 通常就是傳 self，因為要用到 window 指標
          - menu_description: 要傳 [{"na":"File","sub":[]}] 之類的描述檔
        '''
        def gMenu(menu_description)->TpMenu:
            menu: TpMenu = gui.Menu()
            map1 = EasyGUIMenu.map_id_fn
            for a1 in menu_description:
                na = a1['na']
                if 'sub' in a1:                    
                    menu.add_menu(na, gMenu(a1['sub'])[0] )
                else:
                    idd = EasyGUIMenu.menu_id

                    map1[idd] = a1['fn']
                    menu.add_item(na, idd)
                    EasyGUIMenu.menu_id = idd + 1
            return menu, map1
        
        # recursive 產生資料
        menu, map1 = gMenu(menu_description)

        easyGui._menubar = menu
        win = easyGui._window
        for idd, fn in map1.items():
            win.set_on_menu_item_activated(idd, fn)

class easyo3d:
    ''' 這個 class 有點像 namesapce 的概念，有這個，並結合 auto complete 功能，大概就能知道有哪些工具可用 '''
    def rotate180x(obj):
        return _rotate180x(obj)

    def render(obj):
        _render(obj)

    def toMesh(vertexs, triangles, labels=None, isDoSop=True) -> TpO3d.TriangleMesh:
        """ 轉為 triangles mesh 。 SOP: 除去重複點，計算頂點、平面法向量。若含 labels 則會上色 """
        return _toMesh(vertexs, triangles, labels, isDoSop=isDoSop)

    def toMesh2(lobj: LabeledObject, isDoSop=True) ->TpO3d.TriangleMesh:
        """ toMesh(lobj[0], lobj[5], lobj[3] ... 
        轉為 triangles mesh 。 SOP: 除去重複點，計算頂點、平面法向量。若含 labels 則會上色
        """
        return _toMesh(lobj[0], lobj[5], lobj[3], isDoSop=isDoSop)
    
    def toPointCloud(vertexs, normals, colors = None)->o3d.geometry.PointCloud:
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(vertexs)
        if normals is not None:
            pc.normals = o3d.utility.Vector3dVector(normals)
        if colors is not None:
            pc.colors = o3d.utility.Vector3dVector(colors)
        return pc

    def doSop1ForMesh(mesh: TpO3d.TriangleMesh):
        ''' remove duplicated vertices, degenerate triangles, computer normals
        '''
        _doSop1ForMesh(mesh)

    def doSop1ForPointCloud(pc: TpO3d.PointCloud):
        ''' remove duplicated vertices, nan vertices '''
        _doSop1ForPointCloud(pc)

    def farthest_point_down_sample(vertexs,count) -> np.array:
        ''' 雖然，最遠點採樣本質是用 PointCloud，但為了讓 Mesh 也能用，所以 input 設計為 vertexs'''
        return _farthest_point_down_sample(vertexs,count)

class easygui:
    def initial(fnLoad: t.Callable[[TpWindow,TpSceneWidget,TpOpen3DScene], t.NoReturn]):
        ''' 由 _231129b.py demo1 demo2 重構而來，留簡單版本的，方便學弟看程式演化 
        - 可使用 patter `def _onload(window:TpWindow,widget3d: TpSceneWidget, scene3d: TpOpen3DScene)`:
        '''
        _easyGuiInitial(fnLoad)