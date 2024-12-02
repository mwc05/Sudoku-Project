import sudoku_generator
import pygame
import copy


pygame.init()
pygame.display.set_caption('Sudoku')
screen = pygame.display.set_mode((450, 500))
pygame.font.init()
font = pygame.font.SysFont("Boulder", 30)
home_font = pygame.font.SysFont("Boulder", 60)
running = True
main_screen = True
game_over = False
game_won = False
sudoku_board = False
game_board = []
solved_board = []
reset_board = []
square_clicked = ()


# noinspection DuplicatedCode
def game_over_screen():
    screen.fill("light blue")
    screen.blit(home_font.render("Game Over!", True, pygame.Color("white")), (90, 100))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if 3 <= int(mouse_x/50) <=5 and  int(mouse_y/50) == 5:
        pygame.draw.rect(screen, pygame.Color("dark orange"), (150, 250, 150, 50))
    else:
        pygame.draw.rect(screen, pygame.Color("orange"), (150, 250, 150, 50))
    screen.blit(font.render("Restart", True, pygame.Color("white")), (190, 265))
    pygame.display.flip()


# noinspection DuplicatedCode
def game_won_screen():
    screen.fill("light blue")
    screen.blit(home_font.render("Game Won!", True, pygame.Color("white")), (100, 100))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if 3 <= int(mouse_x / 50) <= 5 and int(mouse_y / 50) == 5:
        pygame.draw.rect(screen, pygame.Color("dark orange"), (150, 250, 150, 50))
    else:
        pygame.draw.rect(screen, pygame.Color("orange"), (150, 250, 150, 50))
    screen.blit(font.render("Exit", True, pygame.Color("white")), (205, 265))
    pygame.display.flip()


def start_screen():
    screen.fill("light blue")
    screen.blit(home_font.render("Welcome to Sudoku!", True, pygame.Color("white")), (25, 100))
    screen.blit(home_font.render("Select Gamemode:", True, pygame.Color("white")), (40, 175))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.rect(screen, "orange", (75, 250, 300, 50))
    if 1.5<=round(mouse_x/50,1)<=7.5 and int(mouse_y/50) == 5:
        pygame.draw.rect(screen, pygame.Color("dark orange"),(max(i for i in [1.5,3.5,5.5] if i <= round(mouse_x/50,1))*50, int(mouse_y/50)*50, 100, 50))
    pygame.draw.line(screen, pygame.Color("black"), (75, 250), (375, 250), 5)
    pygame.draw.line(screen, pygame.Color("black"), (75, 300), (375, 300), 5)
    pygame.draw.line(screen, pygame.Color("black"), (75, 250), (75, 300), 5)
    pygame.draw.line(screen, pygame.Color("black"), (175, 250), (175, 300), 5)
    pygame.draw.line(screen, pygame.Color("black"), (275, 250), (275, 300), 5)
    pygame.draw.line(screen, pygame.Color("black"), (375, 250), (375, 300), 5)
    screen.blit(font.render("Easy", True, pygame.Color("white")), (100, 265))
    screen.blit(font.render("Medium", True, pygame.Color("white")), (190, 265))
    screen.blit(font.render("Hard", True, pygame.Color("white")), (300, 265))
    pygame.display.flip()


