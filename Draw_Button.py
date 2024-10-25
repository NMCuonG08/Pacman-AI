import pygame

class Button:
    def __init__(self, x, y, width, height, text='', color=(0, 0, 0), hover_color=(100, 100, 100), text_color=(255, 255, 255), font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)

    # Hàm vẽ button
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # Viền button

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # Kiểm tra nếu button được click
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False
