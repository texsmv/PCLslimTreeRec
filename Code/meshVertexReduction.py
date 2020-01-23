import trimesh
import numpy as np
import pandas as pd
import os
from os.path import join, isdir, isfile
from os import listdir, mkdir
from Code.utils import reduceVertex


DATASET_DIRS = "Dataset/dirs.txt"
DATASET_PATH = "/home/texs/hdd/Datasets/ModelNet10/ModelNet10"
DATASET_OUTPUT_PATH = "Dataset/ModelNet10"
B_TRAIN = True

"""[summary]
    Load class paths of Dataset, can be either training or testing data
Returns:
    [array, array] -- [names of classes, absolute paths of classes]
"""
def getModelNet10Dirs():
    dirs = pd.read_csv(DATASET_DIRS, header=None)
    dirs = dirs.to_numpy().flatten()
    complete_dirs = [join(DATASET_PATH, dir) for dir in dirs]
    if B_TRAIN:
        complete_dirs = [join(dir, "train") for dir in complete_dirs]
    else:
        complete_dirs = [join(dir, "test") for dir in complete_dirs]
    return dirs, complete_dirs




classes, dirs = getModelNet10Dirs()

if not isdir(DATASET_OUTPUT_PATH):
    mkdir(DATASET_OUTPUT_PATH)


pcl = []
for i in range(len(dirs)):
    dir = dirs[i]
    pcl_names = listdir(dir)
    pcl_dirs = [join(dir, d) for d in pcl_names]
    class_dir = join(DATASET_OUTPUT_PATH, classes[i])
    if not isdir(class_dir):
        mkdir(class_dir)

    
    for i in range(len(pcl_dirs)):
        # Convert to OBJ file
        print("-------------------------------------------")
        print(pcl_dirs[i])
        try:
            pcl = trimesh.load(pcl_dirs[i])
        except:
            print("----------------------------Error loading: ", pcl_dirs[i])
        else:
            
            pcl = reduceVertex(pcl)
            if pcl != None:
                pcl.export(join(class_dir, pcl_names[i][:-3] + "off"))
                print(pcl_names[i], " exported succesfully")
            else:
                print("couldn't export")
    









