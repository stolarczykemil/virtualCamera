import numpy as np

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