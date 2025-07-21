import pygame
import sys
import random

pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tic Tac Toe")

# Colors
BG_COLOR = (30, 30, 30)
LINE_COLOR = (200, 200, 200)
X_COLOR = (255, 100, 100)
O_COLOR = (100, 150, 255)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (255, 140, 0)

# Load Custom Font
custom_font_path = "c:\\USERS\\GAMIN\\APPDATA\\LOCAL\\MICROSOFT\\WINDOWS\\FONTS\\TT ROUNDS NEUE TRIAL CONDENSED BLACK.TTF"  # Replace with your font path
font_large = pygame.font.Font(custom_font_path, 80)
font_medium = pygame.font.Font(custom_font_path, 50)
font_small = pygame.font.Font(custom_font_path, 40)

# Board & game variables
board = [" "] * 9
current_player = "X"
game_mode = None  # 'PLAYER' or 'BOT'
game_over = False

# Functions
def draw_grid():
    screen.fill(BG_COLOR)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (screen_width/2 -50, screen_height/2 -150), (screen_width/2 -50, screen_height/2 +150 ), 10)
    pygame.draw.line(screen, LINE_COLOR, (screen_width/2 +50, screen_height/2 -150), (screen_width/2 +50, screen_height/2 +150 ), 10)
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (screen_width/2 -150, screen_height/2 -50), (screen_width/2 +150, screen_height/2 -50 ), 10)
    pygame.draw.line(screen, LINE_COLOR, (screen_width/2 -150, screen_height/2 +50), (screen_width/2 +150, screen_height/2 +50 ), 10)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 -49, screen_height/2 -150), 10 / 2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 -49, screen_height/2 +150 ), 10 / 2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 +51, screen_height/2 +150 ), 10/2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 +150, screen_height/2 -49 ), 10/2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 -150, screen_height/2 +51),  10/2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 +51, screen_height/2 -150), 10/2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 -150, screen_height/2 -49),  10/2)
    pygame.draw.circle(screen, LINE_COLOR, (screen_width/2 +150, screen_height/2 +51), 10/2)

def draw_marks():
    for idx, mark in enumerate(board):
        x = (idx % 3) * 133 + 66
        y = (idx // 3) * 133 + 166
        if mark == "X":
            text = font_large.render("X", True, X_COLOR)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        elif mark == "O":
            text = font_large.render("O", True, O_COLOR)
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)

def check_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if all(board[pos] == player for pos in condition):
            return True
    return False

def is_draw():
    return all(cell != " " for cell in board)

def show_winner(text):
    winner_text = font_medium.render(text, True, (255, 255, 255))
    rect = winner_text.get_rect(center=(screen_width // 2, 70))
    screen.blit(winner_text, rect)
    pygame.display.update()
    pygame.time.wait(2000)

def bot_move():
    empty_cells = [i for i, v in enumerate(board) if v == " "]
    if empty_cells:
        choice = random.choice(empty_cells)
        board[choice] = "O"

def draw_menu():
    screen.fill(BG_COLOR)
    title = font_medium.render("Tic Tac Toe", True, (255, 255, 255))
    title_rect = title.get_rect(center=(screen_width // 2, 100))
    screen.blit(title, title_rect)

    buttons = [
        {"rect": pygame.Rect(100, 180, 200, 60), "text": "VS Player"},
        {"rect": pygame.Rect(100, 260, 200, 60), "text": "VS Computer"}
    ]

    mouse_pos = pygame.mouse.get_pos()

    for btn in buttons:
        color = BUTTON_HOVER if btn["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color, btn["rect"], border_radius=10)
        text = font_small.render(btn["text"], True, (255, 255, 255))
        text_rect = text.get_rect(center=btn["rect"].center)
        screen.blit(text, text_rect)

    pygame.display.update()
    return buttons

# Game Loop
menu_active = True
running = True

while running:
    if menu_active:
        buttons = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        game_mode = "PLAYER" if btn["text"] == "VS Player" else "BOT"
                        board = [" "] * 9
                        current_player = "X"
                        game_over = False
                        menu_active = False

    else:
        draw_grid()
        draw_marks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                if my < 100:
                    continue  # Ignore clicks above the board
                row = (my - 100) // 133
                col = mx // 133
                idx = row * 3 + col

                if board[idx] == " ":
                    board[idx] = current_player
                    if check_winner(current_player):
                        draw_grid()
                        draw_marks()
                        show_winner(f"Player {current_player} Wins!")
                        game_over = True
                    elif is_draw():
                        draw_grid()
                        draw_marks()
                        show_winner("It's a Draw!")
                        game_over = True
                    else:
                        current_player = "O" if current_player == "X" else "X"

        if not game_over and game_mode == "BOT" and current_player == "O":
            pygame.time.wait(500)
            bot_move()
            if check_winner("O"):
                draw_grid()
                draw_marks()
                show_winner("Computer Wins!")
                game_over = True
            elif is_draw():
                draw_grid()
                draw_marks()
                show_winner("It's a Draw!")
                game_over = True
            else:
                current_player = "X"

        if game_over:
            pygame.time.wait(1500)
            menu_active = True

    pygame.display.update()
