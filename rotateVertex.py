from scipy.spatial.transform import Rotation as R
import numpy as np

def rotateVertex(vertex, rotationArray):
    rotation = R.from_rotvec(rotationArray)
    return(rotation.apply(vertex))
