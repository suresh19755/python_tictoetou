import pygame
import sys

# Initialize Pygame
pygame.init()

# --- Screen setup ---
screen = pygame.display.set_mode((600, 700))
pygame.display.set_caption("X O game")

# --- Colors ---
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

size = 200

# --- Fonts ---
font = pygame.font.Font(None, 100)
btn_font = pygame.font.Font(None, 50)

# --- Global Variables ---
board = [["", "", ""],
         ["", "", ""],
         ["", "", ""]]
player = "X"
game_active = False
winner_message = ""

# --- Functions ---

def reset_game():
    global board, player, winner_message
    board = [["", "", ""],
             ["", "", ""],
             ["", "", ""]]
    player = "X"
    winner_message = ""

def check_winner():
    # Check Rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != "":
            y_pos = row * 200 + 100
            return board[row][0], (0, y_pos), (600, y_pos)

    # Check Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            x_pos = col * 200 + 100
            return board[0][col], (x_pos, 0), (x_pos, 600)

    # Check Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0], (0, 0), (600, 600)
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2], (600, 0), (0, 600)

    return None

def draw_grid():
    # Vertical lines
    pygame.draw.line(screen, BLACK, (200, 0), (200, 600), 5)
    pygame.draw.line(screen, BLACK, (400, 0), (400, 600), 5)
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, 200), (600, 200), 5)
    pygame.draw.line(screen, BLACK, (0, 400), (600, 400), 5)
    # Bottom border
    pygame.draw.line(screen, BLACK, (0, 600), (600, 600), 5)

def draw_pieces():
    for row in range(3):
        for col in range(3):
            if board[row][col] != "":
                text = font.render(board[row][col], True, BLACK)
                # FIX IS HERE: Ensure integers and correct parenthesis placement
                x_pos = int(col * size + 70)
                y_pos = int(row * size + 50)
                screen.blit(text, (x_pos, y_pos))

def animate_line(start_pos, end_pos):
    x1, y1 = start_pos
    x2, y2 = end_pos
    steps = 50
    dx = (x2 - x1) / steps
    dy = (y2 - y1) / steps
    
    for i in range(steps + 1):
        current_x = x1 + dx * i
        current_y = y1 + dy * i
        pygame.draw.line(screen, BLACK, (x1, y1), (current_x, current_y), 10)
        pygame.display.update()
        pygame.time.delay(10)

# --- Main Game Loop ---

start_btn_rect = pygame.Rect(200, 300, 200, 80)
end_btn_rect = pygame.Rect(200, 620, 200, 60)

run = True
while run:
    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if not game_active:
                if start_btn_rect.collidepoint(mouse_pos):
                    reset_game()
                    game_active = True
            else:
                if end_btn_rect.collidepoint(mouse_pos):
                    game_active = False
                elif mouse_pos[1] < 600:
                    col = mouse_pos[0] // 200
                    row = mouse_pos[1] // 200
                    if row < 3 and col < 3 and board[row][col] == "":
                        board[row][col] = player
                        
                        # Update screen immediately to show piece
                        screen.fill(GREEN)
                        draw_grid()
                        draw_pieces()
                        pygame.draw.rect(screen, RED, end_btn_rect)
                        end_text = btn_font.render("END GAME", True, WHITE)
                        text_rect = end_text.get_rect(center=end_btn_rect.center)
                        screen.blit(end_text, text_rect)
                        pygame.display.update()
                        
                        result = check_winner()
                        if result:
                            winner, start_pos, end_pos = result
                            animate_line(start_pos, end_pos)
                            pygame.time.delay(1000)
                            winner_message = winner + " WINS!"
                            game_active = False
                        else:
                            player = "O" if player == "X" else "X"

    if not game_active:
        # Start Screen
        pygame.draw.rect(screen, BLUE, start_btn_rect)
        start_text = btn_font.render("START", True, WHITE)
        text_rect = start_text.get_rect(center=start_btn_rect.center)
        screen.blit(start_text, text_rect)
        
        if winner_message != "":
            msg_text = font.render(winner_message, True, BLACK)
            screen.blit(msg_text, (150, 100))
        else:
            title_text = font.render("TIC TAC TOE", True, BLACK)
            screen.blit(title_text, (80, 100))
    else:
        # Game Active Screen
        draw_grid()
        draw_pieces()
        pygame.draw.rect(screen, RED, end_btn_rect)
        end_text = btn_font.render("END GAME", True, WHITE)
        text_rect = end_text.get_rect(center=end_btn_rect.center)
        screen.blit(end_text, text_rect)

    pygame.display.update()

pygame.quit()
sys.exit()