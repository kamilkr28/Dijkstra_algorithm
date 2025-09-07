import math
import matplotlib.pyplot as plt
import networkx as nx

class Graph:
    def __init__(self, graph_dict=None, directed=True):
        self.directed = directed
        self.graph = graph_dict if graph_dict else {}
        self.distances = None
        self.prev = None

    def add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, w))
        if v not in self.graph:      
            self.graph[v] = []
        if not self.directed:
            if v not in self.graph:
                self.graph[v] = []
            self.graph[v].append((u, w))

    def dijkstra(self, start):
        dist = {node: math.inf for node in self.graph}
        dist[start] = 0
        prev = {node: None for node in self.graph}
        visited = set()

        while len(visited) < len(self.graph):
            current = None
            current_dist = math.inf
            for node in self.graph:
                if node not in visited and dist[node] < current_dist:
                    current = node
                    current_dist = dist[node]

            if current is None:
                break

            visited.add(current)

            for neighbor, weight in self.graph.get(current, []):
                new_dist = dist[current] + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current

        self.distances = dist
        self.prev = prev
        return dist, prev

    def get_path(self, end):
        if end not in self.graph:
            print(f"Wierzchołek {end} nie istnieje w grafie.")
            return None
        
        if self.prev is None or self.distances is None:
            raise ValueError("Najpierw wywołaj dijkstra(start)")

        if end not in self.distances or self.distances[end] == math.inf:
            print(f"Nie istnieje ścieżka do wierzchołka {end}.")
            return None

        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = self.prev.get(cur)
        path.reverse()
        return path

    def shortest_path_from(self, start, end, pos=None):
        if start not in self.graph:
            print(f"Wierzchołek startowy {start} nie istnieje w grafie.")
            return None, None
        self.dijkstra(start)
        path = self.get_path(end)
        if path is None:
            print(f"Nie można znaleźć ścieżki do wierzchołka {end}.")
            return None, None
        
        weight = self.distances.get(end)

        print(f"Najkrótsza ścieżka z {start} do {end}: {path}")
        print(f"Minimalna waga ścieżki: {weight}")

        if pos is not None:
            Visualizer.draw(self.graph, pos=pos, path=path, title=f"Ścieżka {start} -> {end}")
        return path, weight


class Visualizer:
    @staticmethod
    def draw(graph_dict, pos, path=None, title="Graf"):
        G = nx.DiGraph()
        for u, edges in graph_dict.items():
            for v, w in edges:
                G.add_edge(u, v, weight=w)

        plt.figure(figsize=(10, 6))
        nx.draw(
            G, pos,
            with_labels=True,
            node_color="lightblue",
            node_size=2000,
            font_size=12,
            arrows=True,
            font_weight="bold"
        )
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange')
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
            
            path_edge_labels = {(u, v): G[u][v]['weight'] for u, v in path_edges}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=path_edge_labels, font_size=14, font_color='red', label_pos=0.5)
        


        plt.title(title)
        plt.axis('off')
        plt.show()
