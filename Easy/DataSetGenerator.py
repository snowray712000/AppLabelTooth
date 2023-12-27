# %%
import numpy as np
import tensorflow as tf
from Easy.easys import easy

# %%


class DataSetGenerator:
    def __init__(self):
        self.npoints = 16000  # down sample
        self.channels = 6  # x y z nx ny nz
        self.batch = 1  # 目前用1
        self.dataset_train = None
        self.dataset_val = None
        self.dataset_test = None
        self.dir_tf = './../Crown_Tf_230915/lower/'  # 以 lower 為例, 這裡面要有 train val 資料夾

    def generateDataSet(self, train_val: str) -> tf.data.TFRecordDataset:
        pathlist_pattern = f'{self.dir_tf}/{train_val}/*.tfrecords'
        pathlist = easy.io.enumFiles(pathlist_pattern)
        if len(pathlist) == 0:
            return None

        def _preprocess_fn(data_record):

            in_features = {
                'points': tf.io.FixedLenFeature([], tf.string),
                'labels': tf.io.FixedLenFeature([], tf.string)
            }

            sample = tf.io.parse_single_example(data_record, in_features)

            points = sample['points']
            labels = sample['labels']

            points = tf.io.decode_raw(points, tf.float32)
            labels = tf.io.decode_raw(labels, tf.int8)

            labels = tf.cast(labels, tf.int64)  # training 是用 int64

            n_points = self.npoints
            channels = self.channels  # x y z nx ny nz
            points = tf.reshape(points, (n_points, channels))
            labels = tf.reshape(labels, (n_points, 1))

            shuffle_idx = tf.range(points.shape[0])
            shuffle_idx = tf.random.shuffle(shuffle_idx)
            points = tf.gather(points, shuffle_idx)
            labels = tf.gather(labels, shuffle_idx)

            return points, labels

        dataset = tf.data.TFRecordDataset(pathlist)
        dataset = dataset.shuffle(len(pathlist))
        dataset = dataset.map(_preprocess_fn)
        cardinality = tf.data.experimental.cardinality(dataset)

        if (cardinality == tf.data.experimental.UNKNOWN_CARDINALITY).numpy():
            dataset = dataset.apply(
                tf.data.experimental.assert_cardinality(len(pathlist)))

        batch_size = self.batch  # 目前用1
        dataset = dataset.batch(batch_size, drop_remainder=True)
        return dataset

    def main(self, n_points, channels, dir_tf='./../Crown_Tf_230915/lower/'):
        ''' 先呼叫 os.chdir(Paths.s.dirTfRecords) 
        dir_tf 是以 lower 為例
        '''
        self.npoints = n_points
        self.channels = channels
        self.dir_tf = dir_tf
        self.dataset_train = self.generateDataSet(train_val="train")
        self.dataset_val = self.generateDataSet(train_val="val")
        # self.dataset_test = self.generateDataSet(train_val="test")  # 已沒用
        return self

    def testMain():  # static
        DataSetGenerator.s.main(
            n_points=16000, channels=6, dir_tf='./../Crown_Tf_230915/lower/')
        print(DataSetGenerator.s.dataset_train)


if __name__ == "__main__":
    import open3d as o3d
    # 載入
    dataSetGen = DataSetGenerator()
    dataSetGen.main(n_points=16000, channels=6,
                    dir_tf='./../Crown_Tf_230915/lower/')
    print(dataSetGen.dataset_train)

    # 測試對不對
    r1 = dataSetGen.dataset_train
    # BatchDataset 無法使用 r1[0]，而是要用 for each 才能取得；可結合 .skip 或 .take 取得
    for a1 in r1.take(1):
        # rr1 = a1['points'] # 取得 'points' 雖然直覺，但卻是錯的，它是回傳個 tuple 不是 dict。所以要以 a1[0] 取得 points 資料
        # a1[0] 的 0, 是 tuple, numpy()[0] 的 0 是batch的第1個。
        points = a1[0].numpy()[0]
        labels = a1[1].numpy()[0]
        print("labels info ", labels.shape, np.unique(labels.reshape(-1)))
        print(np.max(points, axis=0), np.min(points, axis=0))

        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(points[:, :3])
        pc.normals = o3d.utility.Vector3dVector(points[:, 3:])

        obj = pc
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(
            min(obj.get_max_bound() - obj.get_min_bound()))
        o3d.visualization.draw_geometries(
            [axis, obj], mesh_show_back_face=True, point_show_normal=True, mesh_show_wireframe=False)
        break
