"""Обеспечить реализацию алгоритма выявления видимых граней и ребер для одиночного выпуклого объемного тела."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation

vertices = np.array([
    [0,0,0],[1,0,0],[1,1,0],[0,1,0],
    [0,0,1],[1,0,1],[1,1,1],[0,1,1]
])

faces = [
    [0,1,2,3],
    [4,5,6,7],
    [0,1,5,4],
    [2,3,7,6],
    [1,2,6,5],
    [0,3,7,4]
]

ELEV, AZIM = 20, 30

def rotate_y(verts, angle):
    c, s = np.cos(angle), np.sin(angle)
    Ry = np.array([[c, 0, s],
                   [0, 1, 0],
                   [-s, 0, c]])
    center = np.mean(verts, axis=0)
    return (verts - center) @ Ry.T + center

def get_camera_vector(elev, azim):
    elev_r = np.deg2rad(elev)
    azim_r = np.deg2rad(azim)
    vx = np.cos(elev_r) * np.cos(azim_r)
    vy = np.cos(elev_r) * np.sin(azim_r)
    vz = np.sin(elev_r)
    return np.array([vx, vy, vz])

def is_face_visible(face, verts, view_vector):
    p1, p2, p3 = verts[face[0]], verts[face[1]], verts[face[2]]
    normal = np.cross(p2 - p1, p3 - p1)
    cube_center = np.mean(verts, axis=0)
    face_center = np.mean([verts[i] for i in face], axis=0)
    to_center = face_center - cube_center
    if np.dot(normal, to_center) < 0:
        normal = -normal
    return np.dot(normal, view_vector) > 0

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

view_vector = get_camera_vector(ELEV, AZIM)

def update(angle):
    ax.clear()
    rotated = rotate_y(vertices, angle)
    visible_faces = [face for face in faces if is_face_visible(face, rotated, view_vector)]
    poly3d = [[rotated[i] for i in face] for face in visible_faces]

    ax.add_collection3d(Poly3DCollection(poly3d, facecolors='skyblue', edgecolors='black', linewidths=1, alpha=0.5))
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    ax.set_zlim(-1, 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.view_init(elev=ELEV, azim=AZIM)

ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 180), interval=60)

plt.show()
