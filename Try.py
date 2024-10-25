import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ và các màu
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Khởi tạo cửa sổ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game ăn quả")


# Lớp Pacman
class Pacman:
    def __init__(self, x, y):
        self.position = [x, y]  # Vị trí Pacman

    def move(self, dx, dy):
        self.position[0] += dx
        self.position[1] += dy

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (*self.position, GRID_SIZE, GRID_SIZE))


# Lớp Pellet
class Pellet:
    def __init__(self):
        self.position = self.create_pellet()

    def create_pellet(self):
        x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        return [x, y]

    def reset(self):
        self.position = self.create_pellet()

    def draw(self):
        pygame.draw.rect(screen, RED, (*self.position, GRID_SIZE, GRID_SIZE))


# Lớp Game
class Game:
    def __init__(self):
        self.pacman = Pacman(180, 180)  # Tạo đối tượng Pacman
        self.pellet = Pellet()  # Tạo đối tượng Pellet
        self.score = 0
        self.game_active = True

    def move_pacman(self, dx, dy):
        if not self.game_active:
            return

        # Cập nhật vị trí Pacman
        self.pacman.move(dx, dy)

        # Kiểm tra va chạm với pellet
        if self.check_collision():
            self.score += 1
            self.pellet.reset()  # Reset pellet khi Pacman ăn

    def check_collision(self):
        return (self.pacman.position[0] == self.pellet.position[0] and
                self.pacman.position[1] == self.pellet.position[1])

    def draw(self):
        screen.fill(BLACK)
        # Vẽ Pacman
        self.pacman.draw()
        # Vẽ pellet
        self.pellet.draw()
        # Hiển thị điểm số
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Điểm: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def reset(self):
        self.pacman.position = [180, 180]
        self.pellet.reset()
        self.score = 0
        self.game_active = True


# Hàm chính
def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.move_pacman(0, -GRID_SIZE)
        elif keys[pygame.K_DOWN]:
            game.move_pacman(0, GRID_SIZE)
        elif keys[pygame.K_LEFT]:
            game.move_pacman(-GRID_SIZE, 0)
        elif keys[pygame.K_RIGHT]:
            game.move_pacman(GRID_SIZE, 0)

        game.draw()
        clock.tick(10)


if __name__ == "__main__":
    main()
