import math, pygame, sys, algorithms
from pygame.locals import *

pygame.init()
font = pygame.font.SysFont("Arial", 20)
clock = pygame.time.Clock()
screen_x = 1200
screen_y = 1300
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Pathfinder")

ROWS = 50
WIDTH = screen_x

GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 69, 0)
PURPLE = (230, 230, 250)
TURQUOISE = (175, 238, 238)

class Node:
    def __init__(self, row, column, width, total_rows, color = WHITE):
        self.row = row
        self.column = column
        self.width = width
        self.x = row * width
        self.y = column * width
        self.color = color
        self.neighbors = {}
        self.total_rows = total_rows
    
    def get_position(self):
        return (self.row, self.column)

    def visited(self):  
        return self.color == RED

    def is_open(self):   
        return self.color == GREEN

    def is_barrier(self):  
        return self.color == BLACK

    def is_start(self):   
        return self.color == ORANGE

    def is_end(self):   
        return self.color == PURPLE

    def reset(self):  
        self.color == WHITE
    
    def add_neighbors(self):    # TODO: Account for edge cases
        pass

    def add_visited(self):
        self.color = WHITE

    def make_open(self):  
        self.color = GREEN

    def make_barrier(self):   
        self.color = BLACK

    def make_start(self):  
        self.color = ORANGE

    def make_end(self):   
        self.color = PURPLE

    def make_path(self):
        self.color = TURQUOISE

    def draw_node(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        return False

#|-------------------------------- Helper Functions --------------------------------|

def find_length(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def create_graph(rows, width):
    graph = []
    gap = width // rows
    for i in range(rows):
        graph.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            graph[i].append(node)
    return graph    # Object that holds every node in list form, Ex. [ [ [x, y], [x, y] ], [ [x, y], [x, y] ] ]
                    # Expresses as graph[row_y][row_x][element]

def draw_grids(surf, rows, width):
    gap = width // rows   # Gap between nodes
    for i in range(rows):   # Draws vertical rows
        pygame.draw.line(surf, GREY, (0, i*gap), (width, i*gap))
    for j in range(rows):   # Draws horizontal rows
        pygame.draw.line(surf, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    for row in grid:
        for node in row:
            node.draw_node(win)

    draw_grids(win, rows, width)

def get_mouse_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    if y == 0: row = 0
    else: row = y // gap    # Account for divide by 0
    if x == 0: col = 0
    else: col = x // gap
    return (row, col)

# |----------------------------------- Algorithms -----------------------------------|

def A_star(rows, width, start, end):
    pass

def Dijkstra(args):
    pass

# |------------------------------------ Main Loop ------------------------------------|

graph = create_graph(ROWS, WIDTH)   # Instantiate graph
start = False
curr_start = None
end = False
curr_end = None

while True:   # Main Loop
    raw_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = get_mouse_pos(raw_mouse_pos, ROWS, WIDTH)
    mouse_row = mouse_pos[0]
    mouse_col = mouse_pos[1]

    for event in pygame.event.get():   
        if event.type == QUIT:   # Quit the program
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0]:
            node = graph[mouse_row][mouse_col]
            node.make_barrier()
        if pygame.mouse.get_pressed()[2]:
            node = graph[mouse_row][mouse_col]
            node.reset()
        if event.type == KEYDOWN:
            if event == pygame.K_a:   # Make node start
                if start == False:
                    node = graph[mouse_row][mouse_col]
                    node.make_start()
                    curr_start = node
                else:
                    curr_start.reset()
                    node = graph[mouse_row][mouse_col]
                    node.make_start()
                    curr_start = node
            if event == pygame.K_s:   # Make node end
                if end == False:
                    node = graph[mouse_row][mouse_col]
                    node.make_start()
                    curr_end = node
                else:
                    curr_end.reset()
                    node = graph[mouse_row][mouse_col]
                    node.make_end()
                    curr_end = node

    draw(screen, graph, ROWS, WIDTH)

    pygame.display.update()

    clock.tick(60)