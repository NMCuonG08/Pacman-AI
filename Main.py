import pygame
import random
from collections import deque
import sys
from Draw_Button import Button
from Algorithms import bfs,dfs,a_star,greedy_search,uniform_cost_search

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 1500  # Điều chỉnh kích thước để phù hợp với kích thước lưới
SCREEN_HEIGHT = 750
GRID_SIZE = 40  # Kích thước ô lưới

# Thiết lập màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman AI")

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
def update_score():
    global score
    score += 10
# Định nghĩa lớp Pacman
import pygame

class Pacman:
    def __init__(self, x, y, move_delay=2):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.move_delay = move_delay  # Số khung hình phải đợi trước khi di chuyển
        self.move_counter = 0  # Bộ đếm để kiểm soát tốc độ di chuyển
        self.pacman_image = pacman_image  # Tải ảnh Pacman

    def update_direction(self, dx, dy):
        """ Cập nhật hướng đi theo phím bấm """
        self.dx = dx
        self.dy = dy

    def move(self, maze):
        # Chỉ di chuyển khi bộ đếm đạt giá trị delay
        if self.move_counter >= self.move_delay:
            # Kiểm tra xem vị trí tiếp theo có phải là tường không (1 đại diện cho tường)
            if maze[self.y + self.dy][self.x + self.dx] != 1:
                if maze[self.y + self.dy][self.x + self.dx] == 2:
                    update_score()  # Cập nhật điểm số nếu ăn pellet
                    maze[self.y + self.dy][self.x + self.dx] = 0
                self.x += self.dx
                self.y += self.dy
            self.move_counter = 0  # Reset bộ đếm sau khi di chuyển
        else:
            self.move_counter += 1  # Tăng bộ đếm sau mỗi khung hình

    def draw(self, screen):
        # Xác định góc quay dựa trên hướng di chuyển
        if self.dx == 1:  # Pacman đi sang phải
            rotated_image = pygame.transform.rotate(self.pacman_image, 0)
        elif self.dx == -1:  # Pacman đi sang trái
            rotated_image = pygame.transform.rotate(self.pacman_image, 180)
        elif self.dy == 1:  # Pacman đi xuống
            rotated_image = pygame.transform.rotate(self.pacman_image, 270)
        elif self.dy == -1:  # Pacman đi lên
            rotated_image = pygame.transform.rotate(self.pacman_image, 90)
        else:
            rotated_image = self.pacman_image  # Không di chuyển thì không xoay

        # Vẽ Pacman lên màn hình tại vị trí (x, y)
        screen.blit(rotated_image, (self.x * GRID_SIZE, self.y * GRID_SIZE))


# Định nghĩa lớp Ghost
class Ghost:
    def __init__(self, x, y, strategy, algorithm, image, move_delay=10):
        self.x = x
        self.y = y
        self.move_delay = move_delay  # Số khung hình phải đợi trước khi di chuyển
        self.move_counter = 0
        self.strategy = strategy
        self.algorithm = algorithm  # Thuật toán di chuyển
        self.image = image

    def move(self, target_x, target_y, maze):
        # Chỉ di chuyển khi bộ đếm đạt đến giá trị delay
        if self.move_counter >= self.move_delay:
            # Sử dụng thuật toán đã chọn để đuổi theo Pacman
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

            if path and len(path) > 1:  # Kiểm tra nếu path hợp lệ và có nhiều hơn một bước
                self.x, self.y = path[1]
            self.move_counter = 0  # Reset bộ đếm sau khi di chuyển
        else:
            self.move_counter += 1  # Tăng bộ đếm sau mỗi khung hình

    def draw(self, screen):
        screen.blit(self.image, (self.x * GRID_SIZE, self.y * GRID_SIZE))



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

# Mê cung (0 = đường đi, 1 = tường, 2 = pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

pacman = Pacman(1, 1)
#ghost = Ghost(12, 5)

blue = pygame.image.load("images/blue.png")
green = pygame.image.load("images/green.png")
red = pygame.image.load("images/red.png")
yellow = pygame.image.load("images/yellow.png")

ghosts = [
    Ghost(14, 7, 'chase', algorithm='BFS',image= blue),   # Ghost sẽ chạy theo Pacman
    Ghost(13, 8, 'random', algorithm='DFS',image= green),  # Ghost sẽ di chuyển ngẫu nhiên
    Ghost(14, 8, 'chase',algorithm='A*',image=red),   # Ghost khác cũng chạy theo
    Ghost(15, 8, 'random',algorithm='Uniform Cost',image=yellow)    # Ghost này cũng di chuyển ngẫu nhiên
]

# Vòng lặp game
running = True
clock = pygame.time.Clock()


start_button = Button(1150, 10, 200, 50, 'Reset', color=(0, 128, 255), hover_color=(70, 130, 180))
quit_button = Button(1150, 100, 200, 50, 'Stop', color=(255, 0, 0), hover_color=(255, 99, 71))

while running:
    screen.fill((0, 0, 0))

    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.dx = -1
                pacman.dy = 0
            elif event.key == pygame.K_RIGHT:
                pacman.dx = 1
                pacman.dy = 0
            elif event.key == pygame.K_UP:
                pacman.dx = 0
                pacman.dy = -1
            elif event.key == pygame.K_DOWN:
                pacman.dx = 0
                pacman.dy = 1
        if start_button.is_clicked(event):
            print("Start Game button clicked!")
        if quit_button.is_clicked(event):
            print("Quit button clicked!")
            running = False
    # Di chuyển Pacman và Ghost
    pacman.move(maze)
   # ghost.move(pacman.x, pacman.y, maze)



    # Vẽ mê cung
    draw_maze(screen, maze)
    draw_score(screen)
    # Vẽ Pacman và Ghost
    pacman.draw(screen)
   # ghost.draw(screen)
    start_button.draw(screen)
    quit_button.draw(screen)
    for ghost in ghosts:
        ghost.move(pacman.x, pacman.y, maze)
        ghost.draw(screen)

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
