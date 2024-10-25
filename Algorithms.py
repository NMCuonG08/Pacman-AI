from collections import deque

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
    stack = [start]
    visited = set()
    parents = {start: None}

    while stack:
        current = stack.pop()
        if current == target:
            path = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]

        visited.add(current)
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = (x + dx, y + dy)
            if (0 <= next_pos[0] < len(maze[0]) and
                0 <= next_pos[1] < len(maze) and
                maze[next_pos[1]][next_pos[0]] != 1 and
                next_pos not in visited):
                stack.append(next_pos)
                parents[next_pos] = current
    return None









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

    queue = PriorityQueue()
    queue.put((0, start))
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
                queue.put((heuristic(next_pos, target), next_pos))
                parents[next_pos] = current
    return None



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
