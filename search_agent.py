import heapq
from collections import deque
import math

def parse_map(map_str):
    grid = [list(line) for line in map_str.strip().split('\n')]
    start = None
    goal = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == 'S':
                start = (x, y)
            elif char == 'G':
                goal = (x, y)
    return grid, start, goal

def get_neighbors(pos, grid):
    x, y = pos
    neighbors = []
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != '#':
            neighbors.append((nx, ny))
    return neighbors

def heuristic_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def heuristic_zero(p1, p2):
    return 0

def heuristic_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def heuristic_manhattan_x2(p1, p2):
    return 2 * (abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))

def a_star(map_str, heuristic_func=heuristic_manhattan):
    grid, start, goal = parse_map(map_str)
    if not start or not goal:
        return None, 0
    
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    states_expanded = 0

    while frontier:
        _, current = heapq.heappop(frontier)
        states_expanded += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], states_expanded

        for nxt in get_neighbors(current, grid):
            new_g = g_score[current] + 1
            if nxt not in g_score or new_g < g_score[nxt]:
                g_score[nxt] = new_g
                f_score = new_g + heuristic_func(nxt, goal)
                heapq.heappush(frontier, (f_score, nxt))
                came_from[nxt] = current

    return None, states_expanded

def bfs(map_str):
    grid, start, goal = parse_map(map_str)
    if not start or not goal:
        return None, 0
    
    frontier = deque([start])
    came_from = {start: None}
    states_expanded = 0

    while frontier:
        current = frontier.popleft()
        states_expanded += 1

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return path[::-1], states_expanded

        for nxt in get_neighbors(current, grid):
            if nxt not in came_from:
                came_from[nxt] = current
                frontier.append(nxt)

    return None, states_expanded

if __name__ == '__main__':
    warehouse_map = """
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################
"""
    
    print("Running A* (Manhattan)...")
    path_a, exp_a = a_star(warehouse_map)
    print(f"Path Length: {len(path_a)-1 if path_a else 'No path'}, Expanded: {exp_a}")

    print("Running BFS...")
    path_b, exp_b = bfs(warehouse_map)
    print(f"Path Length: {len(path_b)-1 if path_b else 'No path'}, Expanded: {exp_b}")
