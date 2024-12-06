import pygame
import random
from collections import deque
import sys
from Draw_Button import Button
from Algorithms import bfs,dfs,a_star,greedy_search,uniform_cost_search,hill_climbing,genetic_algorithm,beam_search,simulated_annealing
import queue
from Setting import draw_settings_panel,handle_dropdown_events,init_dropdown_states

from Panel import draw_info_panel

pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 1500  # Điều chỉnh kích thước để phù hợp với kích thước lưới
SCREEN_HEIGHT = 750
GRID_SIZE = 40  # Kích thước ô lưới
game_started = False
# Thiết lập màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman AI")
is_settings_open = False
# Tải hình ảnh
pacman_image = pygame.image.load("images/pacman.png")
ghost_image = pygame.image.load("images/ghost.png")
wall_image = pygame.image.load("images/wall.png")
pellet_image = pygame.image.load("images/pellet.png")

# Chuyển đổi kích thước hình ảnh để phù hợp với GRID_SIZE
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))
ghost_image = pygame.transform.scale(ghost_image, (GRID_SIZE, GRID_SIZE))
wall_image = pygame.transform.scale(wall_image, (GRID_SIZE, GRID_SIZE))
pellet_image = pygame.transform.scale(pellet_image, (GRID_SIZE // 2, GRID_SIZE // 2))

score = 0

# Hàm cập nhật điểm số

start_time = pygame.time.get_ticks()

def draw_score_and_time(screen, score, elapsed_time):
    font = pygame.font.Font(None, 36)  # Chọn font
    minutes = elapsed_time // 60000
    seconds = (elapsed_time % 60000) // 1000
    time_text = f"Time: {minutes:02}:{seconds:02}"
    score_text = f"Score: {score}"
    text = font.render(f"{score_text}  {time_text}", True, (255, 255, 255))  # Tạo văn bản điểm số và thời gian
    screen.blit(text, (10, 10))

import pygame


import heapq
def runbfs(maze, start, ghosts):
    
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    q = queue.Queue()
    q.put((start, []))
    visited.add(start)

    def is_safe(new_pos):
        for ghost in ghosts:
            if abs(new_pos[0] - ghost[0]) <= 1 and abs(new_pos[1] - ghost[1]) <= 1:
                return False
        return True

    while not q.empty():
        (x, y), path = q.get()
        for d in directions:
            new_pos = (x + d[0], y + d[1])
            if new_pos in visited or not (0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows) or maze[new_pos[1]][new_pos[0]] == 1:
                continue
            if not is_safe(new_pos):
                continue  # Avoid positions too close to ghosts
            if maze[new_pos[1]][new_pos[0]] == 2:  # Target point (food)
                return path + [new_pos]
            q.put((new_pos, path + [new_pos]))
            visited.add(new_pos)
    return []

def a_start(maze, start, ghosts):
    
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited.add(start)

    def is_safe(new_pos):
        for ghost in ghosts:
            if abs(new_pos[0] - ghost[0]) <= 1 and abs(new_pos[1] - ghost[1]) <= 1:
                return False
        return True

    def heuristic(pos, target):
        return abs(pos[0] - target[0]) + abs(pos[1] - target[1])

    while pq:
        cost, (x, y), path = heapq.heappop(pq)
        if maze[y][x] == 2:  # Target point (food)
            return path + [(x, y)]
        for d in directions:
            new_pos = (x + d[0], y + d[1])
            if new_pos in visited or not (0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows) or maze[new_pos[1]][new_pos[0]] == 1:
                continue
            if not is_safe(new_pos):
                continue  # Avoid positions too close to ghosts
            new_cost = cost + 1 + heuristic(new_pos, (x, y))
            heapq.heappush(pq, (new_cost, new_pos, path + [new_pos]))
            visited.add(new_pos)
    return []



def run_dfs(maze, start, ghosts):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    visited = set()
    stack = [(start, [])]
    visited.add(start)

    def is_safe(new_pos):
        for ghost in ghosts:
            if abs(new_pos[0] - ghost[0]) <= 1 and abs(new_pos[1] - ghost[1]) <= 1:
                return False
        return True

    while stack:
        (x, y), path = stack.pop()
        for d in directions:
            new_pos = (x + d[0], y + d[1])
            if new_pos in visited or not (0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows) or maze[new_pos[1]][new_pos[0]] == 1:
                continue
            if not is_safe(new_pos):
                continue  # Avoid positions too close to ghosts
            if maze[new_pos[1]][new_pos[0]] == 2:  # Target point (food)
                return path + [new_pos]
            stack.append((new_pos, path + [new_pos]))
            visited.add(new_pos)
    return []

def update_score():
    global score
    score += 10


class Pacman:
    def __init__(self, x, y, move_delay=0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.move_delay = move_delay
        self.move_counter = 0
        self.pacman_image = pacman_image
        self.path = []
        self.is_hunting = False  # Initialize is_hunting attribute
        self.hunting_time = 0  #
    def update_direction(self, dx, dy):
        self.dx = dx
        self.dy = dy
    def move(self, maze):
        if self.move_counter >= self.move_delay:
            if maze[self.y + self.dy][self.x + self.dx] != 1:
                if maze[self.y + self.dy][self.x + self.dx] == 2:
                    update_score()  # Viên đạn bình thường
                    maze[self.y + self.dy][self.x + self.dx] = 0
                elif maze[self.y + self.dy][self.x + self.dx] == 3:  # Viên đạn đặc biệt
                    update_score(50)  # Tăng điểm cho viên đạn đặc biệt
                    maze[self.y + self.dy][self.x + self.dx] = 0
                    self.is_hunting = True  # Bắt đầu chế độ săn
                    self.hunting_time = 5 * 60  # 5 giây ở 60 FPS
                self.x += self.dx
                self.y += self.dy
            self.move_counter = 0
        else:
            self.move_counter += 1

        # Giảm thời gian săn nếu đang trong chế độ săn
        if self.is_hunting:
            self.hunting_time -= 1
            if self.hunting_time <= 0:
                self.is_hunting = False  # Tăng bộ đếm sau mỗi khung hình

    def follow_path(self, path):
        self.path = path
        if self.path:
            next_pos = self.path[0]
            self.update_direction(next_pos[0] - self.x, next_pos[1] - self.y)

    def draw(self, screen):
        if self.dx == 1:
            rotated_image = pygame.transform.rotate(self.pacman_image, 0)
        elif self.dx == -1:
            rotated_image = pygame.transform.rotate(self.pacman_image, 180)
        elif self.dy == 1:
            rotated_image = pygame.transform.rotate(self.pacman_image, 270)
        elif self.dy == -1:
            rotated_image = pygame.transform.rotate(self.pacman_image, 90)
        else:
            rotated_image = self.pacman_image
        screen.blit(rotated_image, (self.x * GRID_SIZE, self.y * GRID_SIZE))

# Định nghĩa lớp Ghost
class Ghost:
    def __init__(self, x, y, algorithm, image, color, move_delay=1):
        self.x = x
        self.y = y
        self.move_delay = move_delay  # Số khung hình phải đợi trước khi di chuyển
        self.move_counter = 0
        self.algorithm = algorithm  # Thuật toán di chuyển
        self.image = image
        self.color = color  # Thêm màu sắc riêng cho Ghost
        self.original_position = (x, y)  # Lưu vị trí gốc
        self.is_alive = True
        self.trail = deque(maxlen=50)  # Lưu vết, tối đa 50 vị trí

    def reset_position(self):
        self.x, self.y = self.original_position  # Khôi phục về vị trí gốc
        self.is_alive = True
        self.trail.clear()  # Xóa vết di chuyển

    def move(self, target_x, target_y, maze):
        # Chỉ di chuyển khi bộ đếm đạt đến giá trị delay
        if self.move_counter >= self.move_delay:
            if self.algorithm == 'BFS':
                path = bfs((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'DFS':
                path = dfs((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'A*':
                path = a_star((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Greedy':
                path = greedy_search((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Uniform Cost':
                path = uniform_cost_search((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Hill Climbing':
                path = hill_climbing((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Simulated Annealing':
                path = simulated_annealing((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Genetic Algorithm':
                path = genetic_algorithm((self.x, self.y), (target_x, target_y), maze)
            elif self.algorithm == 'Beam Search':
                path = beam_search((self.x, self.y), (target_x, target_y), maze)


            if path and len(path) > 1:  # Kiểm tra nếu path hợp lệ và có nhiều hơn một bước
                self.x, self.y = path[1]
                self.trail.append((self.x, self.y))
            else:
                print(f"{self.algorithm} không tìm thấy lộ trình hợp lệ.")
            # Lưu vị trí mới vào vết di chuyển
            self.move_counter = 0  # Reset bộ đếm sau khi di chuyển
        else:
            self.move_counter += 1  # Tăng bộ đếm sau mỗi khung hình

    def draw(self, screen):
        # Vẽ dấu vết trước
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, [(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2) for x, y in self.trail], 3)
        # Vẽ ghost với màu sắc đã chỉ định
        screen.blit(self.image, (self.x * GRID_SIZE, self.y * GRID_SIZE))

def find_valid_spawn_positions(maze):
    valid_positions = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 0 or cell == 2:  # Empty space or food
                valid_positions.append((x, y))
    return valid_positions


def draw_score(screen):
    font = pygame.font.Font(None, 36)  # Chọn font
    text = font.render(f"Score: {score}", True, (255, 255, 255))  # Tạo văn bản điểm số
    screen.blit(text, (10, 10))  # Vẽ văn bản lên màn hình
# Hàm vẽ mê cung
def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 1:
                screen.blit(wall_image, (x * GRID_SIZE, y * GRID_SIZE))
            elif tile == 2:
                screen.blit(pellet_image, (x * GRID_SIZE + GRID_SIZE // 4, y * GRID_SIZE + GRID_SIZE // 4))


def create_maze() :
    return (
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )

maze = create_maze()

def reset_game():
    global pacman, ghosts, score, maze,start_time

    # Lưu các cài đặt thuật toán hiện tại
    ghost_algorithms = [ghost.algorithm for ghost in ghosts]

    # Reset Pacman's position
    pacman = Pacman(1, 1)
    valid_positions = find_valid_spawn_positions(maze)
    x1,y1 = random.choice(valid_positions)
    x2,y2 = random.choice(valid_positions)
    x3,y3 = random.choice(valid_positions)
    x4,y4 = random.choice(valid_positions)

    # Reset Ghost positions nhưng giữ nguyên thuật toán đã chọn
    ghosts = [
        Ghost(x1, y1, algorithm='BFS', image=blue, color=(0, 0, 255)),  # blue
        Ghost(x2, y2, algorithm='Greedy', image=green, color=(0, 255, 0)),  # green
        Ghost(x3, y3, algorithm='A*', image=red, color=(255, 0, 0)),  # red
        Ghost(x4, y4, algorithm='Uniform Cost', image=yellow, color=(255, 255, 0))
    ]

    # Reset the score
    score = 0

    # Reset the maze with pellets (2) and walls (1)
    maze = create_maze()
    start_time = pygame.time.get_ticks()

def check_collision():
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            return True
    return False

ghosts_paused = False
pacman = Pacman(1, 1)
#ghost = Ghost(12, 5)

blue = pygame.image.load("images/blue.png")
green = pygame.image.load("images/green.png")
red = pygame.image.load("images/red.png")
yellow = pygame.image.load("images/yellow.png")

valid_positions = find_valid_spawn_positions(maze)
x1,y1 = random.choice(valid_positions)
x2,y2 = random.choice(valid_positions)
x3,y3 = random.choice(valid_positions)
x4,y4 = random.choice(valid_positions)

    # Reset Ghost positions nhưng giữ nguyên thuật toán đã chọn
ghosts = [
        Ghost(x1, y1, algorithm='BFS', image=blue, color=(0, 0, 255)),  # blue
        Ghost(x2, y2, algorithm='Greedy', image=green, color=(0, 255, 0)),  # green
        Ghost(x3, y3, algorithm='A*', image=red, color=(255, 0, 0)),  # red
        Ghost(x4, y4, algorithm='Uniform Cost', image=yellow, color=(255, 255, 0))
]

dropdown_states = init_dropdown_states(ghosts)
# Vòng lặp game
running = True
clock = pygame.time.Clock()

# Game loop

settings_button = Button("Setting",(1300,250),"Settings")
start_button = Button("Reset",(1300,50),"Reset")
quit_button = Button("Stop",(1300,150),"Stop")
pause_button = Button("Pause",(1300,350),"Pause")
def handle_button_clicks(event):
    global game_started
    # Handle existing button clicks
    # ...
    # Handle pause button click
    if pause_button.is_clicked(event):
        game_started = not game_started 


while running:
    screen.fill((0, 0, 0))

    # Event handling
    events = pygame.event.get()  # Chỉ gọi pygame.event.get() một lần
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Nhấn nút Settings
            if settings_button.is_clicked(event):
                is_settings_open = True

            if is_settings_open:
                dropdown_rects, dropdown_options_list, close_button = draw_settings_panel(screen, ghosts,
                                                                                          dropdown_states)
                handle_dropdown_events(event, dropdown_rects, dropdown_options_list, ghosts, dropdown_states)

                mouse_pos = pygame.mouse.get_pos()

                # Kiểm tra nếu nút "Close" được nhấn
                if close_button.collidepoint(mouse_pos):
                    is_settings_open = False# Thay đổi thuật toán cho tất cả ma

        # Nếu Settings đang đóng, xử lý game logic
        if not is_settings_open:
            game_started = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p :  # Dừng/tiếp tục ma
                    ghosts_paused = not ghosts_paused

                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:

                    if event.key == pygame.K_LEFT:
                        pacman.dx, pacman.dy = -1, 0
                    elif event.key == pygame.K_RIGHT:
                        pacman.dx, pacman.dy = 1, 0
                    elif event.key == pygame.K_UP:
                        pacman.dx, pacman.dy = 0, -1
                    elif event.key == pygame.K_DOWN:
                        pacman.dx, pacman.dy = 0, 1

            if start_button.is_clicked(event):
                reset_game()
                game_started = False

            if quit_button.is_clicked(event):
                running = False
            if pause_button.is_clicked(event):  # Dừng/tiếp tục ma
                ghosts_paused = not ghosts_paused
                game_started = not game_started 

    # Nếu Settings đang mở, chỉ vẽ giao diện Settings
    if is_settings_open:
        dropdown_rect, dropdown_options, close_button = draw_settings_panel(screen, ghosts,
                                                                                          dropdown_states)
    else:
        # Các logic game khác (di chuyển Pacman, Ghosts)
        if game_started:
            ghosts_positions = [(ghost.x, ghost.y) for ghost in ghosts if ghost.is_alive]
            pacman.follow_path(run_dfs(maze, (pacman.x, pacman.y), ghosts_positions))

            pacman.move(maze)

            if not ghosts_paused:
                for ghost in ghosts:
                    ghost.move(pacman.x, pacman.y, maze)
                    if ghost.is_alive and pacman.x == ghost.x and pacman.y == ghost.y:
                        if pacman.is_hunting:
                            ghost.is_alive = False
                            pygame.time.set_timer(pygame.USEREVENT, 5000)
                        else:
                            reset_game()
        else:
        # Nếu game đang tạm dừng, không di chuyển Pacman và Ghosts
            draw_maze(screen, maze)
            elapsed_time = pygame.time.get_ticks() - start_time
            draw_score_and_time(screen, score, elapsed_time)
            pacman.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen)
                if not ghost.is_alive:
                    ghost.reset_position()
        draw_maze(screen, maze)
        draw_score(screen)
        elapsed_time = pygame.time.get_ticks() - start_time
        draw_score_and_time(screen, score, elapsed_time)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
            if not ghost.is_alive:
                ghost.reset_position()

        if ghosts_paused:
            font = pygame.font.Font(None, 74)
            text = font.render("Ghosts Paused", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Luôn vẽ các nút
    draw_info_panel(screen)
    settings_button.draw(screen)
    start_button.draw(screen)
    quit_button.draw(screen)
    pause_button.draw(screen)
    # Update display and clock tick
    pygame.display.flip()
    clock.tick(5)

