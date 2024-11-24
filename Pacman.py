# Định nghĩa lớp Pacman
import pygame

SCREEN_WIDTH = 1500  # Điều chỉnh kích thước để phù hợp với kích thước lưới
SCREEN_HEIGHT = 750
GRID_SIZE = 40
pacman_image = pygame.image.load("images/pacman.png")
ghost_image = pygame.image.load("images/ghost.png")
wall_image = pygame.image.load("images/wall.png")
pellet_image = pygame.image.load("images/pellet.png")

# Chuyển đổi kích thước hình ảnh để phù hợp với GRID_SIZE
pacman_image = pygame.transform.scale(pacman_image, (GRID_SIZE, GRID_SIZE))

def update_score():
    global score
    score += 10


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
