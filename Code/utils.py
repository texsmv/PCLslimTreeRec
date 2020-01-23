import trimesh
import subprocess
import time

def reduceVertex(mesh, vertices = 1024):
    mesh.export("temp.obj")
    subprocess.run(["Manifold/build/manifold", "temp.obj", "temp.obj", "1500"])

    mesh = trimesh.load("temp.obj")

    n_tries = 0
    while(mesh.vertices.shape[0] != vertices):
        n_vertices = mesh.vertices.shape[0]
        n_faces = mesh.faces.shape[0]
        out_faces = n_faces - ((n_vertices - vertices) * 2)

        subprocess.run(["Manifold/build/simplify", "-i", "temp.obj", "-o","temp.obj","-m", "-f", str(out_faces)] )

        mesh = trimesh.load("temp.obj")
        n_tries += 1
        if n_tries >= 3:
            return None

    subprocess.run(["rm","temp.obj"])
    return mesh


# mesh = trimesh.load('Dataset/ModelNet10/bathtub/bathtub_0005.obj')
# mesh = reduceVertex(mesh)
# mesh.show()

# mesh = trimesh.load("/home/texs/hdd/Datasets/ModelNet10/ModelNet10/chair/train/chair_0772.off")
# mesh = reduceVertex(mesh)
# if mesh != None:
#     mesh.show()