def board_screen(board):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.fill("light blue")
    if not square_clicked:
        if int(mouse_y/50) < 9:
            pygame.draw.rect(screen, "lightblue3", (int(mouse_x/50)*50, int(mouse_y/50)*50, 50, 50))
    else:
        pygame.draw.rect(screen, "lightblue3", (square_clicked[0]*50, square_clicked[1]*50, 50, 50))
    for i in range(9,0,-1):
        pygame.draw.line(screen, "gray50", (i*50, 0), (i*50, 450))
    for i in range(9,0,-1):
        pygame.draw.line(screen, "gray50", (0, i*50), (450, i*50))
    for i in range(0, 3):
        if (int(mouse_x/150), int(mouse_y/50)) == (i, 9):
            pygame.draw.rect(screen, "dark orange", (i*150, 450, 150, 50))
        else:
            pygame.draw.rect(screen, "orange", (i*150, 450, 150, 50))
    for i in range(3,0,-1):
        pygame.draw.line(screen, "black", (i*150, 0), (i*150, 500))
    for i in range(3,0,-1):
        pygame.draw.line(screen, "black", (0, i*150), (450, i*150))
    for i in range(9):
        for x in range(9):
            if str(board.board[i][x]) != "0":
                if str(reset_board.board[i][x]) != "0":
                    screen.blit(font.render(str(board.board[i][x]), True, pygame.Color("black")), (i*50+20, x*50+18))
                else:
                    screen.blit(font.render(str(board.board[i][x]), True, pygame.Color("gray40")), (i*50+20, x*50+18))
    screen.blit(font.render("Reset", True, pygame.Color("white")), (50, 465))
    screen.blit(font.render("Restart", True, pygame.Color("white")), (190, 465))
    screen.blit(font.render("Exit", True, pygame.Color("white")), (355, 465))
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # global running # very useful for changing variables later
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.name(event.key) == "return":
                square_clicked = ()
            elif square_clicked and reset_board.board[square_clicked[0]][square_clicked[1]]==0:
                if pygame.key.name(event.key) in ["1","2","3","4","5","6","7","8","9"]:
                    game_board.board[square_clicked[0]][square_clicked[1]] = int(pygame.key.name(event.key))
                elif pygame.key.name(event.key) == "backspace":
                    game_board.board[square_clicked[0]][square_clicked[1]] = 0
            if square_clicked and pygame.key.name(event.key) in ["up","down","left","right"]:
                if pygame.key.name(event.key) == "down" and square_clicked[1] < 8:
                    square_clicked = (square_clicked[0], square_clicked[1]+1)
                elif pygame.key.name(event.key) == "left" and square_clicked[0] > 0:
                    square_clicked = (square_clicked[0]-1, square_clicked[1])
                elif pygame.key.name(event.key) == "right" and square_clicked[0] < 8:
                    square_clicked = (square_clicked[0]+1, square_clicked[1])
                elif pygame.key.name(event.key) == "up" and square_clicked[1] > 0:
                    square_clicked = (square_clicked[0], square_clicked[1]-1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if sudoku_board:
                if (int(event.pos[0]/150), int(event.pos[1]/50)) == (0, 9):
                    game_board = copy.deepcopy(reset_board)
                elif (int(event.pos[0]/150), int(event.pos[1]/50)) == (1,9):
                    square_clicked = ()
                    game_board = []
                    solved_board = []
                    sudoku_board = False
                    main_screen = True
                elif (int(event.pos[0]/150), int(event.pos[1]/50)) == (2,9):
                    running = False
                else:
                    if square_clicked == (int(event.pos[0]/50), int(event.pos[1]/50)):
                        square_clicked = ()
                    else:
                        square_clicked = (int(event.pos[0]/50), int(event.pos[1]/50))
            if main_screen:
                if 1.5 <= round(event.pos[0]/50, 1) <= 3.5 and int(event.pos[1]/50) == 5:
                    main_screen = False
                    sudoku_board = True
                    game_board = sudoku_generator.SudokuGenerator(9, 30)
                    game_board.fill_values()
                    solved_board = copy.deepcopy(game_board.get_board())
                    game_board.remove_cells()
                    reset_board = copy.deepcopy(game_board)
                elif 3.5 <= round(event.pos[0]/50, 1) <= 5.5 and int(event.pos[1]/50) == 5:
                    main_screen = False
                    sudoku_board = True
                    game_board = sudoku_generator.SudokuGenerator(9, 40)
                    game_board.fill_values()
                    solved_board = copy.deepcopy(game_board.get_board())
                    game_board.remove_cells()
                    reset_board = copy.deepcopy(game_board)
                elif 5.5 <= round(event.pos[0]/50, 1) <= 7.5 and int(event.pos[1]/50) == 5:
                    main_screen = False
                    sudoku_board = True
                    game_board = sudoku_generator.SudokuGenerator(9, 50)
                    game_board.fill_values()
                    solved_board = copy.deepcopy(game_board.get_board())
                    game_board.remove_cells()
                    reset_board = copy.deepcopy(game_board)
            if game_over:
                if 3 <= int(event.pos[0]/50) <=5 and  int(event.pos[1]/50) == 5:
                    game_over = False
                    main_screen = True
            if game_won:
                if 3 <= int(event.pos[0]/50) <=5 and  int(event.pos[1]/50) == 5:
                    running = False
    if main_screen:
        start_screen()
    if sudoku_board:
        board_screen(game_board)
        if game_board.board == solved_board:
            sudoku_board = False
            game_won = True
        elif not any(0 in i for i in game_board.board):
            sudoku_board = False
            game_over = True
    if game_won:
        game_won_screen()
    if game_over:
        game_over_screen()
pygame.quit()
