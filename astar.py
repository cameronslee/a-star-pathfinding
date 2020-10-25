import pygame
import math
from queue import PriorityQueue

#everything square
WIDTH = 800
#set up display
WIN = pygame.display.set_mode((WIDTH, WIDTH))
#caption for display
pygame.display.set_caption("A* Path finding Algorithm")

#color def
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


#keep track of nodes in grid with colors
class Spot:
    def __init__(self, row, col, width, total_rows):
        #avoid global variables
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    #has been considered
    def is_closed(self):
        return self.color == RED

    #is in open set
    def is_open(self):
        return self.color == GREEN

    #obstacle
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    #lt = less than
    def __lt__(self, other):
        return False

#heuristic function, first implementing manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return  abs(x1 - x2) + abs(y1 - y2)

#hold all spots in grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(0, rows):
        grid.append([])
        for j in range(0, rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot) #in row i append the spot 

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

#mouse pos
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

#main loop
def main(win, width):
    ROWS = 50 # 50 x 50 grid can be changed
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            #if algorithm has begun continue, user cannot touch anything during alg
            if started:
                continue
            
            # 0 == left mouse button, 1 == middle  2 == right mouse 
            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                #print('Mouse positon: ', pos)
                row, col = get_clicked_pos(pos, ROWS, width)
                #print('Row, col: ', row, col)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pass

    pygame.quit()

main(WIN, WIDTH)

    
