import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib.pyplot as plt
import math as m

fig = plt.figure()

#创建3d绘图区域
ax = plt.axes(projection='3d')
# ax = plt.axes()

size = 2
ax.scatter(size,0,0)
ax.scatter(0,size,0)
ax.scatter(0,0,size)
ax.scatter(-size,0,0)
ax.scatter(0,-size,0)
ax.scatter(0,0,-size)

roller_direction = np.array([0,-1])

# path_direction = [-0.12010435,0.99276127]
path_direction = np.array([203547,-25803]) - np.array([203389,-27109])
path_direction_length = np.linalg.norm(path_direction)
path_direction_norm = path_direction / path_direction_length
print(path_direction,path_direction_length,path_direction_norm,roller_direction)

a = np.dot(roller_direction,path_direction) / path_direction_length
degrees = m.degrees(m.acos(a))
print('dot',a)

r = np.cross(roller_direction,path_direction)
print('cross',r)
if r < 0:
    degrees = 180 + 180 - degrees

print(degrees)

ax.plot([0,roller_direction[0]],[0,roller_direction[1]],[0,0])
ax.plot([0,path_direction_norm[0]],[0,path_direction_norm[1]],[0,0])

plt.show(block=True)


