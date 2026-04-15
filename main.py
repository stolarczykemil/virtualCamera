import numpy as np
import pygame

def load_vertices(filename):
    with open(filename, "r") as f:
        vertices = []
        for line in f:
            points = line.split()
            if len(points) == 3:
                vertices.append([float(points[0]), float(points[1]), float(points[2])])
    return np.array(vertices)

def load_edges(filename):
    with open(filename, "r") as f:
        edges = []
        for line in f:
            parts = line.split()
            if len(parts) == 2:
                edges.append([int(parts[0]), int(parts[1])])
    return edges

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

def process_key(scene_matrix, key, mode):
    return np.eye(4)

def main():
    vertices = load_vertices("data/vertices.txt")
    vertices = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    edges = load_edges("data/edges.txt")
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    fov = 90
    mode = True
    scene_matrix = np.eye(4)
    running = True
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                mode = not mode
            scene_matrix = process_key(scene_matrix, event.key, mode)
            transformed_vertices = vertices @ scene_matrix.T
            screen.fill((0, 0, 0))
            for edge in edges:
                clipped = clip_edge(transformed_vertices[edge[0]], transformed_vertices[edge[1]])
                if clipped is not None:
                    cv1, cv2 = clipped
                    points_to_project = np.array([cv1, cv2])
                    projected = project_vertices(points_to_project, width, height, fov)
                    p1 = projected[0]
                    p2 = projected[1]
                    pygame.draw.line(screen, (255, 255, 255), p1, p2, 1)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
