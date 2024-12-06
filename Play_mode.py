import pygame
import sys
import subprocess
import os
from Draw_Button import Button

# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chọn Chế Độ Chơi"

# Màu sắc
BUTTON_COLOR = (0, 0, 0)          # Màu đen cho nút
BUTTON_HOVER_COLOR = (0, 255, 0)    # Màu xanh lá khi hover
TEXT_COLOR = (0, 0, 0)        # Màu đen cho chữ
BORDER_COLOR = (0, 0, 0)            # Màu đen cho viền
BACKGROUND_COLOR = (0, 0, 0)  # Màu trắng cho nền

# Cài đặt font chữ
FONT = pygame.font.SysFont('Arial', 24, bold=True)

class PlayModeView:
    def __init__(self, screen):
        self.screen = screen
        self.button_list = []

        # Tạo các nút bấm với text và vị trí
        # Chú ý: position là một tuple (x, y), text là tên nút
        self.button_list.append(Button("Play Pacman and Ghost AI", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), text="Play Pacman and Ghost AI"))
        self.button_list.append(Button("Play Pacman AI mode", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50), text="Play Pacman AI mode"))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for button in self.button_list:
            button.draw(self.screen)  # Vẽ nút lên màn hình
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Nhấn chuột trái
                pos = event.pos
                for button in self.button_list:
                    if button.is_clicked(event):  # Kiểm tra nếu nút bị nhấn
                        if button.name == "Play Pacman and Ghost AI":
                            self.play_mode_1()
                        elif button.name == "Play Pacman AI mode":
                            self.play_mode_2()
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for button in self.button_list:
                # Lấy vị trí con trỏ chuột và kiểm tra xem có hover trên nút hay không
                if button.rect.collidepoint(pos):
                    button.image = button.hover_image
                else:
                    button.image = button.image

    def play_mode_1(self):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Main.py')
        subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))

    def play_mode_2(self):
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Pacman-AI.py')
        subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)
    play_mode_view = PlayModeView(screen)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            play_mode_view.handle_event(event)

        play_mode_view.draw()
        clock.tick(60)  # Giới hạn 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
