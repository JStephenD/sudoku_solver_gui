import pygame
from collections import defaultdict

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Anonymous Pro for Powerline', 50)

W = 407
H = 407
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Sudoku Solver')
cellw = W // 9
cellh = H // 9

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (100,190,100)
BLUE = (100,100,190)

background = pygame.Surface(win.get_size()).convert()
background = background.convert()
background.fill(WHITE)

sudoku = '004300209005009001070060043006002087190007400050083000600000105003508690042910300'

game = [list(map(int, list(sudoku[i:i+9]))) for i in range(0, 9*9, 9)]
game_surface = pygame.Surface((W, H))
game_surface.blit(background, (0,0))

solution = [row[:] for row in game]
solution_surface = pygame.Surface((W,H))

def draw_bg():
    win.blit(background, (0,0))

def draw_grids():
    for x in range(0, 10):
        if x % 3 == 0:
            pygame.draw.line(win, GREEN, (0, x*cellh+1), (W, x*cellh+1))
        pygame.draw.line(win, GREEN, (0, x*cellh), (W, x*cellh))
    for y in range(0, 10):
        if y % 3 == 0:
            pygame.draw.line(win, GREEN, (y*cellw+1, 0), (y*cellw+1, H))    
        pygame.draw.line(win, GREEN, (y*cellw, 0), (y*cellw, H))

def clear_num(x, y, col=WHITE):
    pygame.draw.rect(solution_surface, col, (y*cellh+2, x*cellw+2, cellw-2, cellh-2))

def draw_num(num, x, y, col=BLACK, win=win):
    text = font.render(str(num), 1, col)
    textw, texth = text.get_size()
    offsety = cellw//2 - textw//2 + 2
    offsetx = cellh//2 - texth//2 + 2
    win.blit(text, (y*cellh + offsety, x*cellw + offsetx))

def draw_nums(game):
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
    while True:
        y -= 1
        if y <= -1:
            y = 8
            x -= 1
            if x == -1:
                return 'no solution'
        if game[x][y] == 0:
            return (x, y)

def next_cell():
    for x in range(9):
        for y in range(9):
            if solution[x][y] == 0:
                return (x,y)
    return (-1,-1)

def main():
    pygame.display.flip()
    pygame.time.delay(200)
    draw_bg()
    draw_grids()
    draw_nums(game)

    x, y = 0, 0
    temp = defaultdict(list)

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
        while solving:
            if game[x][y] == 0:
                num = None
                for possible in range(1,10):
                    if is_valid(x, y, possible):
                        temp[(x,y)].append(num)
                        num = possible
                if num is None:
                    solution[x][y] = 0
                    res = backtrack_from(x, y)
                    if isinstance(res, str):
                        no_solution = True
                        break
                    x, y = res
                    clear_num(x, y)
                    y-=1
                # else:
                solution[x][y] = num
                draw_num(num, x, y, col=BLUE, win=solution_surface)
                win.blit(solution_surface, (0,0))
                pygame.display.flip()
                pygame.time.delay(100)

            y+=1
            if y == 9:
                x+=1
                y=0
            if x == 9:
                solving = False # SOLVED            
            break

        pygame.display.flip()
        clock.tick(30)
    for row1,row2 in zip(game, solution):
        print(row1, row2)
    pygame.quit()


if __name__ == '__main__': main()