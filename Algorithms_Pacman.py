import pygame
import queue

def run_bfs(pacman, maze, ghosts):
    path = bfs(maze, (pacman.x, pacman.y), ghosts)
    pacman.follow_path(path)

def bfs(maze, start, ghosts):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    q = queue.Queue()
    q.put((start, []))
    visited.add(start)

    while not q.empty():
        (x, y), path = q.get()
        for d in directions:
            new_pos = (x + d[0], y + d[1])
            if new_pos in ghosts or new_pos in visited or not (0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows) or maze[new_pos[1]][new_pos[0]] == 1:
                continue
            if maze[new_pos[1]][new_pos[0]] == 0:  # Target point
                return path + [new_pos]
            q.put((new_pos, path + [new_pos]))
            visited.add(new_pos)
    return []