from collections import deque
import random
import math


def bfs(start, target, maze):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parents = {start: None}
    while queue:
        current = queue.popleft()
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1 and
                next_pos not in visited):
                queue.append(next_pos)
                visited.add(next_pos)
                parents[next_pos] = current
    return None


def dfs(start, target, maze):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các hướng di chuyển
    stack = [start]          # Stack để duyệt DFS
    visited = set()          # Lưu các vị trí đã thăm
    visited.add(start)
    parents = {start: None}  # Lưu đường đi

    while stack:
        current = stack.pop()  # Lấy vị trí hiện tại từ stack
        if current == target:  # Nếu đến mục tiêu, dựng lại đường đi
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]  # Trả về đường đi từ start -> target

        x, y = current
        for dx, dy in directions:
            next_pos = (x + dx, y + dy)

            # Kiểm tra điều kiện hợp lệ
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1 and
                next_pos not in visited):
                stack.append(next_pos)  # Thêm vào stack
                visited.add(next_pos)   # Đánh dấu đã thăm
                parents[next_pos] = current  # Cập nhật cha của ô đó

    return None  # Trả về None nếu không tìm thấy đường đi


def a_star(start, target, maze):
    from queue import PriorityQueue

    queue = PriorityQueue()
    queue.put((0, start))
    g_costs = {start: 0}
    parents = {start: None}

    while not queue.empty():
        current = queue.get()[1]
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1):
                new_g_cost = g_costs[current] + 1
                if next_pos not in g_costs or new_g_cost < g_costs[next_pos]:
                    g_costs[next_pos] = new_g_cost
                    f_cost = new_g_cost + heuristic(next_pos, target)
                    queue.put((f_cost, next_pos))
                    parents[next_pos] = current
    return None

def heuristic(a, b):
    # Hàm heuristic sử dụng khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])






def greedy_search(start, target, maze):
    from queue import PriorityQueue

    queue = PriorityQueue()  # Hàng đợi ưu tiên cho Greedy Search
    queue.put((0, start))    # Đưa vị trí bắt đầu vào hàng đợi với heuristic = 0
    visited = set()          # Để kiểm tra các ô đã thăm
    parents = {start: None}  # Lưu đường đi

    while not queue.empty():
        current = queue.get()[1]  # Lấy ô có giá trị heuristic thấp nhất
        if current == target:     # Nếu đến đích, dựng lại đường đi
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]     # Trả về đường đi từ start -> target

        visited.add(current)      # Đánh dấu ô hiện tại đã thăm
        x, y = current

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)

            # Kiểm tra điều kiện hợp lệ
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1 and
                next_pos not in visited):
                queue.put((heuristic(next_pos, target), next_pos))  # Thêm vào hàng đợi với heuristic
                parents[next_pos] = current  # Cập nhật cha của ô đó

    return None  # Trả về None nếu không tìm thấy đường đi




def uniform_cost_search(start, target, maze):
    from queue import PriorityQueue

    queue = PriorityQueue()
    queue.put((0, start))
    g_costs = {start: 0}
    parents = {start: None}

    while not queue.empty():
        current = queue.get()[1]
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1):
                new_cost = g_costs[current] + 1
                if next_pos not in g_costs or new_cost < g_costs[next_pos]:
                    g_costs[next_pos] = new_cost
                    queue.put((new_cost, next_pos))
                    parents[next_pos] = current
    return None

def hill_climbing(start, target, maze):
    current = start
    visited = set()
    path = [current]

    while current != target:
        visited.add(current)
        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                     if 0 <= x + dx < len(maze[0]) and 0 <= y + dy < len(maze) and maze[y + dy][x + dx] != 1]
        neighbors = [n for n in neighbors if n not in visited]

        if not neighbors:
            return None  # Stuck in a local maximum

        # Pick the neighbor with the lowest heuristic value (closer to the target)
        current = min(neighbors, key=lambda n: heuristic(n, target))
        path.append(current)

    return path


def genetic_algorithm(start, target, maze, population_size=20, generations=100, mutation_rate=0.1, path_length=100):
    def generate_individual():
        # Generate a random sequence of moves
        return [random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)]) for _ in range(path_length)]

    def fitness(individual):
        position = start
        visited = set()
        for move in individual:
            x, y = position
            dx, dy = move
            next_pos = (x + dx, y + dy)
            # Ensure the next position is within bounds and not a wall
            if (0 <= next_pos[0] < len(maze[0]) and
                    0 <= next_pos[1] < len(maze) and
                    maze[next_pos[1]][next_pos[0]] != 1):
                position = next_pos
                visited.add(next_pos)
            if position == target:
                break
        return -heuristic(position, target), position  # Return fitness and the final position

    def mutate(individual):
        if random.random() < mutation_rate:
            idx = random.randint(0, len(individual) - 1)
            individual[idx] = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def crossover(parent1, parent2):
        idx = random.randint(0, len(parent1) - 1)
        return parent1[:idx] + parent2[idx:]

    # Initialize population
    population = [generate_individual() for _ in range(population_size)]

    best_individual = None
    best_position = None
    for generation in range(generations):
        # Sort population based on fitness (descending order)
        population = sorted(population, key=lambda ind: fitness(ind)[0], reverse=True)
        next_gen = population[:2]  # Elitism: Keep top 2 individuals

        while len(next_gen) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)
            offspring = crossover(parent1, parent2)
            mutate(offspring)
            next_gen.append(offspring)

        population = next_gen

        # Track the best individual across generations
        current_best = max(population, key=lambda ind: fitness(ind)[0])
        current_fitness, current_position = fitness(current_best)
        if not best_individual or current_fitness > fitness(best_individual)[0]:
            best_individual = current_best
            best_position = current_position

        # Optionally terminate early if a solution is found
        if best_position == target:
            break

    # Return the path (list of moves) and the final position reached
    return best_individual, best_position


def beam_search(start, target, maze, beam_width=2):
    beams = [(start, [start])]
    while beams:
        new_beams = []
        for current, path in beams:
            if current == target:
                return path

            x, y = current
            neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                         if 0 <= x + dx < len(maze[0]) and 0 <= y + dy < len(maze) and maze[y + dy][x + dx] != 1]
            for neighbor in neighbors:
                if neighbor not in path:
                    new_path = path + [neighbor]
                    new_beams.append((neighbor, new_path))

        # Sort beams by heuristic and keep the best ones
        beams = sorted(new_beams, key=lambda b: heuristic(b[0], target))[:beam_width]

    return None

def simulated_annealing(start, target, maze, initial_temperature=100, cooling_rate=0.99):
    current = start
    path = [current]
    temperature = initial_temperature

    while temperature > 1:
        if current == target:
            return path

        x, y = current
        neighbors = [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                     if 0 <= x + dx < len(maze[0]) and 0 <= y + dy < len(maze) and maze[y + dy][x + dx] != 1]

        if not neighbors:
            return None

        next_move = random.choice(neighbors)
        delta_e = heuristic(current, target) - heuristic(next_move, target)

        if delta_e > 0 or random.random() < math.exp(delta_e / temperature):
            current = next_move
            path.append(current)

        temperature *= cooling_rate

    return None

