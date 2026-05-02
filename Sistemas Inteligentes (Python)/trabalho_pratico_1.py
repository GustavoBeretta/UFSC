import heapq
import time
import json

SOLUTION = (1, 2, 3, 4, 5, 6, 7, 8, 0)

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(state):
    empty_index = state.index(0)
    empty_row, empty_column = divmod(empty_index, 3)

    neighbors = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for delta_row, delta_column in moves:
        new_row, new_col = empty_row + delta_row, empty_column + delta_column
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_index = new_row * 3 + new_col
            new_state = list(state)
            new_state[empty_index], new_state[new_zero_index] = new_state[new_zero_index], new_state[empty_index]
            neighbors.append(tuple(new_state))
            
    return neighbors

def h_uniform(state):
    return 0

def h_not_admissible(state):
    return h_manhattan(state) * 3

def h_misplaced(state):
    misplaced_count = 0
    for i in range(9):
        if state[i] != 0 and state[i] != SOLUTION[i]:
            misplaced_count += 1
    return misplaced_count

def h_manhattan(state):
    total_distance = 0
    for i in range(9):
        if state[i] != 0:
            target_index = SOLUTION.index(state[i])
            current_row, current_column = divmod(i, 3)
            target_row, target_column = divmod(target_index, 3)
            total_distance += abs(current_row - target_row) + abs(current_column - target_column)
    return total_distance

def a_star(initial_state, heuristic_func):
    max_frontier_size = 0
    nodes_visited = 0
    visited = set()
    frontier = []

    start_time = time.time()
    
    start_node = Node(initial_state, g=0, h=heuristic_func(initial_state))
    heapq.heappush(frontier, start_node)
    frontier_states = {initial_state: start_node.g}

    while frontier:
        max_frontier_size = max(max_frontier_size, len(frontier))

        current_node = heapq.heappop(frontier)

        nodes_visited += 1
        visited.add(current_node.state)

        if current_node.state == SOLUTION:
            end_time = time.time()

            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            
            return {
                "nodes_visited": nodes_visited,
                "path_length": len(path) - 1,
                "path": path[::-1],
                "execution_time": end_time - start_time,
                "max_frontier_size": max_frontier_size,
                "final_frontier": [n.state for n in frontier],
                "visited_nodes": list(visited)
            }

        for neighbor_state in get_neighbors(current_node.state):
            if neighbor_state in visited:
                continue

            tentative_g = current_node.g + 1

            if neighbor_state not in frontier_states or tentative_g < frontier_states[neighbor_state]:
                frontier_states[neighbor_state] = tentative_g
                h = heuristic_func(neighbor_state)
                neighbor_node = Node(neighbor_state, current_node, tentative_g, h)
                heapq.heappush(frontier, neighbor_node)

    return None

if __name__ == "__main__":
    print("\nEscolha a dificuldade do tabuleiro inicial:\n")
    print("1 - Fácil   (1, 2, 3, 4, 5, 6, 0, 7, 8)")
    print("2 - Médio   (0, 1, 2, 3, 4, 5, 6, 7, 8)")
    print("3 - Difícil (8, 6, 7, 2, 5, 4, 3, 0, 1)")
    opcao_dificuldade = input("\nSua escolha (1/2/3): ")

    if opcao_dificuldade == '1':
        initial_board = (1, 2, 3, 4, 5, 6, 0, 7, 8)
    elif opcao_dificuldade == '2':
        initial_board = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    else:
        initial_board = (8, 6, 7, 2, 5, 4, 3, 0, 1)

    print("\nEscolha a heurística a ser utilizada:\n")
    print("1 - Custo Uniforme)")
    print("2 - Não Admissível")
    print("3 - Peças fora do lugar")
    print("4 - Distância de Manhattan")
    opcao_heuristica = input("\nSua escolha (1/2/3/4): ")

    if opcao_heuristica == '1':
        heuristica = h_uniform
        nome_heuristica = "Custo Uniforme"
    elif opcao_heuristica == '2':
        heuristica = h_not_admissible
        nome_heuristica = "Heurística Não Admissível"
    elif opcao_heuristica == '3':
        heuristica = h_misplaced
        nome_heuristica = "Peças fora do lugar"
    else:
        heuristica = h_manhattan
        nome_heuristica = "Distância de Manhattan"

    print(f"\nExecutando A* com a heurística: {nome_heuristica} ...\n")
    
    result = a_star(initial_board, heuristica)

    if result:
        print("=== CAMINHO ENCONTRADO ===")
        for step, state in enumerate(result['path']):
            print(f"Passo {step}: {state}")
        print("==========================\n")

        print(f"a) Total de Nodos Visitados: {result['nodes_visited']}")
        print(f"b) Tamanho do Caminho: {result['path_length']}")
        print(f"c) Tempo de Execução: {result['execution_time']:.8f} segundos")
        print(f"d) Maior tamanho da fronteira: {result['max_frontier_size']}")

        output_data = {
            "fronteira_final": result["final_frontier"],
            "visitados": result["visited_nodes"]
        }
        with open("a_star_data.json", "w") as json_file:
            json.dump(output_data, json_file, indent=4)
        print("e) Arquivo 'a_star_data.json' gerado com sucesso!\n")
    else:
        print("Não foi possível encontrar uma solução para esse tabuleiro.\n")