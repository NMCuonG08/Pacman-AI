import pygame
SCREEN_WIDTH=1500
SCREEN_HEIGHT=750

def draw_info_panel(screen):
    rect = pygame.Rect(1300, 500,50,10)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("List of members", True, (255, 255, 0))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
    rect2 = pygame.Rect(1300, 530, 50, 10)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Nguyen Hai Trieu", True, (255, 255, 0))
    text_rect = text_surface.get_rect(center=rect2.center)
    screen.blit(text_surface, text_rect)
    rect3 = pygame.Rect(1300, 560, 50, 10)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Le Cong Bao", True, (255, 255, 0))
    text_rect = text_surface.get_rect(center=rect3.center)
    screen.blit(text_surface, text_rect)
    rect4 = pygame.Rect(1300, 590, 50, 10)
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Nguyen Manh Cuong", True, (255, 255, 0))
    text_rect = text_surface.get_rect(center=rect4.center)
    screen.blit(text_surface, text_rect)