import pygame
from collections import defaultdict

# INIT PYGAME STUFF
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Anonymous Pro for Powerline', 50) # or None if you dont have the font
pygame.display.set_caption('Sudoku Solver')

# GLOBAL VARIABLES
W = 407 # refer to test.py to get dimensions
H = 407 # added 2 pixels for 3x3 subgrid emphasis with double lines
win = pygame.display.set_mode((W, H))
cellw = W // 9
cellh = H // 9

# COLORS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (100,190,100)
BLUE = (100,100,190)

# WHITE BACKGROUND GLOBAL
background = pygame.Surface(win.get_size()).convert()
background = background.convert()
background.fill(WHITE)

# SAMPLE GAME
sudoku = '004300209005009001070060043006002087190007400050083000600000105003508690042910300'

# GAME -> original copy, used to backtrack to the previous zero value cell
game = [list(map(int, list(sudoku[i:i+9]))) for i in range(0, 9*9, 9)]
game_surface = pygame.Surface((W, H))
game_surface.blit(background, (0,0))

# SOLUTION -> copy the game at the start, but is filled with values while running,
# since cells are filled, I wont be able to track the previous zero cells,
# therefore this game copy is needed.
solution = [row[:] for row in game]
solution_surface = pygame.Surface((W,H))

def draw_bg():
    ''' paints a white background to main screen
    '''
    win.blit(background, (0,0))

def draw_grids():
    ''' paints lines, first by rows then by columns
        shows emphasis on the subgrids by doubling the line
    ''' 
    for x in range(0, 10):
        if x % 3 == 0:
            pygame.draw.line(win, GREEN, (0, x*cellh+1), (W, x*cellh+1))
        pygame.draw.line(win, GREEN, (0, x*cellh), (W, x*cellh))
    for y in range(0, 10):
        if y % 3 == 0:
            pygame.draw.line(win, GREEN, (y*cellw+1, 0), (y*cellw+1, H))    
        pygame.draw.line(win, GREEN, (y*cellw, 0), (y*cellw, H))

def clear_num(x, y, col=WHITE):
    ''' paints a white box to clear the painted number
        on x, y position
    '''
    pygame.draw.rect(solution_surface, col, (y*cellh+2, x*cellw+2, cellw-2, cellh-2))

def draw_num(num, x, y, col=BLACK, win=win):
    ''' paints a number
        on x, y position
    '''
    text = font.render(str(num), 1, col)
    textw, texth = text.get_size()
    offsety = cellw//2 - textw//2 + 2
    offsetx = cellh//2 - texth//2 + 2
    win.blit(text, (y*cellh + offsety, x*cellw + offsetx))

def draw_nums(game):
    ''' called only once
        paint the board with the game numbers excluding 0
    '''
    i, j = 0, 0
    for row in game:
        j = 0
        for num in row: 
            if num != 0: draw_num(num, i, j)
            game_surface.blit(win, (0, 0))
            pygame.display.flip()
            pygame.time.wait(20)
            j+=1
        i+=1
    solution_surface.blit(game_surface, (0,0))

def is_valid(x, y, num):
    ''' checks if the number is valid if 
        placed at x, y,
        checks: row, col, subgrid
    '''
    # row
    if solution[x].count(num) == 1: return False
    #col
    if [row[y] for row in solution].count(num) == 1: return False
    #grid
    gridx, gridy = x // 3, y // 3
    grid = [solution[x*gridx+x][y*gridy+y] for x in range(3) for y in range(3)]
    if grid.count(num) == 1: return False
    #default
    return True

def backtrack_from(x, y):
    ''' from x, y, backtrack to the previous x, y 
        where its value is 0, here the game copy is
        essential, because backtracking on a filled
        solution, we cant find 0s
    '''
    while True:
        y -= 1
        if y <= -1:
            y = 8
            x -= 1
            if x == -1:
                return 'no solution'
        if game[x][y] == 0:
            return (x, y)

def next_cell(x, y):
    ''' traverses the board by 1 cell
    '''
    y += 1
    if y == 9:
        y = 0
        x += 1
    return (x, y)

def main():
    pygame.display.flip()
    pygame.time.delay(200)
    draw_bg()
    draw_grids()
    draw_nums(game)

    x, y = 0, 0
    seen = defaultdict(list)

    # once = True
    no_solution = False
    solving = True
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False

        draw_bg()
        draw_grids()
        win.blit(solution_surface, (0,0))
        
        if no_solution: 
            print('no solution found')
            pygame.quit()
        if game[x][y] == 0:
            pass

        x, y = next_cell(x, y)
        print((x,y), game[x][y])

        pygame.display.flip()
        clock.tick(30)
    for row1,row2 in zip(game, solution):
        print(row1, row2)
    pygame.quit()


if __name__ == '__main__': main()