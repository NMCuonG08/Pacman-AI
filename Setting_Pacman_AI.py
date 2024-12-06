import pygame
import random
from collections import deque
import sys
from Draw_Button import Button
from Algorithms import bfs, dfs, a_star, greedy_search, uniform_cost_search, hill_climbing, genetic_algorithm, beam_search, simulated_annealing
from Setting import draw_settings_panel, handle_dropdown_events, init_dropdown_states
from Panel import draw_info_panel

pygame.init()

# Kích thước màn hình
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
GRID_SIZE = 40  # Kích thước ô lưới
game_started = False

# Thiết lập màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pacman AI")
is_settings_open = False

# Tải hình ảnh
pacman_image = pygame.image.load("images/pacman.png")
wall_image = pygame.image.load("images/wall.png")
pellet_image = pygame.image.load("images/pellet.png")

# Chuyển đổi kích thước hình ảnh để phù hợp với GRID_SIZE
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))
wall_image = pygame.transform.scale(wall_image, (GRID_SIZE, GRID_SIZE))
pellet_image = pygame.transform.scale(pellet_image, (GRID_SIZE // 2, GRID_SIZE // 2))

score = 0

# Hàm cập nhật điểm số
def update_score(points=10):
    global score
    score += points


class Pacman:
    def __init__(self, x, y, move_delay=0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.move_delay = move_delay  # Số khung hình phải đợi trước khi di chuyển
        self.move_counter = 0  # Bộ đếm để kiểm soát tốc độ di chuyển
        self.pacman_image = pacman_image
        self.is_hunting = False  # Biến để theo dõi chế độ săn
        self.hunting_time = 0

    def update_direction(self, dx, dy):
        """ Cập nhật hướng đi theo phím bấm """
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


# Hàm vẽ bảng Settings với một dropdown cho Pacman
def draw_settings_panel(screen, pacman, dropdown_state):
    """Vẽ bảng Settings với tùy chọn thuật toán cho Pacman"""
    panel_width = 400
    panel_height = 300
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = (SCREEN_HEIGHT - panel_height) // 2

    # Tạo bảng settings
    pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, (200, 200, 200), (panel_x, panel_y, panel_width, panel_height), 5)

    # Tiêu đề
    font = pygame.font.Font(None, 36)
    text = font.render("Settings", True, (255, 255, 255))
    screen.blit(text, (panel_x + panel_width // 2 - text.get_width() // 2, panel_y + 20))

    # Vẽ dropdown cho Pacman
    dropdown_rect, dropdown_options = draw_algorithm_dropdown(
        screen, panel_x + 50, panel_y + 80, pacman.algorithm, dropdown_state
    )

    # Nút "Close" để đóng bảng Settings
    close_button = pygame.Rect(panel_x + panel_width - 100, panel_y + panel_height - 50, 80, 30)
    pygame.draw.rect(screen, (200, 50, 50), close_button)
    text_close = font.render("Close", True, (255, 255, 255))
    screen.blit(text_close, (close_button.x + 10, close_button.y + 5))

    return [dropdown_rect], [dropdown_options], close_button  # Trả về danh sách đúng dạng



def draw_algorithm_dropdown(screen, x, y, current_algorithm, is_open):
    font = pygame.font.Font(None, 24)
    options = ["A*", "BFS", "Uniform Cost", "Greedy", "Hill Climbing", "Simulated Annealing", "Genetic Algorithm"]
    dropdown_width, dropdown_height = 200, 30

    # Vẽ ô dropdown chính
    dropdown_rect = pygame.Rect(x, y, dropdown_width, dropdown_height)
    pygame.draw.rect(screen, (100, 100, 100), dropdown_rect)
    pygame.draw.rect(screen, (200, 200, 200), dropdown_rect, 2)

    text = font.render(current_algorithm, True, (255, 255, 255))
    screen.blit(text, (dropdown_rect.x + 10, dropdown_rect.y + 5))

    dropdown_options = []
    if is_open:  # Hiển thị danh sách tùy chọn khi mở
        for i, option in enumerate(options):
            option_rect = pygame.Rect(x, y + (i + 1) * dropdown_height, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (50, 50, 50), option_rect)
            pygame.draw.rect(screen, (200, 200, 200), option_rect, 1)
            dropdown_options.append((option, option_rect))

            text_option = font.render(option, True, (255, 255, 255))
            screen.blit(text_option, (option_rect.x + 10, option_rect.y + 5))

    return dropdown_rect, dropdown_options

def handle_dropdown_events(event, dropdown_rects, dropdown_options_list, pacman, dropdown_state):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        for i, dropdown_rect in enumerate(dropdown_rects):
            # Nếu nhấn vào dropdown, mở/đóng nó
            if dropdown_rect.collidepoint(mouse_pos):
                dropdown_state[i] = not dropdown_state[i]

            # Nếu dropdown đang mở, kiểm tra nhấn vào tùy chọn
            if dropdown_state[i]:
                for option, option_rect in dropdown_options_list[i]:
                    if option_rect.collidepoint(mouse_pos):
                        pacman.algorithm = option  # Cập nhật thuật toán
                        dropdown_state[i] = False  # Đóng dropdown sau khi chọn

    return dropdown_state