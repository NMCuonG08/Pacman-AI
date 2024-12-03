import pygame
import random
from collections import deque
import sys
import os
from Algorithms_Pacman import run_bfs


# Thêm đường dẫn hiện tại vào sys.path để import các module tùy chỉnh
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Draw_Button import Button
from Algorithms import bfs, dfs, a_star, greedy_search, uniform_cost_search, hill_climbing, genetic_algorithm, beam_search, simulated_annealing
from Setting import draw_settings_panel, handle_dropdown_events, init_dropdown_states
from Panel import draw_info_panel

pygame.init()

# Kích thước màn hình và lưới
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
GRID_SIZE = 40

# Thiết lập màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman AI")

# Tải hình ảnh
pacman_image = pygame.image.load("images/pacman.png")
ghost_image = pygame.image.load("images/ghost.png")
wall_image = pygame.image.load("images/wall.png")
pellet_image = pygame.image.load("images/pellet.png")

blue = pygame.image.load("images/blue.png")
green = pygame.image.load("images/green.png")
red = pygame.image.load("images/red.png")
yellow = pygame.image.load("images/yellow.png")

# Chuyển đổi kích thước hình ảnh
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))
ghost_image = pygame.transform.scale(ghost_image, (GRID_SIZE, GRID_SIZE))
wall_image = pygame.transform.scale(wall_image, (GRID_SIZE, GRID_SIZE))
pellet_image = pygame.transform.scale(pellet_image, (GRID_SIZE // 2, GRID_SIZE // 2))
is_settings_open = False
game_started = False

blue = pygame.transform.scale(blue, (GRID_SIZE, GRID_SIZE))
green = pygame.transform.scale(green, (GRID_SIZE, GRID_SIZE))
red = pygame.transform.scale(red, (GRID_SIZE, GRID_SIZE))
yellow = pygame.transform.scale(yellow, (GRID_SIZE, GRID_SIZE))





score = 0

# Hàm cập nhật điểm số
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
        self.is_hunting = False
        self.hunting_time = 0
        self.path = []  # Thêm thuộc tính path để lưu đường đi

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

        if self.is_hunting:
            self.hunting_time -= 1
            if self.hunting_time <= 0:
                self.is_hunting = False

    def follow_path(self, path):
        self.path = path

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

class Ghost:
    def __init__(self, x, y, image, color, move_delay=1):
        self.x = x
        self.y = y
        self.move_delay = move_delay
        self.move_counter = 0
        self.image = image
        self.color = color
        self.original_position = (x, y)
        self.is_alive = True
        self.trail = deque(maxlen=50)

    def reset_position(self):
        self.x, self.y = self.original_position
        self.is_alive = True
        self.trail.clear()

    def move(self, maze):
        if self.move_counter >= self.move_delay:
            possible_moves = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for d in directions:
                new_pos = (self.x + d[0], self.y + d[1])
                if maze[new_pos[1]][new_pos[0]] != 1:
                    possible_moves.append(new_pos)
            if possible_moves:
                self.x, self.y = random.choice(possible_moves)
                self.trail.append((self.x, self.y))
            self.move_counter = 0
        else:
            self.move_counter += 1

    def draw(self, screen):
        if len(self.trail) > 1:
            pygame.draw.lines(screen, self.color, False, [(x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2) for x, y in self.trail], 3)
        screen.blit(self.image, (self.x * GRID_SIZE, self.y * GRID_SIZE))

def draw_score(screen):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def draw_maze(screen, maze):
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            if tile == 1:
                screen.blit(wall_image, (x * GRID_SIZE, y * GRID_SIZE))
            elif tile == 2:
                screen.blit(pellet_image, (x * GRID_SIZE + GRID_SIZE // 4, y * GRID_SIZE + GRID_SIZE // 4))

def create_maze():
    return (
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    )

maze = create_maze()


def get_possible_positions(maze):
    positions = []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell != 1:  # Assuming 1 represents a wall
                positions.append((x, y))
    return positions

def initialize_ghosts(maze, ghost_images):
    possible_positions = get_possible_positions(maze)
    ghosts = []
    for color, image in ghost_images:
        x, y = random.choice(possible_positions)
        ghosts.append(Ghost(x, y, image=image, color=color))
        possible_positions.remove((x, y))  # Ensure no two ghosts start at the same position
    return ghosts

ghost_images = [
    ((0, 0, 255), blue),
    ((0, 255, 0), red),
    ((255, 0, 0), green),
    ((255, 255, 0), yellow)
]

def reset_game():
    global pacman, ghosts, score, maze

    pacman = Pacman(1, 1)

    ghosts = initialize_ghosts(maze, ghost_images)

    score = 0
    maze = create_maze()

def check_collision():
    for ghost in ghosts:
        if pacman.x == ghost.x and pacman.y == ghost.y:
            return True
    return False

ghosts_paused = False
pacman = Pacman(1, 1)

ghosts = initialize_ghosts(maze, ghost_images)

dropdown_states = init_dropdown_states(ghosts)
running = True
clock = pygame.time.Clock()

settings_button = Button("Setting", (1300, 250), "Settings")
BFSbtn =  Button("BFS", (1300, 450), "BFS")
start_button = Button("Reset", (1300, 50), "Reset")
quit_button = Button("Stop", (1300, 150), "Stop")
pause_button = Button("Pause", (1300, 350), "Pause")

def handle_button_clicks(event):
    global game_started
    if pause_button.is_clicked(event):
        game_started = not game_started

while running:
    screen.fill((0, 0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if settings_button.is_clicked(event):
                is_settings_open = True

            if is_settings_open:
                dropdown_rects, dropdown_options_list, close_button = draw_settings_panel(screen, ghosts, dropdown_states)
                handle_dropdown_events(event, dropdown_rects, dropdown_options_list, ghosts, dropdown_states)

                mouse_pos = pygame.mouse.get_pos()

                if close_button.collidepoint(mouse_pos):
                    is_settings_open = False
            if BFSbtn.is_clicked(event):
                print("BFS")
                run_bfs(pacman, maze, ghosts)
                
                
                
        if not is_settings_open:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    ghosts_paused = not ghosts_paused

                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    game_started = True
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
            if pause_button.is_clicked(event):
                ghosts_paused = not ghosts_paused

    if is_settings_open:
        dropdown_rect, dropdown_options, close_button = draw_settings_panel(screen, ghosts, dropdown_states)
    else:
        if game_started:
            pacman.move(maze)

            if not ghosts_paused:
                for ghost in ghosts:
                    ghost.move(maze)
                    if ghost.is_alive and pacman.x == ghost.x and pacman.y == ghost.y:
                        if pacman.is_hunting:
                            ghost.is_alive = False
                            pygame.time.set_timer(pygame.USEREVENT, 5000)
                        else:
                            reset_game()

        draw_maze(screen, maze)
        draw_score(screen)
        pacman.draw(screen)
        for ghost in ghosts:
            ghost.draw(screen)
            if not ghost.is_alive:
                ghost.reset_position()

        if ghosts_paused:
            font = pygame.font.Font(None, 74)
            text = font.render("Ghosts Paused", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    draw_info_panel(screen)
    settings_button.draw(screen)
    pacman.move(maze)
    start_button.draw(screen)
    quit_button.draw(screen)
    pause_button.draw(screen)
    BFSbtn.draw(screen)

    pygame.display.flip()
    clock.tick(5)

if __name__ == "__main__":
    main()