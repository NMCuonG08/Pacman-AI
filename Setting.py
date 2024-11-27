import pygame

# Biến điều khiển hiển thị bảng settings


SCREEN_WIDTH=1500
SCREEN_HEIGHT=750

def init_dropdown_states(ghosts):
    return [False] * len(ghosts)


def draw_settings_panel(screen, ghosts, dropdown_states):
    """Vẽ bảng Settings với tùy chọn thuật toán cho mỗi ghost"""
    panel_width = SCREEN_WIDTH
    panel_height = SCREEN_HEIGHT
    panel_x = (SCREEN_WIDTH - panel_width)
    panel_y = (SCREEN_HEIGHT - panel_height)

    # Tạo bảng settings
    pygame.draw.rect(screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(screen, (200, 200, 200), (panel_x, panel_y, panel_width, panel_height), 5)

    # Tiêu đề
    font = pygame.font.Font(None, 36)
    text = font.render("Settings", True, (255, 255, 255))
    screen.blit(text, (panel_x + panel_width // 2 - text.get_width() // 2, panel_y + 20))

    # Hiển thị dropdown và ảnh của từng ghost
    dropdown_rects = []
    dropdown_options_list = []
    for i, ghost in enumerate(ghosts):
        # Vị trí vẽ mỗi ghost và dropdown
        ghost_x = panel_x + 50
        ghost_y = panel_y + 80 + i * 100

        # Vẽ hình ảnh ghost
        screen.blit(ghost.image, (ghost_x, ghost_y))

        # Vẽ dropdown cho ghost
        dropdown_rect, dropdown_options = draw_algorithm_dropdown(
            screen, ghost_x + 100, ghost_y, ghost.algorithm, dropdown_states[i]
        )
        dropdown_rects.append(dropdown_rect)
        dropdown_options_list.append(dropdown_options)

    # Nút "Close"
    close_button = pygame.Rect(panel_x + panel_width - 100, panel_y + panel_height - 50, 80, 30)
    pygame.draw.rect(screen, (200, 50, 50), close_button)
    text_close = font.render("Close", True, (255, 255, 255))
    screen.blit(text_close, (close_button.x + 10, close_button.y + 5))

    return dropdown_rects, dropdown_options_list, close_button

# Biến trạng thái dropdown
is_dropdown_open = [False]  # Một danh sách trạng thái cho các dropdown

def draw_algorithm_dropdown(screen, x, y, current_algorithm, is_open):
    """Vẽ menu lựa chọn thuật toán"""
    font = pygame.font.Font(None, 24)
    options = ["A*", "BFS",'Uniform Cost', 'Greedy','Hill Climbing','Simulated Annealing','Genetic Algorithm']
    dropdown_width, dropdown_height = 200, 30

    # Vẽ menu hiện tại
    dropdown_rect = pygame.Rect(x, y, dropdown_width, dropdown_height)
    pygame.draw.rect(screen, (100, 100, 100), dropdown_rect)
    pygame.draw.rect(screen, (200, 200, 200), dropdown_rect, 2)

    text = font.render(current_algorithm, True, (255, 255, 255))
    screen.blit(text, (dropdown_rect.x + 10, dropdown_rect.y + 5))

    dropdown_options = []
    if is_open:  # Chỉ hiển thị danh sách khi dropdown mở
        for i, option in enumerate(options):
            # Tọa độ các tùy chọn được thay đổi để hiển thị ngang
            option_x = x + dropdown_width  # Dịch ngang sang phải
            option_y = y + i * dropdown_height

            option_rect = pygame.Rect(option_x, option_y, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, (50, 50, 50), option_rect)
            pygame.draw.rect(screen, (200, 200, 200), option_rect, 1)
            dropdown_options.append((option, option_rect))

            text_option = font.render(option, True, (255, 255, 255))
            screen.blit(text_option, (option_rect.x + 10, option_rect.y + 5))

    return dropdown_rect, dropdown_options



def handle_dropdown_events(event, dropdown_rects, dropdown_options_list, ghosts, dropdown_states):
    """Xử lý sự kiện chuột cho dropdown"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()

        for i, dropdown_rect in enumerate(dropdown_rects):
            # Kiểm tra nếu dropdown được nhấn
            if dropdown_rect.collidepoint(mouse_pos):
                # Đóng tất cả các dropdown khác, chỉ mở dropdown hiện tại
                for j in range(len(dropdown_states)):
                    dropdown_states[j] = (i == j)

            # Nếu dropdown đang mở, kiểm tra các mục
            elif dropdown_states[i]:
                for option, option_rect in dropdown_options_list[i]:
                    if option_rect.collidepoint(mouse_pos):
                        # Cập nhật thuật toán cho ghost tương ứng
                        ghosts[i].algorithm = option
                        dropdown_states[i] = False