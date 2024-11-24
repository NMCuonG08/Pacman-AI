import pygame
SCREEN_WIDTH=1500
SCREEN_HEIGHT=750

def draw_info_panel(screen, avatar_path):
    avatar_size = 300
    padding = 50  # Khoảng cách từ cạnh màn hình
    avatar_x = SCREEN_WIDTH - avatar_size - padding
    avatar_y = SCREEN_HEIGHT - avatar_size - padding

    # Kiểm tra nếu có đường dẫn ảnh
    if avatar_path:
        try:
            avatar = pygame.image.load(avatar_path)
            avatar = pygame.transform.scale(avatar, (avatar_size, avatar_size))
            screen.blit(avatar, (avatar_x, avatar_y))
        except pygame.error:
            print(f"Không thể tải ảnh: {avatar_path}")
            pygame.draw.rect(screen, (50, 50, 50), (avatar_x, avatar_y, avatar_size, avatar_size))
            font = pygame.font.Font(None, 24)
            text = font.render("No Image", True, (255, 255, 255))
            screen.blit(text, (avatar_x + 10, avatar_y + avatar_size // 3))
    else:
        # Hiển thị ô trống nếu không có ảnh
        pygame.draw.rect(screen, (50, 50, 50), (avatar_x, avatar_y, avatar_size, avatar_size))
        font = pygame.font.Font(None, 24)
        text = font.render("No Image", True, (255, 255, 255))
        screen.blit(text, (avatar_x + 10, avatar_y + avatar_size // 3))
