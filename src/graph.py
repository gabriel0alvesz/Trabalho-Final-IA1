from Read_docs import ReadDocs
import networkx as nx
import matplotlib.pyplot as plt
import heapq
from collections import deque

def preenche_listas():
    rd = ReadDocs()
    rd.ReadDoc("./files/vertices.txt")
    v = rd.Tokenizer()
    
    rd.ReadDoc("./files/arcos.txt")
    aux_arcos = rd.Tokenizer()
    aux_arcos = [linha.split('/') for linha in aux_arcos]
    arcos = [[city[0], city[1], float(city[2])] for city in aux_arcos]
    
    return v, arcos

def gera_grafo(v: list, a: list) -> nx.Graph:
    grafo = nx.Graph()
    for i in range(0, len(v)):
        grafo.add_node(v[i])
    for j in range(0, len(a)):
        grafo.add_edge(a[j][0], a[j][1], weight=a[j][2])
    return grafo

def degree_heuristic(u: str, v: str, g: nx.Graph):
    # print(f"{u} -> {v} = {g.degree(u) - g.degree(v)}")
    return abs(g.degree(u) - g.degree(v))

def heuristic_dijkstra(u: str, v: str, grafo: nx.Graph):
    return 0

def a_star_custom(g: nx.Graph, start: str, goal: str, heuristic) -> tuple:
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    g_costs = {start: 0}
    f_costs = {start: heuristic(start, goal, g)}
    came_from = {}
    
    explored_nodes = set()
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, len(explored_nodes), g_costs[goal]
        
        explored_nodes.add(current)
        
        for neighbor in g.neighbors(current):
            weight = g[current][neighbor]['weight']
            tentative_g_cost = g_costs[current] + weight
            
            if neighbor not in g_costs or tentative_g_cost < g_costs[neighbor]:
                came_from[neighbor] = current
                g_costs[neighbor] = tentative_g_cost
                f_costs[neighbor] = tentative_g_cost + heuristic(neighbor, goal, g)
                if neighbor not in explored_nodes:
                    heapq.heappush(open_set, (f_costs[neighbor], neighbor))
    
    return [], len(explored_nodes), 0

def bfs(g: nx.Graph, start: str, goal: str) -> tuple:
    queue = deque([start])
    came_from = {start: None}
    explored_nodes = set()
    
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, len(explored_nodes), sum(g[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        
        explored_nodes.add(current)
        
        for neighbor in g.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
    
    return [], len(explored_nodes), 0

def dfs(g: nx.Graph, start: str, goal: str) -> tuple:
    stack = [start]
    came_from = {start: None}
    explored_nodes = set()
    
    while stack:
        current = stack.pop()
        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, len(explored_nodes), sum(g[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
        
        explored_nodes.add(current)
        
        for neighbor in g.neighbors(current):
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
    
    return [], len(explored_nodes), 0

def caminho_total_real(caminho: list, grafo: nx.Graph) -> float:
    custo_total: float = 0.0

    for i in range(len(caminho) - 1):
        no_atual = caminho[i]
        proximo_no = caminho[i + 1]
        
        if grafo.has_edge(no_atual, proximo_no):
            custo_total += grafo[no_atual][proximo_no]['weight']
    
    return custo_total

def resultados_Astar(start: str, destinos: list, grafo: nx.Graph, heuristic) -> dict:
    current_node = start

    total_path = [start]
    total_cost = 0.1
    total_explored = 0
    
    for destination in destinos:
        # A* Algorithm
        path, explored_nodes, cost = a_star_custom(grafo, current_node, destination, heuristic)
        if not path:
            print(f"ERRO: Não há caminho entre {current_node} e {destination}!")
            return {'path': [], 'explored': 0, 'cost': 0}
        
        total_path.extend(path[1:])
        total_cost += cost
        total_explored += explored_nodes
        current_node = destination
    
    
    return {'path': total_path, 'explored': total_explored, 'cost': total_cost, 'cost_real_path': caminho_total_real(total_path, grafo)}

def resultados_BFS(start: str, destinos: list, grafo: nx.Graph) -> dict:
    
    current_node = start
    total_path = [start]
    total_cost = 0.1
    total_explored = 0

    for i in range(0, len(destinos)):
        path, explored_nodes, cost = bfs(grafo, current_node, destinos[i])
        if not path:
            print(f"ERRO: Não há caminho entre {current_node} e {destinos[i]}!")
            return {'path': [], 'explored': 0, 'cost': 0}

        total_path.extend(path[1:])
        total_cost += cost
        total_explored += explored_nodes
        current_node = destinos[i] 
    
    return {'path': total_path, 'explored': total_explored, 'cost': total_cost}

def resultados_DFS(start: str, destinos: list, grafo: nx.Graph) -> dict:
    
    current_node = start
    total_path = [start]
    total_cost = 0.1
    total_explored = 0

    for i in range(0, len(destinos)):
        path, explored_nodes, cost = dfs(grafo, current_node, destinos[i])
        if not path:
            print(f"ERRO: Não há caminho entre {current_node} e {destinos[i]}!")
            return {'path': [], 'explored': 0, 'cost': 0}

        total_path.extend(path[1:])
        total_cost += cost
        total_explored += explored_nodes
        current_node = destinos[i]
    
    return {'path': total_path, 'explored': total_explored, 'cost': total_cost}

def plota_grafo(g: nx.Graph, algoritmo: str, caminho: list = []):
    
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(g, seed=31, k=7)
    
    # Desenha os nós
    nx.draw(g, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight='bold', edge_color="gray")
    
    path_edges = []
    # Destaca o caminho encontrado
    if(caminho):
        path_edges = list(zip(caminho, caminho[1:]))  # Converte o caminho em uma lista de arestas
    
    nx.draw_networkx_edges(g, pos, edgelist=path_edges, edge_color="red", width=3)
    
    labels = nx.get_edge_attributes(g, 'weight')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

    plt.title("Grafo com Caminho Destacado")
    plt.savefig(f"./assets/{algoritmo}.png")


def print_resultados(algoritmo: str, resultados: dict, plot: bool = False):
    print(f"Grafo: {grafo}\n")
    print(algoritmo)    
    print(f"  Caminho encontrado: {resultados['path']}")
    print(f"  Número total de nós explorados: {resultados['explored']}")
   
    
    if algoritmo == "Astar_Grau" or algoritmo == "Astar_Dijkstra":
        print(f"  Custo real do caminho: {round(resultados['cost_real_path'], 2)}")
    else:{
         print(f"  Custo total do caminho: {round(resultados['cost'],3)}")
    }
        
    if plot:
        plota_grafo(grafo, algoritmo, resultados['path'])


if __name__ == "__main__":
    vertice, arcos = preenche_listas()

    grafo = gera_grafo(vertice, arcos)

    destinos = ["J.K", "Peixe Vivo", "Barro Preto"]
    
    resultados = resultados_Astar("Loja-SUPREMA", destinos, grafo, heuristic_dijkstra)

    print_resultados("Astar_Dijkstra", resultados, plot=True)

