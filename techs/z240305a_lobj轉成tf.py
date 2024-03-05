#%%
from add_parent_dir_to_sys_path import set_cwd_and_add_parent_dir_to_sys_path_callme_initially
set_cwd_and_add_parent_dir_to_sys_path_callme_initially()
from Easy import *

#%%
# 列舉 tf 資料夾下的所有 .lobj 檔
import glob
pathLObjs = glob.glob('./../../tf/*/*/*.lobj')
#%%
from Easy.FilterOfOutlier import FilterOfOutlier

def sliceMultiLayer(points: npt.NDArray, labels:npt.NDArray, isLower:bool)->t.List[npt.NDArray]:
    z = points[:,2]
    zmax, zmin = np.max(z), np.min(z)
    
    zTeeth = z[labels != 0]
    zTeethMaxOrMin = np.min(zTeeth) if isLower else np.max(zTeeth)
    
    # 例如 1.31
    ratio = (zmax - zmin) / (zmax - zTeethMaxOrMin) if isLower else (zmax - zmin) / (zTeethMaxOrMin - zmin)
    
    # 例如 1.31 1.21 1.11 1.01
    ratios = np.arange(ratio, 1, -0.1)
    
    def fn1(ratio):
        if isLower:
            return zmax - ratio * (zmax - zTeethMaxOrMin)
        return zmin + ratio * (zTeethMaxOrMin - zmin)
    zlimits = lq.linq(ratios).select(fn1).to_list()
    
    idxsOfLimit = lq.linq(zlimits).select(lambda zlimit: z > zlimit if isLower else z < zlimit).to_list()
    return idxsOfLimit
#%
def generateXyznnnLabel(points: npt.NDArray, normals: npt.NDArray, labels:npt.NDArray)->t.Tuple[npt.NDArray, npt.NDArray]:
    
    idxs = easyo3d.farthest_point_down_sample(points, 16000)
    
    xyz2a = points[idxs]
    normals2 = normals[idxs]
    labels2 = labels[idxs]
    
    xyz2b = (xyz2a - np.mean(xyz2a, axis=0)) / np.std(xyz2a[:,0])
    
    return np.hstack([xyz2b, normals2], dtype=np.float32), labels2

import tensorflow as tf
def export_tfrecord_for_pointnetpp(path_record, xyznnn, labels):
    with tf.io.TFRecordWriter(path_record) as tfwriter:
        ftrs = tf.train.Features(
            feature={
                'points': tf.train.Feature(bytes_list=tf.train.BytesList(value=[xyznnn.tobytes()])),
                'labels': tf.train.Feature(bytes_list=tf.train.BytesList(value=[labels.tobytes()]))
            }
        )
        example = tf.train.Example(features=ftrs)
        tfwriter.write(example.SerializeToString())
        tfwriter.close()
        
countPath = len(pathLObjs)    
for iPath, pathLobj in enumerate( pathLObjs ):
    lobj = LabeledObject().read(pathLobj)
    mesh = easyo3d.toMesh2(lobj)
    normals = np.array(mesh.vertex_normals)
    
    isLower = 'lower' in os.path.basename(pathLobj)
    
    idxsNonOutlier = FilterOfOutlier().main(lobj, 'lower' if isLower else 'upper', mesh)
    
    points2 = lobj[0][idxsNonOutlier]
    normals2 = normals[idxsNonOutlier]
    labels2 = lobj[3][idxsNonOutlier]
    
    # 切多層
    idxsOfLimit = sliceMultiLayer(points2, labels2, isLower)
    
    paths_tfrecords = [pathLobj.replace('.lobj', f'_{i}.tfrecords') for i in range(len(idxsOfLimit))]
    
    for i, idxLimit in enumerate( idxsOfLimit ):
        points3 = points2[idxLimit]
        normals3 = normals2[idxLimit]
        labels3 = labels2[idxLimit]
        
        xyznnn, labels4 = generateXyznnnLabel(points3, normals3, labels3)
        export_tfrecord_for_pointnetpp(paths_tfrecords[i], xyznnn, labels4) 
    
    print(f'{iPath}/{countPath} done')
