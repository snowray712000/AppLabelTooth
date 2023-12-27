from __future__ import annotations # Menu 使用 Menu ，當然，也可以直接使用 Self
"""
for python auto completed in VSCode
author: @snowray712000
"""
#%%
import typing as t
from enum import Enum, IntEnum
import numpy as np
import numpy.typing as npt
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering

class NoValue(Enum):
    ''' 舊版還沒有 StrEnum，使用此來達成，這是官網教的。 '''
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)
#%%
# io
class IoModule:
    ''' 用法 IoModule().read_triangle_mesh 
    - IoModule() 其實就是回傳 o3d.io 不會真的配記憶體
    '''
    def __new__(cls) -> Self:
        return o3d.io
    
    def read_triangle_mesh(self,filename: str, enable_post_processing: bool = False, print_progress: bool = False)->TriangleMesh:
        
        pass
        
#%%
# data
class PLYPointCloud:
    def __new__(cls, data_root: str = ""):
        return o3d.data.PLYPointCloud()
    @property
    def data_root(self)->str:
        pass
    @property
    def download_dir(self)->str:
        '''${data_root}/${download_prefix}/${prefix}'''
        pass
    @property
    def extract_dir(self)->str:
        '''${data_root}/${extract_dir}/${prefix}'''
        pass
    @property
    def path(self)->str:
        ''' 通常是用這個 .ply '''
        pass
    @property
    def prefix(self)->str:
        pass
class BunnyMesh(PLYPointCloud):
    def __new__(cls):
        return o3d.data.BunnyMesh()
    
#%%
# utility
class DoubleVector:    
    """float64 array"""
    def append(self, x: float):
        """Add an item to the end of the list"""
        pass
    def clear(self):
        """Clear the contents"""
        pass
    def count(self, x: float)->int:
        """Return the number of times x appears in the list"""
        pass
    def extend(self, L: DoubleVector):
        """Extend the list by appending all the items in the given list"""
        pass
    def insert(self, i: int, x: float):
        """Insert an item at a given position."""
        pass
    def pop(self,i :t.Optional[int])->float:
        """Remove and return the last item"""
        pass
    def remove(self, x: float):
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""
        pass
class IntVector(DoubleVector):
    pass
class Vector2dVector(DoubleVector):
    """Convert float64 numpy array of shape (n, 2) to Open3D format."""
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Vector2dVector(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.float64],Vector2dVector]):
        pass
    pass
class Vector2iVector(IntVector):
    """Convert int32 numpy array of shape (n, 2) to Open3D format.."""
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Vector2iVector(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.int32],Vector2iVector]):
        pass     
    
class Vector3dVector(DoubleVector):
    """Convert float64 numpy array of shape (n, 3) to Open3D format."""
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Vector3dVector(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.float64],Vector3dVector]):
        pass
    pass
class Vector3iVector(IntVector):
    """Convert int32 numpy array of shape (n, 3) to Open3D format.."""
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Vector3iVector(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.int32],Vector3iVector]):
        pass    
    
class Vector4iVector(IntVector):
    """Convert int32 numpy array of shape (n, 4) to Open3D format.."""
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Vector4iVector(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.int32],Vector4iVector]):
        pass    
class Matrix3dVector:
    '''Convert float64 numpy array of shape (n, 3, 3) to Open3D format.'''
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Matrix3dVector(*args, **kwargs)
    def __init__(self, arg0: t.Optional[t.Union[Matrix3dVector,t.Iterable]]):
        pass
    def append(self, x: npt.NDArray[np.float64[3,3]]):
        """Add an item to the end of the list"""
        pass
    def clear(self):
        """Clear the contents"""
        pass
    def count(self, x: npt.NDArray[np.float64[3,3]])->int:
        """Return the number of times x appears in the list"""
        pass
    def extend(self, L: t.Union[Matrix3dVector,t.Iterable]):
        """Extend the list by appending all the items in the given list"""
        pass
    def insert(self, i: int, x: npt.NDArray[np.float64[3,3]]):
        """Insert an item at a given position."""
        pass
    def pop(self,i :t.Optional[int])->npt.NDArray[np.float64[3,3]]:
        """Remove and return the last item or at index i"""
        pass
    def remove(self, x: npt.NDArray[np.float64[3,3]]):
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""
        pass

class Matrix4dVector:
    '''
classopen3d.utility.Matrix4dVector
Convert float64 numpy array of shape (n, 4, 4) to Open3D format.
    '''
    def __new__(cls, *args, **kwargs):
        return o3d.utility.Matrix4dVector(*args, **kwargs)
    def __init__(self, arg0: t.Optional[t.Union[Matrix4dVector,t.Iterable]]):
        pass
    def append(self, x: npt.NDArray[np.float64[4,4]]):
        """Add an item to the end of the list"""
        pass
    def clear(self):
        """Clear the contents"""
        pass
    def count(self, x: npt.NDArray[np.float64[4,4]])->int:
        """Return the number of times x appears in the list"""
        pass
    def extend(self, L: t.Union[Matrix4dVector,t.Iterable]):
        """Extend the list by appending all the items in the given list"""
        pass
    def insert(self, i: int, x: npt.NDArray[np.float64[4,4]]):
        """Insert an item at a given position."""
        pass
    def pop(self,i :t.Optional[int])->npt.NDArray[np.float64[4,4]]:
        """Remove and return the last item or at index i"""
        pass
    def remove(self, x: npt.NDArray[np.float64[4,4]]):
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""
        pass
#%%
# geometry
class AxisAlignedBoundingBox:
    '''
dimension(self)
Returns whether the geometry is 2D or 3D.

Returns
int

get_axis_aligned_bounding_box(self)
Returns an axis-aligned bounding box of the geometry.

Returns
open3d.geometry.AxisAlignedBoundingBox

get_box_points(self)
Returns the eight points that define the bounding box.

Returns
open3d.utility.Vector3dVector

get_center(self)
Returns the center of the geometry coordinates.

Returns
numpy.ndarray[numpy.float64[3, 1]]

get_extent(self)
Get the extent/length of the bounding box in x, y, and z dimension.

Returns
numpy.ndarray[numpy.float64[3, 1]]

get_geometry_type(self)
Returns one of registered geometry types.

Returns
open3d.geometry.Geometry.GeometryType

get_half_extent(self)
Returns the half extent of the bounding box.

Returns
numpy.ndarray[numpy.float64[3, 1]]

get_max_bound(self)
Returns max bounds for geometry coordinates.

Returns
numpy.ndarray[numpy.float64[3, 1]]

get_max_extent(self)
Returns the maximum extent, i.e. the maximum of X, Y and Z axis

Returns
float

get_min_bound(self)
Returns min bounds for geometry coordinates.

Returns
numpy.ndarray[numpy.float64[3, 1]]

get_oriented_bounding_box(self)
Returns an oriented bounding box of the geometry.

Returns
open3d.geometry.OrientedBoundingBox

get_point_indices_within_bounding_box(self, points)
Return indices to points that are within the bounding box.

Parameters
points (open3d.utility.Vector3dVector) – A list of points.

Returns
List[int]

get_print_info(self)
Returns the 3D dimensions of the bounding box in string format.

Returns
str    
    '''
    def dimension(self)->int:
        """Returns whether the geometry is 2D or 3D."""        
        pass
    
    pass

class DeformAsRigidAsPossibleEnergy:
    pass

class FilterScope:
    pass
r1 = AxisAlignedBoundingBox()

class Geometry:
    class Type:
        Unspecified: Geometry.Type = o3d.geometry.Geometry.Type.Unspecified
        PointCloud: Geometry.Type = o3d.geometry.Geometry.Type.PointCloud
        VoxelGrid: Geometry.Type = o3d.geometry.Geometry.Type.VoxelGrid
        HalfEdgeTriangleMesh: Geometry.Type = o3d.geometry.Geometry.Type.HalfEdgeTriangleMesh
        TriangleMesh: Geometry.Type = o3d.geometry.Geometry.Type.TriangleMesh
        LineSet: Geometry.Type = o3d.geometry.Geometry.Type.LineSet
        TetraMesh: Geometry.Type = o3d.geometry.Geometry.Type.TetraMesh
        Image: Geometry.Type = o3d.geometry.Geometry.Type.Image
        RGBDImage: Geometry.Type = o3d.geometry.Geometry.Type.RGBDImage        
        @property
        def value(self)->Geometry.Type:
            pass
        @value.setter
        def value(self, value: Geometry.Type):
            pass
    def clear(self)->Geometry:
        """Clear all elements in the geometry"""
        pass
    def dimension(self)->int:
        """Returns whether the geometry is 2D or 3D."""        
        pass
    def is_empty(self)->bool:
        """Returns True iff the geometry is empty."""        
        pass
    

class Geometry2D(Geometry):
    def get_max_bound(self)->npt.NDArray[np.float64[2,1]]:
        """Returns max bounds for geometry coordinates."""        
        pass
    def get_min_bound(self)->npt.NDArray[np.float64[2,1]]:
        """Returns min bounds for geometry coordinates."""        
        pass    

