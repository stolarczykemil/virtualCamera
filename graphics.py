import numpy as np
import pygame

def clip_edge(v1, v2):
    if v1[2] >= 0.1 and v2[2] >= 0.1:
        return v1, v2
    if v1[2] <= 0.1 and v2[2] <= 0.1:
        return None
    if v1[2] > v2[2]:
        v1, v2 = v2, v1
    t = (0.1 - v1[2]) / (v2[2] - v1[2])
    v1_clipped = v1 + t * (v2 - v1)
    return v1_clipped, v2

def project_vertices(vertices, width, height, fov):
    x_proj = vertices[:, 0] / vertices[:, 2]
    y_proj = vertices[:, 1] / vertices[:, 2]
    fov_scale = 1.0 / np.tan(np.radians(fov) / 2)
    x_screen = x_proj  * fov_scale * (width / 2) + width / 2
    y_screen = -y_proj * fov_scale * (height / 2) + height / 2
    projected_points = np.column_stack((x_screen, y_screen)).astype(int)
    return projected_points

def get_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def get_rotation_x_matrix(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])

def get_rotation_y_matrix(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ])

def get_rotation_z_matrix(angle):
    c, s = np.cos(angle), np.sin(angle)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])


def process_key(scene_matrix, key, mode, fov):
    speed = 0.5
    rot_speed = 0.05
    zoom_speed = 2.0

    transform = np.eye(4)
    if not mode:
        if key == pygame.K_w:
            transform = get_translation_matrix(0, 0, -speed)
        elif key == pygame.K_s:
            transform = get_translation_matrix(0, 0, speed)
        elif key == pygame.K_a:
            transform = get_translation_matrix(speed, 0, 0)
        elif key == pygame.K_d:
            transform = get_translation_matrix(-speed, 0, 0)
        elif key == pygame.K_q:
            transform = get_translation_matrix(0, -speed, 0)
        elif key == pygame.K_e:
            transform = get_translation_matrix(0, speed, 0)

        elif key == pygame.K_UP:
            fov = max(10, fov - zoom_speed)
        elif key == pygame.K_DOWN:
            fov = min(170, fov + zoom_speed)
    else:
        if key == pygame.K_w:
            transform = get_rotation_x_matrix(rot_speed)
        elif key == pygame.K_s:
            transform = get_rotation_x_matrix(-rot_speed)
        elif key == pygame.K_a:
            transform = get_rotation_y_matrix(rot_speed)
        elif key == pygame.K_d:
            transform = get_rotation_y_matrix(-rot_speed)
        elif key == pygame.K_q:
            transform = get_rotation_z_matrix(-rot_speed)
        elif key == pygame.K_e:
            transform = get_rotation_z_matrix(rot_speed)
    new_scene_matrix = transform @ scene_matrix
    return new_scene_matrix, fov