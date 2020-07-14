import pandas as pd
import numpy as np
import collections
import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)

import time
import datetime
import csv

start = time.time()
start_time = datetime.datetime.now().time()

# Cenário 3

class Vertex:
    def __init__(self, value):
        self.value = value
        self.neighbours = list()

    def add_neighbour(self, vertex):
        if vertex not in self.neighbours:
            self.neighbours.append(vertex)

class Graph:
    vertices = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.value not in self.vertices:
            self.vertices[vertex.value] = vertex
            return True
        else:
            return False
    
    def add_edge(self, u, v):
        self.vertices[v].add_neighbour(u)
        self.vertices[u].add_neighbour(v)
    
    def print_graph(self):
        for key in sorted(list(self.vertices.keys())):
            print(key + str(self.vertices[key].neighbours))


def read_file():
    data = pd.read_csv(r'traducao3.txt', sep=" ", header=None, skiprows=2)
    data.columns=['A', 'B']
    return data

def build_graph(data):
    # Escolher entre (matriz, lista de adjacencia ou lista de pares).   
    numero_vertices_max = data["A"].max()
    numero_vertices = data["A"].shape[0]
    
    arrayVertices1 = data["A"].to_list()
    arrayVertices2 = data["B"].to_list()

    grafo = Graph()
    for item in range(int(numero_vertices_max)):
        grafo.add_vertex(Vertex(item))
    
    for item in range(numero_vertices - 1):
        grafo.add_edge(arrayVertices1[item], arrayVertices2[item])
    
    return grafo


def bfs(graph, root):
    distance = 0
    visited = []
    visited.append(root)
    queue = collections.deque([(root, distance)])
    array_count = []
    count_dist = 0

    while queue:
        v, distance = queue.popleft()
        if v != root:
            array_count.append([v, distance])
        count_size = 0

        for neighbour in graph.vertices[v].neighbours:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append((neighbour, distance + 1))


    return array_count


def main():

    data = read_file()
    grafo = build_graph(data)

    array_res = bfs(grafo, 0)
    
    end = time.time()
    end_time = datetime.datetime.now().time()
    print('Tempo de execução: \n', end - start, '\n\nHorário de execução: \ninicio:', start_time, '\n', 'término: ', end_time)

    num_cols = []
    count = 0

    with open("ep4.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(array_res)

main()