class Geometry3D(Geometry):
    def get_axis_aligned_bounding_box(self)->AxisAlignedBoundingBox:
        """Returns an axis-aligned bounding box of the geometry."""        
        pass
    def get_center(self)->npt.NDArray[np.float64[3,1]]:
        """Returns the center of the geometry coordinates."""        
        pass
    def get_max_bound(self)->npt.NDArray[np.float64[3,1]]:
        """Returns max bounds for geometry coordinates."""        
        pass
    def get_min_bound(self)->npt.NDArray[np.float64[3,1]]:      
        """Returns min bounds for geometry coordinates."""        
        pass
    def get_oriented_bounding_box(self)->OrientedBoundingBox:
        """Returns an oriented bounding box of the geometry."""        
        pass
    def rotate(self, R: t.Optional[npt.NDArray[np.float64[3,3]]], center: t.Optional[npt.NDArray[np.float64[3,1]]])->Geometry3D:
        """Apply rotation to the geometry coordinates and normals."""        
        pass
    def scale(self, scale: float, center: t.Optional[npt.NDArray[np.float64[3,1]]])->Geometry3D:
        """Apply scaling to the geometry coordinates."""        
        pass
    def transform(self, arg0: npt.NDArray[np.float64[4,4]]):
        """Apply transformation (4x4 matrix) to the geometry coordinates."""        
        pass
    def translate(self, translation: npt.NDArray[np.float64[3,1]], relative: bool = True)->Geometry3D:
        """Apply translation to the geometry coordinates."""        
        pass
    
    @staticmethod
    def get_rotation_matrix_from_axis_angle(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_quaternion(rotation: npt.NDArray[np.float64[4,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_xyz(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_xzy(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_yxz(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_yzx(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_zxy(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    @staticmethod
    def get_rotation_matrix_from_zyx(rotation: npt.NDArray[np.float64[3,1]])->npt.NDArray[np.float64[3,3]]:
        pass
    
class HalfEdge:
    pass

class HalfEdgeTriangleMesh:
    pass

class ImageFilterType:
    pass

class Image(Geometry2D):
    """geometry.Image"""
    def create_pyramid(self, num_of_levels: int, with_gaussian_filter: bool)->t.List[Image]:
        """Function to create ImagePyramid
        
        - Parameters:
            - num_of_levels (int) –
            - with_gaussian_filter (bool) – When True, image in the pyramid will first be filtered by a 3x3 Gaussian kernel before downsampling.
        """        
        pass
    def filter(self, filter_type: ImageFilterType)->Image:
        """Function to filter Image
        
        - Parameters:
            - filter_type (open3d.geometry.ImageFilterType) – The filter type to be applied.
        """        
        pass
    @staticmethod
    def filter_pyramid(image_pyramid: t.List[Image], filter_type: ImageFilterType)->t.List[Image]:
        """Function to filter ImagePyramid
        - Parameters:
            - image_pyramid (List[open3d.geometry.Image]) – The ImagePyramid object
            - filter_type (open3d.geometry.ImageFilterType) – The filter type to be applied.
        """        
        pass
    def flip_horizontal(self)->Image:
        """Function to flip image horizontally (from left to right)"""        
        pass
    def flip_vertical(self)->Image:
        """Function to flip image vertically (upside down)"""        
        pass
    

class ImageFilterType:
    Gaussian3: ImageFilterType = o3d.geometry.ImageFilterType.Gaussian3
    Gaussian5: ImageFilterType = o3d.geometry.ImageFilterType.Gaussian5
    Gaussian7: ImageFilterType = o3d.geometry.ImageFilterType.Gaussian7
    Sobel3dx: ImageFilterType = o3d.geometry.ImageFilterType.Sobel3dx
    Sobel3dy: ImageFilterType = o3d.geometry.ImageFilterType.Sobel3dy
    @property
    def value(self)->ImageFilterType:
        pass
    @value.setter
    def value(self, value: ImageFilterType):
        pass
    pass
class KDTreeSearchParam:
    ''' open3d.geometry.KDTreeSearchParam '''
    pass
class Feature:
    ''' open3d.pipelines.registration.Feature '''
    pass
class KDTreeFlann:
    def __new__(cls, *args, **kwargs):
        return o3d.geometry.KDTreeFlann(*args, **kwargs)
    def __init__(self, arg0: t.Union[npt.NDArray[np.float64],Geometry,Feature]):
        pass
    def search_hybrid_vector_3d(self, query: npt.NDArray[np.float64[3,1]], radius: float, max_nn: int)->t.Tuple[int,IntVector,DoubleVector]:
        """ Hybrid search for neighbors within a radius. If the number of neighbors found is less than max_nn, then kNN search is used. Otherwise, radius search is used. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_hybrid_vector_xd(self, query: npt.NDArray[np.float64], radius: float, max_nn: int)->t.Tuple[int,IntVector,DoubleVector]:
        """ Hybrid search for neighbors within a radius. If the number of neighbors found is less than max_nn, then kNN search is used. Otherwise, radius search is used. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_knn_vector_3d(self, query: npt.NDArray[np.float64[3,1]], knn: int)->t.Tuple[int,IntVector,DoubleVector]:
        """ kNN search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_knn_vector_xd(self, query: npt.NDArray[np.float64], knn: int)->t.Tuple[int,IntVector,DoubleVector]:
        """ kNN search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_radius_vector_3d(self, query: npt.NDArray[np.float64[3,1]], radius: float)->t.Tuple[int,IntVector,DoubleVector]:
        """ Radius search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_radius_vector_xd(self, query: npt.NDArray[np.float64], radius: float)->t.Tuple[int,IntVector,DoubleVector]:
        """ Radius search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_vector_3d(self, query: npt.NDArray[np.float64[3,1]], search_param: KDTreeSearchParam)->t.Tuple[int,IntVector,DoubleVector]:
        """ Search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def search_vector_xd(self, query: npt.NDArray[np.float64], search_param: KDTreeSearchParam)->t.Tuple[int,IntVector,DoubleVector]:
        """ Search for neighbors. Returns the number of neighbors found, the indices of the neighbors, and the squared distances to the neighbors."""        
        pass
    def set_feature(self, feature: Feature)->bool:
        """Sets the data for the KDTree from the feature data."""        
        pass
    def set_geometry(self, geometry: Geometry)->bool:
        """Sets the data for the KDTree from geometry."""        
        pass
    def set_matrix_data(self, data: npt.NDArray[np.float64])->bool:
        """Sets the data for the KDTree from a matrix."""        
        pass
    pass

class KDTreeSearchParamHybrid:
    pass

class KDTreeSearchParamKNN:
    pass

class KDTreeSearchParamRadius:
    pass

class LineSet:
    pass

class MeshBase:
    pass

class Octree:
    pass

class OctreeColorLeafNode:
    pass

class OctreelnternalNode:
    pass

class OctreelnternalPointNode:
    pass

class OctreeLeafNode:
    pass

class OctreeNodeInfo:
    pass

class OctreePointColorLeafNode:
    pass

class OrientedBoundingBox:
    pass
class PinholeCameraIntrinsic:
    """ open3d.camera.PinholeCameraIntrinsic """
    pass
class PointCloud(Geometry3D):
    def __new__(cls):
        return o3d.geometry.PointCloud()
    def cluster_dbscan(self, eps: float, min_points: int, print_progress: bool = False)->IntVector:
        """Cluster PointCloud using the DBSCAN algorithm Ester et al., ‘A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise’, 1996. Returns a list of point labels, -1 indicates noise according to the algorithm."""        
        pass
    def compute_convex_hull(self)->t.Tuple[TriangleMesh,t.List[int]]:
        """Computes the convex hull of the point cloud.
        convex 凸包/凸殼"""        
        pass
    def compute_mahalanobis_distance(self)->DoubleVector:
        """Function to compute the Mahalanobis distance for points in a point cloud. See: https://en.wikipedia.org/wiki/Mahalanobis_distance.
        馬氏距離"""        
        pass
    def compute_mean_and_covariance(self)->t.Tuple[npt.NDArray[np.float64[3,1]],npt.NDArray[np.float64[3,3]]]:
        """Function to compute the mean and covariance matrix of a point cloud."""        
        pass
    def compute_nearest_neighbor_distance(self)->DoubleVector:
        """Function to compute the distance from a point to its nearest neighbor in the point cloud"""        
        pass
    def compute_point_cloud_distance(self, target: PointCloud)->DoubleVector:
        """For each point in the source point cloud, compute the distance to the target point cloud."""        
        pass
    def compute_point_cloud_distance(self, target: PointCloud)->DoubleVector:
        """For each point in the source point cloud, compute the distance to the target point cloud."""        
        pass
    def crop(self, bounding_box: t.Union[AxisAlignedBoundingBox,OrientedBoundingBox])->PointCloud:
        """Function to crop input pointcloud into output pointcloud"""
        pass
    def dimension(self)->int:
        """Returns whether the geometry is 2D or 3D."""
        pass
    def estimate_covariances(self, search_param: t.Optional[KDTreeSearchParamKNN] = None):
        """Function to compute the covariance matrix for each point in the point cloud"""
        pass
    def estimate_normals(self, search_param: t.Optional[KDTreeSearchParamKNN] = None, fast_normal_computation: bool = True):
        """Function to compute the normals of a point cloud. Normals are oriented with respect to the input point cloud if normals exist"""
        pass
    def has_colors(self)->bool:
        """Returns True if the point cloud contains point colors."""
        pass
    def has_covariances(self)->bool:
        """Returns True if the point cloud contains covariances."""
        pass
    def has_normals(self)->bool:
        """Returns True if the point cloud contains point normals."""
        pass
    def has_points(self)->bool:
        """Returns True if the point cloud contains points."""
        pass
    def hidden_point_removal(self, camera_location: npt.NDArray[np.float64[3,1]], radius: float)->t.Tuple[TriangleMesh,t.List[int]]:
        """Removes hidden points from a point cloud and returns a mesh of the remaining points. Based on Katz et al. ‘Direct Visibility of Point Sets’, 2007. Additional information about the choice of radius for noisy point clouds can be found in Mehra et. al. ‘Visibility of Noisy Point Cloud Data’, 2010."""
        pass
    def normalize_normals(self)->PointCloud:
        """Normalize point normals to length 1."""
        pass
    def orient_normals_consistent_tangent_plane(self, k: int):
        """Function to orient the normals with respect to consistent tangent planes"""
        pass  
    def orient_normals_to_align_with_direction(self, orientation_reference: npt.NDArray[np.float64[3,1]] = np.array([0.0, 0.0, 1.0])):
        """Function to orient the normals of a point cloud"""
        pass
    def orient_normals_towards_camera_location(self, camera_location: npt.NDArray[np.float64[3,1]] = np.array([0.0, 0.0, 0.0])):
        """Function to orient the normals of a point cloud"""
        pass
    def paint_uniform_color(self, color: npt.NDArray[np.float64[3,1]])->PointCloud:
        """Assigns each point in the PointCloud the same color."""
        pass
    def random_down_sample(self, sampling_ratio: float)->PointCloud:
        """Function to downsample input pointcloud into output pointcloud randomly. The sample is generated by randomly sampling the indexes from the point cloud."""
        pass
    def remove_non_finite_points(self, remove_nan: bool = True, remove_infinite: bool = True)->PointCloud:
        """Function to remove non-finite points from the PointCloud"""
        pass
    def remove_radius_outlier(self, nb_points: int, radius: float, print_progress: bool = False)->t.Tuple[PointCloud,t.List[int]]:
        """Function to remove points that have less than nb_points in a given sphere of a given radius"""
        pass
    def remove_statistical_outlier(self, nb_neighbors: int, std_ratio: float, print_progress: bool = False)->t.Tuple[PointCloud,t.List[int]]:
        """Function to remove points that are further away from their neighbors in average"""
        pass
    def segment_plane(self, distance_threshold: float, ransac_n: int, num_iterations: int, seed: t.Optional[int] = None)->t.Tuple[npt.NDArray[np.float64[4,1]],t.List[int]]:
        """Segments a plane in the point cloud using the RANSAC algorithm."""
        pass
    def select_by_index(self, indices: IntVector, invert: bool = False)->PointCloud:
        """Function to select points from input pointcloud into output pointcloud."""
        pass
    def uniform_down_sample(self, every_k_points: int)->PointCloud:
        """Function to downsample input pointcloud into output pointcloud uniformly. The sample is performed in the order of the points with the 0-th point always chosen, not at random."""
        pass
    def voxel_down_sample(self, voxel_size: float)->PointCloud:
        """Function to downsample input pointcloud into output pointcloud with a voxel. Normals and colors are averaged if they exist."""
        pass
    def voxel_down_sample_and_trace(self, voxel_size: float, min_bound: npt.NDArray[np.float64[3,1]], max_bound: npt.NDArray[np.float64[3,1]], approximate_class: bool = False)->t.Tuple[PointCloud,npt.NDArray[np.int32],t.List[IntVector]]:
        """Function to downsample using PointCloud.VoxelDownSample. Also records point cloud index before downsampling"""
        pass
    @staticmethod
    def create_from_depth_image(depth: Image, intrinsic: PinholeCameraIntrinsic, extrinsic: t.Optional[npt.NDArray[np.float64[4,4]]] = None, depth_scale: float = 1000.0, depth_trunc: float = 1000.0, stride: int = 1, project_valid_depth_only: bool = True)->PointCloud:
        """Factory function to create a pointcloud from a depth image and a camera. Given depth value d at (u, v) image coordinate, the corresponding 3d point is:
        
        z = d / depth_scale
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy
        
        - Parameters:
            - depth (open3d.geometry.Image) – The input depth image can be either a float image, or a uint16_t image.
            - intrinsic (open3d.camera.PinholeCameraIntrinsic) – Intrinsic parameters of the camera.
            - extrinsic (numpy.ndarray[numpy.float64[4, 4]], optional) – array([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
            - depth_scale (float, optional, default=1000.0) – The depth is scaled by 1 / depth_scale.
            - depth_trunc (float, optional, default=1000.0) – Truncated at depth_trunc distance.
            - stride (int, optional, default=1) – Sampling factor to support coarse point cloud extraction.
            - project_valid_depth_only (bool, optional, default=True) –        
        """
        pass
    @staticmethod
    def create_from_rgbd_image(image: RGBDImage, intrinsic: PinholeCameraIntrinsic, extrinsic: t.Optional[npt.NDArray[np.float64[4,4]]] = None, project_valid_depth_only: bool = True)->PointCloud:
        """Factory function to create a pointcloud from an RGB-D image and a camera. Given depth value d at (u, v) image coordinate, the corresponding 3d point is:
        
        z = d / depth_scale
        x = (u - cx) * z / fx
        y = (v - cy) * z / fy
        
        - Parameters:
            - image (open3d.geometry.RGBDImage) – The input image.
            - intrinsic (open3d.camera.PinholeCameraIntrinsic) – Intrinsic parameters of the camera.
            - extrinsic (numpy.ndarray[numpy.float64[4, 4]], optional) – array([[1., 0., 0., 0.], [0., 1., 0., 0.], [0., 0., 1., 0.], [0., 0., 0., 1.]])
            - project_valid_depth_only (bool, optional, default=True) –        
        """
        pass  
    @staticmethod
    def estimate_point_covariances(input: PointCloud, search_param: t.Optional[KDTreeSearchParamKNN] = None)->npt.NDArray[np.float64[3,3]]:
        """Static function to compute the covariance matrix for each point in the given point cloud, doesn’t change the input
        
        - Parameters:
            - input (open3d.geometry.PointCloud) – The input point cloud.
            - search_param (open3d.geometry.KDTreeSearchParam, optional, default=KDTreeSearchParamKNN with knn = 30) – The KDTree search parameters for neighborhood search.
        """        
        pass
    @property
    def colors(self)-> Vector3dVector:
        """
        RGB colors of points.
        - Type: float64 array of shape (num_points, 3), range [0, 1] , use numpy.asarray() to access data"""
        pass
    @colors.setter
    def colors(self, value: Vector3dVector):
        pass
    @property
    def covariances(self)->Matrix3dVector:
        """
        Points covariances.
        - Type: float64 array of shape (num_points, 3, 3), use numpy.asarray() to access data
        """
        pass
    @covariances.setter
    def covariances(self, value: Matrix3dVector):
        pass
    @property
    def normals(self)->Vector3dVector:
        """
        Points normals.
        - Type: float64 array of shape (num_points, 3), use numpy.asarray() to access data
        """
        pass
    @normals.setter
    def normals(self, value: Vector3dVector):
        pass
    @property
    def points(self)->Vector3dVector:
        """
        Points coordinates.
        - Type: float64 array of shape (num_points, 3), use numpy.asarray() to access data
        """
        pass
    @points.setter
    def points(self, value: Vector3dVector):
        pass

    

class RGBDImage:
    pass

class SimplificationContraction:
    pass

class TetraMesh:
    pass

class TriangleMesh(Geometry3D):       
    def __new__(cls):
        return o3d.geometry.TriangleMesh()   
    def __init__(self, mesh: t.Optional[TriangleMesh]):
        pass
    def __init__(self, vertices: Vector3dVector, triangles: Vector3iVector):
        pass
    @staticmethod
    def lazyToPointCloud(mesh: TriangleMesh)->PointCloud:
        ''' 轉換成點雲
        - 筆記: o3d.geometry.TriangleMesh 本來就沒有這個函式，所以不能寫成 self.lazyToPointCloud(self): 
        '''
        pc = PointCloud()
        pc.points = mesh.vertices
        if mesh.has_vertex_colors():
            pc.colors = mesh.vertex_colors
        if mesh.has_vertex_normals():
            pc.normals = mesh.vertex_normals
        return pc
    def cluster_connected_triangles(self)->t.Tuple[IntVector,t.List[int],DoubleVector]:
        """Function that clusters connected triangles, i.e., triangles that are connected via edges are assigned the same cluster index. This function returns an array that contains the cluster index per triangle, a second array contains the number of triangles per cluster, and a third vector contains the surface area per cluster."""        
        pass
    def compute_adjacency_list(self)->TriangleMesh:
        """Function to compute adjacency list, call before adjacency list is needed"""
        pass
    def computer_convex_hull(self)->t.Tuple[TriangleMesh,t.List[int]]:
        """Computes the convex hull of the triangle mesh."""
        pass
    def compute_triangle_normals(self)->TriangleMesh:
        """Function to compute triangle normals, call before triangle normals are needed"""
        pass
    def compute_vertex_normals(self)->TriangleMesh:
        """Function to compute vertex normals, call before vertex normals are needed"""
        pass
    def crop(self, bounding_box: t.Union[AxisAlignedBoundingBox,OrientedBoundingBox])->TriangleMesh:
        """Function to crop input TriangleMesh into output TriangleMesh"""
        pass
    def deform_as_rigid_as_possible(self, constraint_vertex_indices: IntVector, constraint_vertex_positions: Vector3dVector, max_iter: int, energy: t.Optional[DeformAsRigidAsPossibleEnergy], smoothed_alpha: float = 0.01)->TriangleMesh:
        """This function deforms the mesh using the method by Sorkine and Alexa, ‘As-Rigid-As-Possible Surface Modeling’, 2007"""
        pass
    def dimension(self)->int:
        """Returns whether the geometry is 2D or 3D."""
        pass
    def euler_poincare_characteristic(self)->int:
        """Function that computes the Euler-Poincaré characteristic, i.e., V + F - E, where V is the number of vertices, F is the number of triangles, and E is the number of edges."""
        pass
    def filter_sharpen(self, number_of_iterations: int = 1, strength: float = 1, filter_scope: t.Optional[FilterScope] = None)->TriangleMesh:
        """Function to sharpen triangle mesh. The output value (vo) is the input value (vi) plus strength times the input value minus he sum of he adjacent values. vo=vixstrength(vi∗|N|−∑n∈Nvn)"""
        pass
    def filter_smooth_laplacian(self, number_of_iterations: int = 1, lambda_: float = 0.5, filter_scope: t.Optional[FilterScope] = None)->TriangleMesh:
        """Function to smooth triangle mesh using Laplacian. vo=vi⋅λ(sumn∈Nwnvn−vi), with vi being the input value, vo the output value, N is the set of adjacent neighbours, wn is the weighting of the neighbour based on the inverse distance (closer neighbours have higher weight), and lambda is the smoothing parameter."""
        pass
    def filter_smooth_simple(self, number_of_iterations: int = 1, filter_scope: t.Optional[FilterScope] = None)->TriangleMesh:
        """Function to smooth triangle mesh with simple neighbour average. vo=vi+∑n∈Nvn)|N|+1, with vi being the input value, vo the output value, and N is the set of adjacent neighbours."""
        pass
    def filter_smooth_taubin(self, number_of_iterations: int = 1, lambda_: float = 0.5, mu: float = -0.53, filter_scope: t.Optional[FilterScope] = None)->TriangleMesh: 
        """Function to smooth triangle mesh using method of Taubin, “Curve and Surface Smoothing Without Shrinkage”, 1995. Applies in each iteration two times filter_smooth_laplacian, first with filter parameter lambda and second with filter parameter mu as smoothing parameter. This method avoids shrinkage of the triangle mesh."""
        pass
    def get_non_manifold_edges(self, allow_boundary_edges: bool = True)->Vector2iVector:
        """Get list of non-manifold edges."""
        pass
    def get_non_manifold_vertices(self)->IntVector:
        """Returns a list of indices to non-manifold vertices."""
        pass
    def get_self_intersecting_triangles(self)->Vector2iVector:
        """Returns a list of indices to triangles that intersect the mesh."""
        pass
    def get_surface_area(self)->float:
        """Function that computes the surface area of the mesh, i.e. the sum of the individual triangle surfaces."""
        pass
    def get_volume(self)->float:
        """Function that computes the volume of the mesh, under the condition that it is watertight and orientable."""
        pass
    def has_adjacency_list(self)->bool:
        """Returns True if the mesh contains adjacency normals."""
        pass
    def has_textures(self)->bool:
        """Returns True if the mesh contains a texture image."""
        pass
    def has_triangle_material_ids(self)->bool:
        """Returns True if the mesh contains material ids."""
        pass
    def has_triangle_normals(self)->bool:
        """Returns True if the mesh contains triangle normals."""
        pass
    def has_triangle_uvs(self)->bool:
        """Returns True if the mesh contains uv coordinates."""
        pass
    def has_triangles(self)->bool:
        """Returns True if the mesh contains triangles."""
        pass
    def has_vertex_colors(self)->bool:
        """Returns True if the mesh contains vertex colors."""
        pass
    def has_vertex_normals(self)->bool:
        """Returns True if the mesh contains vertex normals."""
        pass
    def has_vertices(self)->bool:
        """Returns True if the mesh contains vertices."""
        pass
    def is_edge_manifold(self, allow_boundary_edges: bool = True)->bool:
        """Tests if the triangle mesh is edge manifold.
        - Parameters:
            - allow_boundary_edges: If true, than non-manifold edges are defined as edges with more than two adjacent triangles, otherwise each edge that is not adjacent to two triangles is defined as non-manifold.
        """
        pass
    def is_empty(self)->bool:
        """Returns True iff the geometry is empty."""
        pass
    def is_intersecting(self, arg0: TriangleMesh)->bool:
        """Tests if the triangle mesh is intersecting the other triangle mesh."""
        pass
    def is_orientable(self)->bool:
        """Tests if the triangle mesh is orientable."""
        pass
    def is_self_intersecting(self)->bool:
        """Tests if the triangle mesh is self-intersecting."""
        pass
    def is_vertex_manifold(self)->bool:
        """Tests if all vertices of the triangle mesh are manifold."""
        pass
    def is_watertight(self)->bool:
        """Tests if the triangle mesh is watertight."""
        pass
    def merge_close_vertices(self, eps: float)->TriangleMesh:
        """Function that will merge close by vertices to a single one. The vertex position, normal and color will be the average of the vertices. The parameter eps defines the maximum distance of close vertices. This function might help to close triangle soups."""
        pass
    def normalize_normals(self)->TriangleMesh:
        """Normalize both triangle normals and vertex normals to length 1."""
        pass
    def orient_triangles(self)->bool:
        """If the mesh is orientable this function orients all triangles such that all normals point towards the same direction."""
        pass
    def paint_uniform_color(self, arg0: npt.NDArray[np.float64[3,1]])->MeshBase:
        """Assigns each vertex in the TriangleMesh the same color."""
        pass
    def remove_degenerate_triangles(self)->TriangleMesh:
        """Function that removes degenerate triangles, i.e., triangles that references a single vertex multiple times in a single triangle. They are usually the product of removing duplicated vertices."""
        pass
    def remove_duplicated_triangles(self)->TriangleMesh:
        """Function that removes duplicated triangles, i.e., removes triangles that reference the same three vertices, independent of their order."""
        pass
    def remove_duplicated_vertices(self)->TriangleMesh:
        """Function that removes duplicated verties, i.e., vertices that have identical coordinates."""
        pass
    def remove_non_manifold_edges(self)->TriangleMesh:
        """Function that removes all non-manifold edges, by successively deleting triangles with the smallest surface area adjacent to the non-manifold edge until the number of adjacent triangles to the edge is <= 2."""
        pass
    def remove_triangles_by_index(self, triangle_indices: IntVector):
        """This function removes the triangles with index in triangle_indices. Call remove_unreferenced_vertices to clean up vertices afterwards."""
        pass
    def remove_triangles_by_mask(self, triangle_mask: IntVector):
        """This function removes the triangles where triangle_mask is set to true. Call remove_unreferenced_vertices to clean up vertices afterwards."""
        pass
    def remove_unreferenced_vertices(self)->TriangleMesh:
        """This function removes vertices from the triangle mesh that are not referenced in any triangle of the mesh."""
        pass
    def remove_vertices_by_index(self, vertex_indices: t.List[int]):
        """This function removes the vertices with index in vertex_indices. Note that also all triangles associated with the vertices are removed."""
        pass
    def remove_vertices_by_mask(self, vertex_mask: t.List[bool]):
        """This function removes the vertices that are masked in vertex_mask. Note that also all triangles associated with the vertices are removed."""
        pass
    def sample_points_poisson_disk(self, number_of_points: int, init_factor: float = 5, pcl: t.Optional[PointCloud] = None, use_triangle_normal: bool = False, seed: int = -1)->PointCloud:
        """Function to sample points from the mesh, where each point has approximately the same distance to the neighbouring points (blue noise). Method is based on Yuksel, “Sample Elimination for Generating Poisson Disk Sample Sets”, EUROGRAPHICS, 2015."""
        pass
    def sample_points_uniformly(self, number_of_points: int = 100, use_triangle_normal: bool = False, seed: int = -1)->PointCloud:
        """Function to uniformly sample points from the mesh."""
        pass    
    def select_by_index(self, indices: t.List[int], cleanup: bool = True)->TriangleMesh:
        """Function to select mesh from input triangle mesh into output triangle mesh. input: The input triangle mesh. indices: Indices of vertices to be selected."""        
        pass
    def simplify_quadric_decimation(self, target_number_of_triangles: int, maximum_error: float = np.inf, boundary_weight: float = 1.0)->TriangleMesh:
        """Function to simplify mesh using Quadric Error Metric Decimation by Garland and Heckbert"""
        pass
    def simplify_vertex_clustering(self, voxel_size: float, contraction: t.Optional[SimplificationContraction] = None)->TriangleMesh:
        """Function to simplify mesh using vertex clustering."""
        pass
    def subdivide_loop(self, number_of_iterations: int = 1)->TriangleMesh:
        """Function subdivide mesh using Loop’s algorithm. Loop, “Smooth subdivision surfaces based on triangles”, 1987."""
        pass
    def subdivide_midpoint(self, number_of_iterations: int = 1)->TriangleMesh:
        """Function subdivide mesh using midpoint algorithm."""
        pass
    @staticmethod
    def create_arrow(cylinder_radius: float = 1.0, cone_radius: float = 1.5, cylinder_height: float = 5.0, cone_height: float = 4.0, resolution: int = 20, cylinder_split: int = 4, cone_split: int = 1)->TriangleMesh:
        """Factory function to create an arrow mesh
        
        - Parameters:
            - cylinder_radius (float, optional, default=1.0) – The radius of the cylinder.
            - cone_radius (float, optional, default=1.5) – The radius of the cone.
            - cylinder_height (float, optional, default=5.0) – The height of the cylinder. The cylinder is from (0, 0, 0) to (0, 0, cylinder_height)
            - cone_height (float, optional, default=4.0) – The height of the cone. The axis of the cone will be from (0, 0, cylinder_height) to (0, 0, cylinder_height + cone_height)
            - resolution (int, optional, default=20) – The cone will be split into resolution segments.
            - cylinder_split (int, optional, default=4) – The cylinder_height will be split into cylinder_split segments.
            - cone_split (int, optional, default=1) – The cone_height will be split into cone_split segments.        
        """
        pass
    @staticmethod
    def create_box(width: float = 1.0, height: float = 1.0, depth: float = 1.0, create_uv_map: bool = False, map_texture_to_each_face: bool = False)->TriangleMesh:
        """Factory function to create a box. The left bottom corner on the front will be placed at (0, 0, 0), and default UV map, maps the entire texture to each face.
        
        - Parameters:
            - width (float, optional, default=1.0) – x-directional length.
            - height (float, optional, default=1.0) – y-directional length.
            - depth (float, optional, default=1.0) – z-directional length.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.
            - map_texture_to_each_face (bool, optional, default=False) – Map entire texture to each face.        
        """
        pass
    @staticmethod
    def create_cone(radius: float = 1.0, height: float = 2.0, resolution: int = 20, split: int = 1, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a cone mesh.
        
        - Parameters:
            - radius (float, optional, default=1.0) – The radius of the cone.
            - height (float, optional, default=2.0) – The height of the cone. The axis of the cone will be from (0, 0, 0) to (0, 0, height).
            - resolution (int, optional, default=20) – The circle will be split into resolution segments
            - split (int, optional, default=1) – The height will be split into split segments.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_coordinate_frame(size: float = 1.0, origin: npt.NDArray[np.float64[3,1]] = np.array([0.0, 0.0, 0.0]))->TriangleMesh:
        """Factory function to create a coordinate frame mesh. The coordinate frame will be centered at origin. The x, y, z axis will be rendered as red, green, and blue arrows respectively.
        
        - Parameters:
            - size (float, optional, default=1.0) – The size of the coordinate frame.
            - origin (numpy.ndarray[numpy.float64[3, 1]], optional, default=array([0., 0., 0.])) – The origin of the cooridnate frame.        
        """
        pass
    @staticmethod
    def create_cylinder(radius: float = 1.0, height: float = 2.0, resolution: int = 20, split: int = 4, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a cylinder mesh.
        
        - Parameters:
            - radius (float, optional, default=1.0) – The radius of the cylinder.
            - height (float, optional, default=2.0) – The height of the cylinder. The axis of the cylinder will be from (0, 0, -height/2) to (0, 0, height/2).
            - resolution (int, optional, default=20) – The circle will be split into resolution segments
            - split (int, optional, default=4) – The height will be split into split segments.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_from_point_cloud_alpha_shape(pcd: PointCloud, alpha: float)->TriangleMesh:
        """Alpha shapes are a generalization of the convex hull. With decreasing alpha value the shape schrinks and creates cavities. See Edelsbrunner and Muecke, “Three-Dimensional Alpha Shapes”, 1994.
        
        - Parameters:
            - pcd (open3d.geometry.PointCloud) – PointCloud from which the TriangleMesh surface is reconstructed.
            - alpha (float) – Parameter to control the shape. A very big value will give a shape close to the convex hull.        
        """
        pass
    @staticmethod
    def create_from_point_cloud_ball_pivoting(pcd: PointCloud, radii: DoubleVector)->TriangleMesh:
        """Function that computes a triangle mesh from a oriented PointCloud. This implements the Ball Pivoting algorithm proposed in F. Bernardini et al., “The ball-pivoting algorithm for surface reconstruction”, 1999. The implementation is also based on the algorithms outlined in Digne, “An Analysis and Implementation of a Parallel Ball Pivoting Algorithm”, 2014. The surface reconstruction is done by rolling a ball with a given radius over the point cloud, whenever the ball touches three points a triangle is created.
        
        - Parameters:
            - pcd (open3d.geometry.PointCloud) – PointCloud from which the TriangleMesh surface is reconstructed. Has to contain normals.
            - radii (open3d.utility.DoubleVector) – The radii of the ball that are used for the surface reconstruction.        
        """
        pass
    @staticmethod
    def create_from_point_cloud_poisson(pcd: PointCloud, depth: int = 8, width: int = 0, scale: float = 1.1, linear_fit: bool = False, n_threads: int = -1)->TriangleMesh:
        """Function that computes a triangle mesh from a oriented PointCloud pcd. This implements the Screened Poisson Reconstruction proposed in Kazhdan and Hoppe, “Screened Poisson Surface Reconstruction”, 2013. This function uses the original implementation by Kazhdan. See https://github.com/mkazhdan/PoissonRecon
        
        - Parameters:
            - pcd (open3d.geometry.PointCloud) – PointCloud from which the TriangleMesh surface is reconstructed. Has to contain normals.
            - depth (int, optional, default=8) – Maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound.
            - width (int, optional, default=0) – Specifies the target width of the finest level octree cells. This parameter is ignored if depth is specified
            - scale (float, optional, default=1.1) – Specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples’ bounding cube.
            - linear_fit (bool, optional, default=False) – If true, the reconstructor will use linear interpolation to estimate the positions of iso-vertices.
            - n_threads (int, optional, default=-1) – Number of threads used for reconstruction. Set to -1 to automatically determine it.            
        """
        
    @staticmethod
    def create_icosahedron(radius: float = 1.0, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a icosahedron. The centroid of the mesh will be placed at (0, 0, 0) and the vertices have a distance of radius to the center.
        
        - Parameters:
            - radius (float, optional, default=1.0) – Distance from centroid to mesh vetices.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_moebius(length_split: int = 70, width_split: int = 15, twists: int = 1, raidus: float = 1, flatness: float = 1, width: float = 1, scale: float = 1)->TriangleMesh:
        """Factory function to create a Moebius strip.
        
        - Parameters:
            - length_split (int, optional, default=70) – The number of segments along the Moebius strip.
            - width_split (int, optional, default=15) – The number of segments along the width of the Moebius strip.
            - twists (int, optional, default=1) – Number of twists of the Moebius strip.
            - raidus (float, optional, default=1) –
            - flatness (float, optional, default=1) – Controls the flatness/height of the Moebius strip.
            - width (float, optional, default=1) – Width of the Moebius strip.
            - scale (float, optional, default=1) – Scale the complete Moebius strip.        
        """
        pass
    @staticmethod
    def create_octahedron(radius: float = 1.0, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a octahedron. The centroid of the mesh will be placed at (0, 0, 0) and the vertices have a distance of radius to the center.
        
        - Parameters:
            - radius (float, optional, default=1.0) – Distance from centroid to mesh vetices.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_sphere(radius: float = 1.0, resolution: int = 20, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a sphere mesh centered at (0, 0, 0).
        
        - Parameters:
            - radius (float, optional, default=1.0) – The radius of the sphere.
            - resolution (int, optional, default=20) – The resolution of the sphere. The longitues will be split into resolution segments (i.e. there are resolution + 1 latitude lines including the north and south pole). The latitudes will be split into `2 * resolution segments (i.e. there are 2 * resolution longitude lines.)
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_tetrahedron(radius: float = 1.0, create_uv_map: bool = False)->TriangleMesh:
        """Factory function to create a tetrahedron. The centroid of the mesh will be placed at (0, 0, 0) and the vertices have a distance of radius to the center.
        
        - Parameters:
            - radius (float, optional, default=1.0) – Distance from centroid to mesh vetices.
            - create_uv_map (bool, optional, default=False) – Add default uv map to the mesh.        
        """
        pass
    @staticmethod
    def create_torus(torus_radius: float = 1.0, tube_radius: float = 0.5, radial_resolution: int = 30, tubular_resolution: int = 20)->TriangleMesh:
        """Factory function to create a torus mesh.
        
        - Parameters:
            - torus_radius (float, optional, default=1.0) – The radius from the center of the torus to the center of the tube.
            - tube_radius (float, optional, default=0.5) – The radius of the torus tube.
            - radial_resolution (int, optional, default=30) – The number of segments along the radial direction.
            - tubular_resolution (int, optional, default=20) – The number of segments along the tubular direction.        
        """
        pass
    
    @property
    def adjacency_list(self)->t.List[t.List[int]]:
        """Returns the adjacency list.
        - 例如：[0] 是 [1, 2, 95107, 97737] 表示頂點0的相鄰頂點有1, 2, 95107, 97737        
        """
        pass
    @property
    def textures(self)->t.List[Image]:
        """Returns the textures."""
        pass
    @property
    def triangle_material_ids(self)->IntVector:
        """Returns the triangle material ids."""
        pass
    @property
    def triangle_normals(self)->Vector3dVector:
        """Returns the triangle normals."""
        pass
    @property
    def triangle_uvs(self)->Vector2dVector:
        """Returns the triangle uvs."""
        pass
    @property
    def triangles(self)->Vector3iVector:
        """Returns the triangles."""
        pass
    @property
    def vertex_colors(self)->Vector3dVector:
        """Returns the vertex colors."""
        pass
    @property
    def vertex_normals(self)->Vector3dVector:
        """Returns the vertex normals."""
        pass
    @property
    def vertices(self)->Vector3dVector:
        """Returns the vertices."""
        pass
    
    
class Voxel:
    pass
class VoxelGrid:
    pass

#%%
# rendering
class Camera:
    """rendering.Camera"""    
    class FovType:
        Vertical: Camera.FovType = rendering.Camera.FovType.Vertical        
        Horizontal: Camera.FovType = rendering.Camera.FovType.Horizontal
        @property
        def value(self)->Camera.FovType:
            pass
        @value.setter
        def value(self, value: Camera.FovType):
            pass
    class Projection:
        Perspective: Camera.Projection = rendering.Camera.Projection.Perspective
        Ortho: Camera.Projection = rendering.Camera.Projection.Ortho
        @property
        def value(self)->Camera.Projection:
            pass
        @value.setter
        def value(self, value: Camera.Projection):
            pass
    def copy_from(self, camera: Camera):
        """Copies the settings from the camera passed as the argument into this camera"""
        pass
    def get_far(self)->float:
        """Returns the distance from the camera to the far plane"""
        pass
    def get_field_of_view(self)->float:
        """Returns the field of view of camera, in degrees. Only valid if it was passed to set_projection()."""
        pass
    def get_field_of_view_type(self)->Camera.FovType:
        """Returns the field of view type. Only valid if it was passed to set_projection()."""
        pass
    def get_model_matrix(self)->npt.NDArray[np.float32[4,4]]:
        """Returns the model matrix of the camera"""
        pass
    def get_near(self)->float:
        """Returns the distance from the camera to the near plane"""
        pass
    def get_projection_matrix(self)->npt.NDArray[np.float32[4,4]]:
        """Returns the projection matrix of the camera"""
        pass
    def get_view_matrix(self)->npt.NDArray[np.float32[4,4]]:
        """Returns the view matrix of the camera"""
        pass
    def look_at(self, center: npt.NDArray[np.float32[3,1]], eye: npt.NDArray[np.float32[3,1]], up: npt.NDArray[np.float32[3,1]]):
        """Sets the position and orientation of the camera: look_at(center, eye, up)"""
        pass
    def set_projection(self, *args, **kwargs):
        pass
    def set_projection1(self, field_of_view: float, aspect_ratio: float, far_plane: float, field_of_view_type: Camera.FovType):
        """Sets a perspective projection. set_projection(field_of_view, aspect_ratio, far_plane, field_of_view_type)"""
        self.set_projection(field_of_view, aspect_ratio, far_plane, field_of_view_type)
    def set_projection2(self, projection_type: Camera.Projection, left: float, right: float, bottom: float, top: float, near: float, far: float):
        """Sets the camera projection via a viewing frustum. set_projection(projection_type, left, right, bottom, top, near, far)"""
        self.set_projection(projection_type, left, right, bottom, top, near, far)
    def set_projection3(self, intrinsics: npt.NDArray[np.float64[3,3]], near_plane: float, far_plane: float, image_width: float, image_height: float):
        """Sets the camera projection via intrinsics matrix. set_projection(intrinsics, near_place, far_plane, image_width, image_height)"""
        self.set_projection(intrinsics, near_plane, far_plane, image_width, image_height)
    def unproject(self, x: float, y: float, z: float, view_width: float, view_height: float)->npt.NDArray[np.float32[3,1]]:
        """Takes the (x, y, z) location in the view, where x, y are the number of pixels from the upper left of the view, and z is the depth value. Returns the world coordinate (x’, y’, z’)."""
        pass            
    pass
class ColorGrding:
    pass
class Gradient:
    pass
class MaterialRecord:
    class TpShader(NoValue):
        UNLIT = "defaultUnlit"
        LIT = "defaultLit"
        NORMALS = "normals"
        DEPTH = "depth"
    '''
        property base_reflectance
        property base_roughness
        property clearcoat_img
        property clearcoat_roughness_img
        property generic_imgs
        property generic_params
        property gradient
        property ground_plane_axis
        property has_alpha
        property line_width
            Requires  ‘shader’ to be ‘unlitLine’
        property metallic_img
        property normal_img
        property point_size
        property reflectance_img
        property roughness_img
        property sRGB_color
        property scalar_max
        property scalar_min
        property shader
        property thickness
        property transmission
    '''
    def __new__(cls):
        return rendering.MaterialRecord()
    def lazyMaterialRecord()->MaterialRecord:
        r1 = MaterialRecord()
        r1.shader = "defaultLit"
        return r1
    
    @property
    def absorption_color(self)->npt.NDArray[np.float32[4,1]]:
        pass
    @absorption_color.setter
    def absorption_color(self, absorption_color: npt.NDArray[np.float32[4,1]]):
        pass
        
    @property
    def absorption_distance(self)->float:
        pass
    @absorption_distance.setter
    def absorption_distance(self, absorption_distance: float):
        pass
    
    @property
    def albedo_img(self)->Image:
        pass
    @albedo_img.setter
    def albedo_img(self, albedo_img: Image):
        pass
    @property
    def anisotropy_img(self)->Image:
        pass
    @anisotropy_img.setter
    def anisotropy_img(self, anisotropy_img: Image):
        pass
    @property
    def ao_img(self)->Image:
        pass
    @ao_img.setter
    def ao_img(self, ao_img: Image):
        pass
    @property
    def ao_rough_metal_img(self)->Image:
        pass
    @ao_rough_metal_img.setter
    def ao_rough_metal_img(self, ao_rough_metal_img: Image):
        pass
    @property
    def aspect_ratio(self)->float:
        pass
    @aspect_ratio.setter
    def aspect_ratio(self, aspect_ratio: float):
        pass
    
    @property
    def base_anisotropy(self)->float:
        pass
    @base_anisotropy.setter
    def base_anisotropy(self, base_anisotropy: float):
        pass
    @property
    def base_clearcoat(self)->float:
        pass
    @base_clearcoat.setter
    def base_clearcoat(self, base_clearcoat: float):
        pass
    @property
    def base_clearcoat_roughness(self)->float:
        pass
    @base_clearcoat_roughness.setter
    def base_clearcoat_roughness(self, base_clearcoat_roughness: float):
        pass
    @property
    def base_color(self)->npt.NDArray[np.float32[4,1]]:
        pass
    @base_color.setter
    def base_color(self, base_color: npt.NDArray[np.float32[4,1]]):
        pass
    @property
    def base_metallic(self)->float:
        pass
    @base_metallic.setter
    def base_metallic(self, base_metallic: float):
        pass
    @property
    def shader(self)->str:
        pass
    @shader.setter
    def shader(self, shader: t.Union[str, MaterialRecord.TpShader]):
        """可不設定，常用是 defaultLit 

        Args:
            shader (str): defaultLit defaultUnlit normals unlitLine depth
        """
        pass
    
    
    
    
    
class OffscreenRenderer:
    pass
class Open3DScene:
    def __new__(cls, *args, **kwargs):
        return rendering.Open3DScene(*args, **kwargs)
    def __init__(self, renderer: Open3DScene):
        """初始化一個 open3d 的 scene
        - 通常下一行，就是被用到 widgetScene.scene = self，其中 widgetScene 是 SceneWidget 

        Args:
            renderer (Open3DScene): 通常是用 window.renderer
        """
        pass
    
    def add_geometry(self, name: str, geometry: Geometry3D, material: MaterialRecord, add_downsampled_copy_for_fast_rendering: bool = True):
        """add geometry to scene
        - add_downsampled_copy_for_fast_rendering: 同時加入一個 downsampled copy 以加速渲染
        """       
        pass
    def add_model(self, name: str, model: TriangleMeshModel):
        pass
    def clear_geometry(self):
        pass
    def has_geometry(self, name: str)->bool:
        pass
    def modify_geometry_material(self, name: str, material: MaterialRecord):
        pass
    def remove_geometry(self, name: str):
        pass
    def set_background(self, color: npt.NDArray[np.float32[4,1]], image: Image = None):
        pass    
    def set_background_color(self, color: npt.NDArray[np.float32[4,1]]):
        """deprecated, use set_background instead"""        
        pass
    def show_axes(self, show: bool):
        pass
    def show_geometry(self, name: str, show: bool):
        pass
    def show_skybox(self, show: bool):
        pass
    def update_material(self, material: MaterialRecord):
        pass
    @property
    def background_color(self)->npt.NDArray[np.float32[4,1]]:
        pass
    @property
    def bounding_box(self)->AxisAlignedBoundingBox:
        pass
    @property
    def camera(self)->Camera:
        pass
    @property
    def downsample_threshold(self)->int:
        """若繪圖速度很重要，將這個值設小一點。"""
        pass
    @property
    def scene(self)->Scene:
        pass
    @property
    def view(self)->View:
        pass
        
class Renderer:
    pass

class Scene:        
    UPDATE_POINTS_FLAG:int = rendering.Scene.UPDATE_POINTS_FLAG
    UPDATE_NORMALS_FLAG:int = rendering.Scene.UPDATE_NORMALS_FLAG
    UPDATE_COLORS_FLAG:int = rendering.Scene.UPDATE_COLORS_FLAG
    UPDATE_UV0_FLAG:int = rendering.Scene.UPDATE_UV0_FLAG
        
    class GroundPlane:
        XY: Scene.GroundPlane = rendering.Scene.GroundPlane.XY
        XZ: Scene.GroundPlane = rendering.Scene.GroundPlane.XZ
        YZ: Scene.GroundPlane = rendering.Scene.GroundPlane.YZ
        @property
        def value(self)->Scene.GroundPlane:
            pass
        @value.setter
        def value(self, value: Scene.GroundPlane):
            pass
        
            
    def add_camera(self, name:str, camera: Camera):
        pass
    def add_directional_light(self, name: str, 
                              direction: npt.NDArray[np.float32[3,1]], 
                              color: npt.NDArray[np.float32[3,1]], 
                              intensity: float, cast_shadows: bool)->bool:
        pass
    def add_geometry(self, name: str, geometry: Geometry3D, material: MaterialRecord,
                     downsampled_name = "", downsample_threshold: int = 18446744073709551615)->bool:
        pass
    def add_point_light(self, name: str, color: npt.NDArray[np.float32[3,1]], 
                        position: npt.NDArray[np.float32[3,1]],
                        intensity: float, falloff: float, cast_shadows: bool)->bool:
        pass
    def add_spot_light(self, name: str, color: npt.NDArray[np.float32[3,1]], 
                       position: npt.NDArray[np.float32[3,1]], 
                       direction: npt.NDArray[np.float32[3,1]],
                       intensity: float, falloff: float, inner_cone_angle: float, outer_cone_angle: float, cast_shadows: bool)->bool:
        pass
    def enable_indirect_light(self, enable: bool):
        pass
    def enable_light_shadow(self, name: str, can_cast_shadows: bool):
        pass
    def enable_sun_light(self, enable: bool):
        pass
    def has_geometry(self, name: str)->bool:
        pass
    def remove_camera(self, name: str):
        pass
    def remove_light(self, name: str):
        pass
    def render_to_depth_image(self, callback: t.Callable[[Image], None]):
        """取得深度圖，0.0是靠近，1.0是遠離。通常會搭配 unproject 

        Args:
            callback (t.Callable[[Image], None]): _description_
        """
        pass
    def render_to_image(self, callback: t.Callable[[Image], None]):
        pass
    def set_active_camera(self, name: str):
        pass
    def set_indirect_light(self, name: str)->bool:
        """Loads the indirect light. The name parameter is the name of the file to load"""
        pass
    def set_indirect_light_intensity(self, intensity: float):
        """Sets the brightness of the indirect light"""
        pass
    def set_sun_light(self, direction: npt.NDArray[np.float32[3,1]],
                      color: npt.NDArray[np.float32[3,1]], intensity: float):
        pass
    def update_geometry(self, name: str, geometry: PointCloud, flags: t.Union[int, Scene.UPDATE_POINTS_FLAG,Scene.UPDATE_NORMALS_FLAG,Scene.UPDATE_COLORS_FLAG,Scene.UPDATE_UV0_FLAG]):
        """目前沒有成功使用，只能先用 clear 再 add 一次，就算我是用點雲也沒有成功過"""
        pass
    def update_light_color(self, name: str, color: npt.NDArray[np.float32[3,1]]):
        """Changes a point, spot, or directional light’s color"""
        pass
    def update_light_cone_angles(self, name: str, inner_cone_angle: float, outer_cone_angle: float):
        """Changes a spot light’s inner and outer cone angles"""
        pass
    def update_light_direction(self, name: str, direction: npt.NDArray[np.float32[3,1]]):
        """Changes a spot or directional light’s direction"""
        pass
    def update_light_falloff(self, name: str, falloff: float):
        """Changes a point or spot light’s falloff"""
        pass
    def update_light_intensity(self, name: str, intensity: float):
        """Changes a point, spot or directional light’s intensity"""
        pass
    def update_light_position(self, name: str, position: npt.NDArray[np.float32[3,1]]):
        """Changes a point or spot light’s position"""
        pass
    
class TriangleMeshModel:
    pass
class View:
    pass
    

#%%
# gui
class Size:
    def __new__(cls, *args, **kwargs):
        return gui.Size(*args, **kwargs)
    def __init__(self, width: t.Union[int,float] = 0, height: t.Union[int,float] = 0):
        pass
    @property
    def width(self)->float:
        pass
    @width.setter
    def width(self, width: float):
        pass
    @property
    def height(self)->float:
        pass
    @height.setter
    def height(self, height: float):
        pass
    pass
class Rect:
    def __new__(cls, *args, **kwargs):
        return gui.Rect(*args, **kwargs)
    def __init__(self, x: t.Union[int,float] = 0, y: t.Union[int,float] = 0, width: t.Union[int,float] = 0, height: t.Union[int,float] = 0):
        pass
    def get_bottom(self)->int:
        pass
    def get_left(self)->int:
        pass
    def get_right(self)->int:
        pass
    def get_top(self)->int:
        pass
    @property
    def x(self)->int:
        pass
    @x.setter
    def x(self, x: int):
        pass
    @property
    def y(self)->int:
        pass
    @y.setter
    def y(self, y: int):
        pass
    @property
    def width(self)->int:
        pass
    @width.setter
    def width(self, width: int):
        pass
    @property
    def height(self)->int:
        pass
    @height.setter
    def height(self, height: int):
        pass
    
class Color:
    def __new__(cls, r: float = 1.0, g: float = 1.0, b: float = 1.0, a: float = 1.0):
        return gui.Color(r, g, b, a)
    def set_color(self, r: float, g: float, b: float, a: float):
        pass
    @property
    def red(self)->float:
        pass
    @property
    def green(self)->float:
        pass
    @property
    def blue(self)->float:
        pass
    @property
    def alpha(self)->float:
        pass
    
class Widget:
    class Constraints:
        '''Constraints object for Widget.calc_preferred_size()'''
        @property
        def height(self)->int:
            pass
        def width(self)->int:
            pass

    class EventCallbackResult:
        IGNORED: Widget.EventCallbackResult = gui.Widget.EventCallbackResult.IGNORED
        """Event handler ignored the event, widget will handle event normally"""
        HANDLED: Widget.EventCallbackResult = gui.Widget.EventCallbackResult.HANDLED
        """Event handler handled the event, but widget will still handle the event normally. This is useful when you are augmenting base functionality"""
        CONSUMED: Widget.EventCallbackResult = gui.Widget.EventCallbackResult.CONSUMED
        """Event handler consumed the event, event handling stops, widget will not handle the event. This is useful when you are replacing functionality"""
        @property
        def value(self)->int:
            pass
        @value.setter
        def value(self, value: int):
            pass
        
    def add_child(self, child: Widget):
        pass    
    def calc_preferred_size(self,arg0: LayoutContext, constraints: Constraints)->Size:
        """
        Returns the preferred size of the widget. This is intended to be called only during layout, although it will also work during drawing. Calling it at other times will not work, as it requires some internal setup in order to function properly
        """
        pass
    def get_children(self)->t.List[Widget]:
        """
        Returns the array of children. Do not modify
        """
        pass
    @property
    def visible(self)->bool:
        pass
    @visible.setter
    def visible(self, visible: bool):
        pass
    @property
    def enabled(self)->bool:
        pass
    @enabled.setter
    def enabled(self, enabled: bool):
        pass
    @property
    def tooltip(self)->str:
        pass
    @tooltip.setter
    def tooltip(self, tooltip: str):
        pass
    @property
    def frame(self)->Rect:
        pass
    @frame.setter
    def frame(self, frame: Rect):
        pass
    @property
    def background_color(self)->Color:
        pass
    @background_color.setter
    def background_color(self, color: Color):
        pass
class Margins:
    def __new__(cls, *args, **kwargs):
        return gui.Margins(*args, **kwargs)
    def __init__(self, left: int = 0, top: int = 0, right: int = 0, bottom: int = 0):
        pass
    def lazyMarginsEM(win:Window, left_or_all: float, top: float = 0, right: float = 0, bottom: float = 0):
        if top is None or right is None or bottom is None:
            val = win.theme.font_size * left_or_all
            return Margins(val, val, val, val)
        return Margins(win.theme.font_size * left_or_all, win.theme.font_size * top, win.theme.font_size * right, win.theme.font_size * bottom)
class Theme:
    @property
    def font_size(self)->int:
        pass
    @font_size.setter
    def font_size(self, size: int):
        pass
class Open3DScene:
    class LightingProfile:
        HARD_SHADOWS: Open3DScene.LightingProfile = rendering.Open3DScene.LightingProfile.HARD_SHADOWS
        DARK_SHADOWS: Open3DScene.LightingProfile = rendering.Open3DScene.LightingProfile.DARK_SHADOWS
        MED_SHADOWS: Open3DScene.LightingProfile = rendering.Open3DScene.LightingProfile.MED_SHADOWS
        SOFT_SHADOWS: Open3DScene.LightingProfile = rendering.Open3DScene.LightingProfile.SOFT_SHADOWS
        NO_SHADOWS: Open3DScene.LightingProfile = rendering.Open3DScene.LightingProfile.NO_SHADOWS
        @property
        def value(self)->int:
            pass
        @value.setter
        def value(self, value: int):
            pass
    

    def __new__(cls, renderer: rendering.Renderer):
        return rendering.Open3DScene(renderer)
    def add_geometry(self, name: str, geometry:t.Union[Geometry3D,Geometry], material: MaterialRecord, add_downsampled_copy_for_fast_rendering: bool = True):
        pass
    def add_model(self, name: str, model: TriangleMeshModel):
        """Adds TriangleMeshModel to the scene."""
        pass
    def clear_geometry(self):
        pass
    def has_geometry(self, name: str)->bool:
        pass
    def modify_geometry_material(self, name: str, material: MaterialRecord):
        pass
    def remove_geometry(self, name: str):
        pass
    def set_background(self, color: npt.NDArray[np.float32[4,1]], image: Image = None):
        pass
    def set_background_color(self, color: npt.NDArray[np.float32[4,1]]):
        """deprecated, use set_background instead"""        
        pass
    def set_lighting(self, profile: LightingProfile, sun_dir: npt.NDArray[np.float32[3,1]]):
        """_summary_

        Args:
            profile (LightingProfile): default is MED_SHADOWS
            sun_dir (npt.NDArray[np.float32[3,1]]): default is (0.577, -0.577, -0.577)
        """
        pass
    def set_view_size(self, width: int, height: int):
        pass
    def show_axes(self, show: bool):
        pass
    def show_geometry(self, name: str, show: bool):
        pass
    def show_ground_plane(self, show: bool, axis: Scene.GroundPlane = Scene.GroundPlane.XZ):
        """Toggles display of ground plane"""
        pass
    def show_skybox(self, show: bool):
        pass
    def update_material(self, material: MaterialRecord):
        """Applies the passed material to all the geometries"""
        pass
    @property
    def background_color(self)->npt.NDArray[np.float32[4,1]]:
        pass
    @background_color.setter
    def background_color(self, color: npt.NDArray[np.float32[4,1]]):
        pass
    @property
    def bounding_box(self)->AxisAlignedBoundingBox:
        pass
    @bounding_box.setter
    def bounding_box(self, bounding_box: AxisAlignedBoundingBox):
        pass
    @property
    def camera(self)->Camera:
        pass
    @camera.setter
    def camera(self, camera: Camera):
        pass
    @property
    def downsample_threshold(self)->int:
        """若繪圖速度很重要，將這個值設小一點。"""
        pass
    @downsample_threshold.setter
    def downsample_threshold(self, downsample_threshold: int):
        pass
    @property
    def scene(self)->Scene:
        pass
    @scene.setter
    def scene(self, scene: Scene):
        pass
    @property
    def view(self)->View:
        pass
    @view.setter
    def view(self, view: View):
        pass
    
    
class SceneWidget(Widget):
    class Controls:
        ROTATE_CAMERA: SceneWidget.Controls = gui.SceneWidget.Controls.ROTATE_CAMERA
        ROTATE_CAMERA_SPHERE: SceneWidget.Controls = gui.SceneWidget.Controls.ROTATE_CAMERA_SPHERE
        FLY: SceneWidget.Controls = gui.SceneWidget.Controls.FLY
        ROTATE_SUN: SceneWidget.Controls = gui.SceneWidget.Controls.ROTATE_SUN
        ROTATE_IBL: SceneWidget.Controls = gui.SceneWidget.Controls.ROTATE_IBL
        ROTATE_MODEL: SceneWidget.Controls = gui.SceneWidget.Controls.ROTATE_MODEL
        PICK_POINTS: SceneWidget.Controls = gui.SceneWidget.Controls.PICK_POINTS
        @property
        def value(self)->int:
            pass
        @value.setter
        def value(self, value: int):
            pass
        
    
    def __new__(cls, *args, **kwargs):
        return gui.SceneWidget(*args, **kwargs)
    def __init__(self, scene: Open3DScene = None):
        """初始化一個 SceneWidget，通常會用 window.add_child(sceneWidget)，其中 window 是 Window
        - 接著通常是初始化一個 Open3dScene，然後設定 sceneWidget.scene = open3dScene
        """
        pass    
    def set_on_key(self, callback: t.Callable[[KeyEvent], Widget.EventCallbackResult]):
        """Sets a callback for key events. This callback is passed a KeyEvent object. The callback must return EventCallbackResult.IGNORED, EventCallbackResult.HANDLED, or EventCallbackResult.CONSUMED."""
        pass
    def set_on_mouse(self, callback: t.Callable[[MouseEvent], Widget.EventCallbackResult]):
        """Sets a callback for mouse events. This callback is passed a MouseEvent object. The callback must return EventCallbackResult.IGNORED, EventCallbackResult.HANDLED, or EventCallbackResult.CONSUMED."""
        pass
    def set_on_sun_direction_changed(self, callback: t.Callable[[npt.NDArray[np.float32[3,1]]], None]):
        """Callback when user changes sun direction (only called in ROTATE_SUN control mode). Called with one argument, the [i, j, k] vector of the new sun direction"""
        pass
    def set_view_controls(self, controls: Controls):
        """Sets mouse interaction, e.g. ROTATE_OBJ"""
        pass
    def setup_camera(self, field_of_view: float, model_bounds: o3d.geometry.AxisAlignedBoundingBox, center_of_rotation: npt.NDArray[np.float32[3,1]]):
        pass    
    @property
    def scene(self)->Open3DScene:
        pass
    @scene.setter
    def scene(self, scene: Open3DScene):
        pass
    
    
class FontDescription:
    def __new__(cls, *args, **kwargs):
        return gui.FontDescription(*args, **kwargs)
    def __init__(self, typeface: str = 'sans-serif'):                                       
        pass    
    def add_typeface_for_language(self,typeface: str, arg1:str):
        ''' arg1: zh_all, zh ，但 zh_all 一個 window 會佔 200Mb，而 zh 是常用的 2500 字，只佔 50 Mb
        - typeface: 如果是 windows 可設定 "c:/windows/fonts/mingliu.ttc" # 新細明體
        '''
        pass
class Slider(Widget):
    class Type:
        DOUBLE: Slider.Type = gui.Slider.Type.DOUBLE
        INT: Slider.Type = gui.Slider.Type.INT
        @property
        def value(self)->Slider.Type:
            pass
        @value.setter
        def value(self, value: Slider.Type):
            pass
    
    def __new__(cls, *args, **kwargs) -> Slider:
        return gui.Slider(*args, **kwargs)
    def __init__(self, type: Type):        
        pass
    def set_limits(self, min: float, max: float):
        """Sets the minimum and maximum values for the slider"""
        pass
    def set_on_value_changed(self, callback: t.Callable[[float], None]):
        """Sets f(new_value) which is called with a Float when user changes widget’s value"""
        pass
    @property
    def double_value(self)->float:
        """Slider value (double)"""
        pass
    @double_value.setter
    def double_value(self, double_value: float):
        """Slider value (double)"""
        pass
    @property
    def int_value(self)->int:
        """Slider value (int)"""
        pass
    @int_value.setter
    def int_value(self, int_value: int):
        """Slider value (int)"""
        pass
    @property
    def get_maximum_value(self)->float:
        """The maximum value number can contain (read-only, use set_limits() to set)"""
        pass
    @property
    def get_minimum_value(self)->float:
        """The minimum value number can contain (read-only, use set_limits() to set)"""
        pass
                 
class Label(Widget):
    def __new__(cls, *args, **kwargs) -> Label:
        return gui.Label(*args, **kwargs)
    def __init__(self, text: str = ""):
        pass
class Menu:
    def __new__(cls) -> Menu:
        return gui.Menu()        
    def __init__(self):
        pass
    def add_item(self, label: str, id: int):
        pass
    def add_separator(self):
        pass
    def set_checked(self, id: int, checked: bool):
        pass
    def set_enabled(self, id: int, enabled: bool):
        pass
    def add_menu(self, label: str, menu: Menu):
        pass   
class Layout1D(Widget):
    def __new__(cls, *args, **kwargs) -> Layout1D:
        return gui.Layout1D(*args, **kwargs)   
    def add_fixed(self, size: t.Union[int, float]):
        """Adds a fixed amount of empty space to the layout"""
        pass
    def add_stretch(self):
        """Adds empty space to the layout that will take up as much extra space as there is available in the layout"""
        pass
class Vert(Layout1D):
    def __new__(cls, *args, **kwargs) -> Vert:
        return gui.Vert(*args, **kwargs)
    def __init__(self, spacing: t.Union[int,float] = 0.0, margins: Margins = Margins()):
        pass
class Horiz(Layout1D):
    def __new__(cls, *args, **kwargs) -> Horiz:
        return gui.Horiz(*args, **kwargs)    
    def __init__(self, spacing: t.Union[int,float] = 0.0, margins: Margins = Margins()):
        pass
class CollapsableVert(Layout1D):
    def __new__(cls, *args, **kwargs) -> CollapsableVert:
        return gui.CollapsableVert(*args, **kwargs)    
    def __init__(cls, text: str, spacing: float = 0.0, margins: Margins = Margins()) -> CollapsableVert:
        pass
    def set_is_open(self, is_open: bool):
        """Sets to collapsed (False) or open (True). Requires a call to Window.SetNeedsLayout() afterwards, unless calling before window is visible"""
        pass
    def get_is_open(self)->bool:
        """Check if widget is open."""
        pass

class RadioButton(Widget):
    class Type:
        HORIZ = gui.RadioButton.Type.HORIZ
        VERT = gui.RadioButton.Type.VERT
        @property
        def value(self)->RadioButton.Type:
            pass
        @value.setter
        def value(self, value: RadioButton.Type):
            pass
    def __new__(cls, *args, **kwargs) -> RadioButton:
        return gui.RadioButton(*args, **kwargs)
    def __init__(self, type: Type):
        pass
    def set_items(self, items: t.List[str]):
        """Sets the list to display the list of items provided"""
        pass
    def set_on_selection_changed(self, callback: t.Callable[[int], None]):
        """Calls f(new_idx) when user changes selection"""
        pass
    @property
    def selected_index(self)->int:
        pass
    @selected_index.setter
    def selected_index(self, selected_index: int):
        pass
    @property
    def selected_value(self)->str:
        pass
    pass
class CheckBox(Widget):
    def __new__(cls, *args, **kwargs) -> CheckBox:
        return gui.CheckBox(*args, **kwargs)
    def __init__(self, text: str):
        pass
    def set_on_checked(self, callback: t.Callable[[bool], None]):
        """Calls passed function when checkbox changes state"""
        pass
    @property
    def checked(self)->bool:
        pass
    @checked.setter
    def checked(self, checked: bool):
        pass
    pass    

    
class Button(Widget):
    def __new__(cls, text: str) -> Self:
        return gui.Button(text)
    def set_on_clicked(self, callback: t.Callable[[], None]):
        pass
class ListView(Widget):
    def __new__(cls,*args, **kwargs) -> ListView:
        return gui.ListView(*args, **kwargs)
    def set_items(self, items: t.List[str]):
        """Sets the list to display the list of items provided"""
        pass
    def set_max_visible_items(self, max_visible_items: int):
        """Limit the max visible items shown to user. Set to negative number will make list extends vertically as much as possible, otherwise the list will at least show 3 items and at most show num items."""
        pass
    def set_on_selection_changed(self, callback: t.Callable[[str, bool], None]):
        """Calls f(new_val, is_double_click) when user changes selection"""
        pass
    @property
    def selected_index(self)->int:
        pass
    @selected_index.setter
    def selected_index(self, selected_index: int):
        pass
    @property
    def selected_value(self)->str:
        pass    
class Dialog(Widget):    
    pass
class ColorEdit(Widget):
    def __new__(cls, *args, **kwargs) -> ColorEdit:
        return gui.ColorEdit(*args, **kwargs)
    @property
    def color_value(self)-> Color:
        pass
    @color_value.setter
    def color_value(self, color_value: Color):
        pass
    pass
class FileDialog(Dialog):
    """File picker dialog"""
    class Mode:
        OPEN: FileDialog.Mode = gui.FileDialog.Mode.OPEN
        SAVE: FileDialog.Mode = gui.FileDialog.Mode.SAVE
        OPEN_DIR: FileDialog.Mode = gui.FileDialog.Mode.OPEN_DIR
        @property
        def value(self)->FileDialog.Mode:
            pass
        @value.setter
        def value(self, value: FileDialog.Mode):
            pass
    def __new__(cls, *args, **kwargs):
        return gui.FileDialog(*args, **kwargs)
    def __init__(self, mode: Mode, title: str, theme: Theme):
        """Creates either an open or save file dialog. The first parameter is either FileDialog.OPEN or FileDialog.SAVE. The second is the title of the dialog, and the third is the theme, which is used internally by the dialog for layout. The theme should normally be retrieved from window.theme.
        
        - Parameters:
            - theme: win3D.theme
        """
        pass
    def add_filter(self, extension: str, description: str):
        """Adds a selectable file-type filter: add_filter(‘.stl’, ‘Stereolithography mesh’"""
        pass
    def set_on_cancel(self, callback: t.Callable[[], None]):
        """Cancel callback; required"""
        pass
    def set_on_done(self, callback: t.Callable[[str], None]):
        """Done callback; required"""
        pass
    def set_path(self, path: str):
        """Sets the initial path path of the dialog"""
        pass
class LayoutContext:
    pass
class Window:
    def add_child(self, child: Widget):
        pass
    def close (self):
        pass
    def close_dialog(self):
        pass
    def post_redraw(self):
        '''Sends a redraw message to the OS message queue'''
        pass
    def set_focus_widget(self, widget: Widget):
        pass
    def set_needs_layout(self):
        pass
    def set_on_close(self, callback: t.Callable[[], bool]):
        """當嘗試關閉視窗時，會呼叫這個 callback，如果回傳 True，就會關閉視窗，否則就不會關閉視窗。

        Args:
            callback (t.Callable[[], bool]): 回傳False，取消關閉視窗
        """
        pass
    def set_on_layout(self, callback: t.Callable[[LayoutContext], None]):
        '''Flags window to re-layout'''
        pass
    def set_on_menu_item_activated(self, id: int, callback: t.Callable[[], None]):
        pass
    def set_on_tick_event(self, callback: t.Callable[[], bool]):
        """ tick 就是每 frame 會呼叫。一定要回傳，預設建議是 False
        - return True. 如果需要重繪，也就是任意 widget 有變動，就回傳 True
        - return False. 如果不需要重繪，就回傳 False
        
        Args:
            callback (t.Callable[[], bool]): _description_
        """
        pass
    def show(self, isVisible: bool):
        pass
    def show_dialog(self, dialog: Dialog):
        pass
    def show_menu(self, isVisible: bool):
        pass
    def show_message_box(self, title: str, message: str):
        pass
    def size_to_fit(self):
        pass
    @property
    def content_rect(self)->Rect:
        pass
    @property
    def is_active_window(self)->bool:
        pass
    @property
    def is_visible(self)->bool:
        pass
    @property
    def os_frame(self)->Rect:        
        pass
    @os_frame.setter
    def os_frame(self, os_frame: Rect):
        """
        -坑: 若要設定，必須設定 frame，只設定 frame.x 是無法生效的
        """
        pass
    
    @property
    def renderer(self)->Renderer:
        pass
    @property
    def scaling(self)->float:
        pass
    @property
    def size(self)->Size:
        pass
    @property
    def theme(self)->Theme:
        pass
    @property
    def title(self)->str:
        pass
class MouseButton:
    NONE:MouseButton = gui.MouseButton.NONE
    LEFT:MouseButton = gui.MouseButton.LEFT
    MIDDLE:MouseButton = gui.MouseButton.MIDDLE
    RIGHT:MouseButton = gui.MouseButton.RIGHT
    BUTTON4:MouseButton = gui.MouseButton.BUTTON4
    BUTTON5:MouseButton = gui.MouseButton.BUTTON5
    @property
    def value(self)->MouseButton:
        pass
    @value.setter
    def value(self, value: MouseButton):
        pass
class KeyName:
    """Names of keys. Used by KeyEvent.key"""
    # 加入上面注解中所有的
    NONE: KeyName = gui.KeyName.NONE
    BACKSPACE: KeyName = gui.KeyName.BACKSPACE
    TAB: KeyName = gui.KeyName.TAB
    ENTER: KeyName = gui.KeyName.ENTER
    ESCAPE: KeyName = gui.KeyName.ESCAPE
    SPACE: KeyName = gui.KeyName.SPACE
    EXCLAMATION_MARK: KeyName = gui.KeyName.EXCLAMATION_MARK
    DOUBLE_QUOTE: KeyName = gui.KeyName.DOUBLE_QUOTE
    HASH: KeyName = gui.KeyName.HASH
    DOLLAR_SIGN: KeyName = gui.KeyName.DOLLAR_SIGN
    PERCENT: KeyName = gui.KeyName.PERCENT
    AMPERSAND: KeyName = gui.KeyName.AMPERSAND
    QUOTE: KeyName = gui.KeyName.QUOTE
    LEFT_PAREN: KeyName = gui.KeyName.LEFT_PAREN
    RIGHT_PAREN: KeyName = gui.KeyName.RIGHT_PAREN
    ASTERISK: KeyName = gui.KeyName.ASTERISK
    PLUS: KeyName = gui.KeyName.PLUS
    COMMA: KeyName = gui.KeyName.COMMA
    MINUS: KeyName = gui.KeyName.MINUS
    PERIOD: KeyName = gui.KeyName.PERIOD
    SLASH: KeyName = gui.KeyName.SLASH
    ZERO: KeyName = gui.KeyName.ZERO
    ONE: KeyName = gui.KeyName.ONE
    TWO: KeyName = gui.KeyName.TWO
    THREE: KeyName = gui.KeyName.THREE
    FOUR: KeyName = gui.KeyName.FOUR
    FIVE: KeyName = gui.KeyName.FIVE
    SIX: KeyName = gui.KeyName.SIX
    SEVEN: KeyName = gui.KeyName.SEVEN
    EIGHT: KeyName = gui.KeyName.EIGHT
    NINE: KeyName = gui.KeyName.NINE
    COLON: KeyName = gui.KeyName.COLON
    SEMICOLON: KeyName = gui.KeyName.SEMICOLON
    LESS_THAN: KeyName = gui.KeyName.LESS_THAN
    EQUALS: KeyName = gui.KeyName.EQUALS
    GREATER_THAN: KeyName = gui.KeyName.GREATER_THAN
    QUESTION_MARK: KeyName = gui.KeyName.QUESTION_MARK
    AT: KeyName = gui.KeyName.AT
    LEFT_BRACKET: KeyName = gui.KeyName.LEFT_BRACKET
    BACKSLASH: KeyName = gui.KeyName.BACKSLASH
    RIGHT_BRACKET: KeyName = gui.KeyName.RIGHT_BRACKET
    CARET: KeyName = gui.KeyName.CARET
    UNDERSCORE: KeyName = gui.KeyName.UNDERSCORE
    BACKTICK: KeyName = gui.KeyName.BACKTICK    
    A: KeyName = gui.KeyName.A
    B: KeyName = gui.KeyName.B
    C: KeyName = gui.KeyName.C
    D: KeyName = gui.KeyName.D
    E: KeyName = gui.KeyName.E
    F: KeyName = gui.KeyName.F
    G: KeyName = gui.KeyName.G
    H: KeyName = gui.KeyName.H
    I: KeyName = gui.KeyName.I
    J: KeyName = gui.KeyName.J
    K: KeyName = gui.KeyName.K
    L: KeyName = gui.KeyName.L
    M: KeyName = gui.KeyName.M
    N: KeyName = gui.KeyName.N
    O: KeyName = gui.KeyName.O
    P: KeyName = gui.KeyName.P
    Q: KeyName = gui.KeyName.Q
    R: KeyName = gui.KeyName.R
    S: KeyName = gui.KeyName.S
    T: KeyName = gui.KeyName.T
    U: KeyName = gui.KeyName.U
    V: KeyName = gui.KeyName.V
    W: KeyName = gui.KeyName.W
    X: KeyName = gui.KeyName.X
    Y: KeyName = gui.KeyName.Y
    Z: KeyName = gui.KeyName.Z
    LEFT_BRACE: KeyName = gui.KeyName.LEFT_BRACE
    PIPE: KeyName = gui.KeyName.PIPE
    RIGHT_BRACE: KeyName = gui.KeyName.RIGHT_BRACE
    TILDE: KeyName = gui.KeyName.TILDE
    DELETE: KeyName = gui.KeyName.DELETE
    LEFT_SHIFT: KeyName = gui.KeyName.LEFT_SHIFT
    RIGHT_SHIFT: KeyName = gui.KeyName.RIGHT_SHIFT
    LEFT_CONTROL: KeyName = gui.KeyName.LEFT_CONTROL
    RIGHT_CONTROL: KeyName = gui.KeyName.RIGHT_CONTROL
    ALT: KeyName = gui.KeyName.ALT
    META: KeyName = gui.KeyName.META
    CAPS_LOCK: KeyName = gui.KeyName.CAPS_LOCK
    LEFT: KeyName = gui.KeyName.LEFT
    RIGHT: KeyName = gui.KeyName.RIGHT
    UP: KeyName = gui.KeyName.UP
    DOWN: KeyName = gui.KeyName.DOWN
    INSERT: KeyName = gui.KeyName.INSERT
    HOME: KeyName = gui.KeyName.HOME
    END: KeyName = gui.KeyName.END
    PAGE_UP: KeyName = gui.KeyName.PAGE_UP
    PAGE_DOWN: KeyName = gui.KeyName.PAGE_DOWN
    F1: KeyName = gui.KeyName.F1
    F2: KeyName = gui.KeyName.F2
    F3: KeyName = gui.KeyName.F3
    F4: KeyName = gui.KeyName.F4
    F5: KeyName = gui.KeyName.F5
    F6: KeyName = gui.KeyName.F6
    F7: KeyName = gui.KeyName.F7
    F8: KeyName = gui.KeyName.F8
    F9: KeyName = gui.KeyName.F9
    F10: KeyName = gui.KeyName.F10
    F11: KeyName = gui.KeyName.F11
    F12: KeyName = gui.KeyName.F12
    UNKNOWN: KeyName = gui.KeyName.UNKNOWN    
    @property
    def value(self)->KeyName:
        pass
    @value.setter
    def value(self, value: KeyName):
        pass
    
class KeyModifier:
    """
    Key modifier identifiers
    
    - 搭配 MouseEvent.is_modifier_down() 使用
    - 似乎不能與 KeyEvent 一起用
    """
    NONE: KeyModifier = gui.KeyModifier.NONE
    SHIFT: KeyModifier = gui.KeyModifier.SHIFT
    CTRL: KeyModifier = gui.KeyModifier.CTRL
    ALT: KeyModifier = gui.KeyModifier.ALT
    META: KeyModifier = gui.KeyModifier.META
    @property
    def value(self)->KeyModifier:
        pass
    @value.setter
    def value(self, value: KeyModifier):
        pass
class KeyEvent:
    """
    Object that stores key events
    
    - 似乎不能與 KeyModifier 一起用，所以現在還無法有 Ctrl + Z 之類的功能
    """
    class Type:
        DOWN: KeyEvent.Type = gui.KeyEvent.Type.DOWN
        UP: KeyEvent.Type = gui.KeyEvent.Type.UP
        @property
        def value(self)->KeyEvent.Type:
            pass
        @value.setter
        def value(self, value: KeyEvent.Type):
            pass
    def __call__(self, *args: Any, **kwds: Any) -> KeyEvent:
        return gui.KeyEvent(*args, **kwds)
    @property
    def is_repeat(self)->bool:
        """True if this key down event comes from a key repeat"""
        pass
    @property
    def key(self)-> t.Union[int, KeyName]:
        """This is the actual key that was pressed, not the character generated by the key. This event is not suitable for text entry"""
        pass
    @property
    def type(self)->Type:
        """Key event type"""
    pass
class MouseEvent:
    class Type:
        MOVE: MouseEvent.Type = gui.MouseEvent.Type.MOVE
        BUTTON_DOWN: MouseEvent.Type = gui.MouseEvent.Type.BUTTON_DOWN
        DRAG: MouseEvent.Type = gui.MouseEvent.Type.DRAG
        BUTTON_UP: MouseEvent.Type = gui.MouseEvent.Type.BUTTON_UP
        WHEEL: MouseEvent.Type = gui.MouseEvent.Type.WHEEL
        @property
        def value(self)->MouseEvent.Type:
            pass
        @value.setter
        def value(self, value: MouseEvent.Type):
            pass
    def is_button_down(self, button: MouseButton)->bool:
        """Convenience function to more easily deterimine if a mouse button is pressed"""
        pass
    def is_modifier_down(self, modifier: KeyModifier)->bool:
        """Convenience function to more easily deterimine if a modifier key is down"""
        pass
    
    @property
    def buttons(self)->int:
        """ORed mouse buttons"""
        pass
    @property
    def modifiers(self)->int:
        """ORed modifier keys"""
        pass
    @property
    def type(self)->Type:
        """Mouse event type"""
        pass
    @property
    def wheel_dx(self)->int:
        pass
    @property
    def wheel_dy(self)->int:
        pass
    @property
    def wheel_is_trackpad(self)->bool:
        pass
    @property
    def x(self)->int:
        pass
    @property
    def y(self)->int:
        pass
    pass
    
    
class Application: 
    """ 用 Application() 取得 Application 的 instance，是 singleton ，不會一直 new
    - 若只用 Application. 反而會有錯誤。
    
    初始化範例
    
    ```
    app = TpO3d.Application()
    app.initialize()
    
    font = TpO3d.FontDescription("c:/windows/fonts/mingliu.ttc")
    font.add_typeface_for_language("c:/windows/fonts/mingliu.ttc", "zh_all")
    app.set_font(0, font)
    
    win3D = app.create_window("3D", 768, 768)
    scene = TpO3d.SceneWidget()
    win3D.add_child(scene)
    scene3d = TpO3d.Open3DScene(win3D.renderer)
    scene.scene = scene3d
    
    app.run()
    ```
    """
    def __new__(cls) -> Self:
        return gui.Application.instance   
    def initialize(self):
        pass
    def create_window(self, title: str, width: int, height: int)->Window:
        pass
    def set_font(self,id_font:int , font: FontDescription):
        """通常為了支援中文，為是改字型才會用

        Args:
            id_font (int): 通常設 0，應該是優先順序吧
            font (FontDescription): 字型
        """
        pass
    def run(self):
        pass
    def post_to_main_thread(self, win_vis, func):
        pass
    def add_window(self, win_vis):
        pass
    def quit(self):
        pass
    @property
    def menubar(self)->t.Optional[Menu]:
        pass
    @menubar.setter
    def menubar(self, menu: Menu):
        pass
# %%
