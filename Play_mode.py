import pygame
import sys
import subprocess
import sys
import os
# Khởi tạo pygame
pygame.init()

# Kích thước cửa sổ
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chọn Chế Độ Chơi"

# Màu sắc
BUTTON_COLOR = (0, 0, 255)          # Màu xanh dương
BUTTON_HOVER_COLOR = (0, 255, 0)    # Màu xanh lá khi hover
TEXT_COLOR = (255, 255, 255)        # Màu trắng cho chữ
BORDER_COLOR = (0, 0, 0)            # Màu đen cho viền
BACKGROUND_COLOR = (255, 255, 255)  # Màu trắng cho nền

# Cài đặt font chữ
FONT = pygame.font.SysFont('Arial', 24, bold=True)

class Button:
    def __init__(self, text, center_x, center_y, width, height, action_function):
        self.text = text
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.border_color = BORDER_COLOR
        self.border_width = 3
        self.current_color = self.color
        self.action_function = action_function
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.center_x, self.center_y)
        self.text_surf = FONT.render(self.text, True, TEXT_COLOR)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        # Vẽ hình chữ nhật với màu nền và bo góc
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        # Vẽ viền cho nút
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=10)
        # Vẽ văn bản lên nút
        screen.blit(self.text_surf, self.text_rect)

    def check_mouse_press(self, pos):
        if self.rect.collidepoint(pos):
            self.action_function()

    def check_mouse_hover(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

class PlayModeView:
    def __init__(self, screen):
        self.screen = screen
        self.button_list = []

        # Tạo nút
        self.button_list.append(Button("Play Pacman and Ghost AI", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, 250, 60, self.play_mode_1))
        self.button_list.append(Button("Play Pacman AI mode ", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, 250, 60, self.play_mode_2))

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        for button in self.button_list:
            button.draw(self.screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Nhấn chuột trái
                pos = event.pos
                for button in self.button_list:
                    button.check_mouse_press(pos)
        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for button in self.button_list:
                button.check_mouse_hover(pos)

    
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