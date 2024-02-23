import os
import io
import struct # byte to int
import numpy as np
import open3d as o3d
import Easy.TpO3d as TpO3d
def readStlBinary(fp,isReadNormal):
    '''有時要讀給 open3d 的 mesh，它會重算 normal，就可以不用傳'''
    
    fp.seek(80,os.SEEK_SET)
    
    count_tri = struct.unpack('I', fp.read(4))[0]

    if isReadNormal == False:
        vertexs = np.zeros( (count_tri,3,3), dtype=np.float32 )
        for i in range(count_tri):
            fp.seek(12, os.SEEK_CUR)
            r1 = fp.read(36)
            fp.seek(2, os.SEEK_CUR)
            vertexs[i] = np.frombuffer(r1, dtype=np.float32).reshape((3,3))
        return vertexs, None
    else:
        normals = np.zeros( (count_tri,3), dtype=np.float32 )
        vertexs = np.zeros( (count_tri,3,3), dtype=np.float32 )
        for i in range(count_tri):
            r1 = fp.read(12)
            normals[i] = np.frombuffer(r1, dtype=np.float32)

            r1 = fp.read(36)
            fp.seek(2, os.SEEK_CUR)
            vertexs[i] = np.frombuffer(r1, dtype=np.float32).reshape((3,3))
        return vertexs, normals
    return None,None
def readStlBinary_ToO3dMesh(fp)-> TpO3d.TriangleMesh:
    """讀取 stl 檔，並轉成 open3d 的 mesh，也有作 sop
    """
    vertexs, normals = readStlBinary(fp, isReadNormal=False)
    vertexs = vertexs.reshape((-1,3))
    
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertexs)    
    ids = np.arange(len(vertexs), dtype=np.int32).reshape((-1,3))
    mesh.triangles = o3d.utility.Vector3iVector(ids)
    
    mesh.remove_duplicated_vertices()
    mesh.remove_degenerate_triangles()
    mesh.remove_duplicated_triangles()
    mesh.compute_vertex_normals()
    mesh.compute_triangle_normals()

    return mesh

if __name__ == "__main__":
    import open3d as o3d
    path = "./../CrownSegmentationNew/1/upper_mod.stl"
    
    # test4
    with open(path,"rb") as file:
        mesh = readStlBinary_ToO3dMesh(file)
        obj = mesh
        axis = o3d.geometry.TriangleMesh.create_coordinate_frame(min(obj.get_max_bound() - obj.get_min_bound()))
        o3d.visualization.draw_geometries([axis, obj], mesh_show_back_face=True, point_show_normal=True, mesh_show_wireframe=False)

    # test3
    with open(path,"rb") as file:
        vertexs, normals = readStlBinary(file, isReadNormal=False)
    # test2
    with open(path,"rb") as file:
        r1 = file.read()
        with io.BytesIO(r1) as file2:
            stl = readStlBinary(file2, isReadNormal=True)    
    # test1
    with open(path,"rb") as file:
        stl = readStlBinary(file, isReadNormal=True)
    

        
    