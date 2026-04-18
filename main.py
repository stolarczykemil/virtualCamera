from graphics import process_key, clip_edge, project_vertices
from utils import load_edges, load_vertices
import numpy as np
import pygame

def main():
    vertices = load_vertices("data/vertices.txt")
    vertices = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    edges = load_edges("data/edges.txt")
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height))
    fov = 90
    mode = False
    scene_matrix = np.eye(4)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    mode = not mode
                scene_matrix, fov = process_key(scene_matrix, event.key, mode, fov)
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
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
