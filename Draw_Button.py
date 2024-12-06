import pygame
import pygame.sprite
import os
import json


basedir = os.path.dirname(__file__)
images = {}
class Button(pygame.sprite.Sprite):
    BUTTON_IMAGE = "button"
    BUTTON_HOVER_IMAGE = "button-hover"
    BUTTON_TEXT_SIZE = 25
    BUTTON_TEXT_COLOR = (0, 0, 0)
    BUTTON_CHECK_TIME = 200
    def __init__(self, name, position,text='',text_color=(0, 255, 220),font_size=30):
        super().__init__()
        self.name = name
        self.position = position
        self.image = pygame.image.load(os.path.join(basedir, "./images/button.png")).convert_alpha()
        self.hover_image = pygame.image.load(os.path.join(basedir, "./images/button-hover.png")).convert_alpha()
        self.text_color = text_color
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self._current_image = self.image
        self.rect = self._current_image.get_rect(center=self.position)

    # Hàm vẽ button
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self._current_image = self.hover_image
        else:
            self._current_image = self.image


        text_position = (self.position[0], self.position[1] - 2)
        screen.blit(self._current_image, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # Kiểm tra nếu button được click
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            if self.rect.collidepoint(event.pos):
                return True
        return False