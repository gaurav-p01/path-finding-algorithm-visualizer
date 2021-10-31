import pygame
from sys import exit

# fps
clock = pygame.time.Clock()
FPS = 30

# blocks and window sizes | rows = columns, breadth = width
WIDTH = 600
ROWS = 30
BLOCK_WIDTH = WIDTH//ROWS

# colors 1
NEIGHBOR_COLOR = "#d8bfff" # light purple
CLOSED_COLOR = "#b280ff" # purple
BARRIER_COLOR = "#000000" # black
DEFAULT_COLOR = "#ffffff" # white
START_COLOR = "#ff9999" # red
END_COLOR = "#99ff99" # green
ROUTE_COLOR = "#ffff99" # yellow
LINE_COLOR = "#000000" # black


#colors 2
# NEIGHBOR_COLOR = "#eaf4ff" # light blue
# CLOSED_COLOR = "#add6ff" #blue
# BARRIER_COLOR = "#000000" #black
# DEFAULT_COLOR = "#ffffff" #white
# START_COLOR = "#ff9999" # red 
# END_COLOR = "#99ff99" # green
# ROUTE_COLOR = "#ffff99" # yellow
# LINE_COLOR = "#000000" # black


WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Path Finding Algorithm")

class Block:
    def __init__(self, row, col):
        self.row = row
        self.x = self.row*BLOCK_WIDTH
        self.col = col
        self.y = self.col*BLOCK_WIDTH
        self.color = DEFAULT_COLOR
        self.g_score = float("inf")
        self.f_score = float("inf")
        self.came_from = None
        self.id = (self.row * ROWS) + self.col


    def get_neighbors(self):
        neighbors = []
        if self.row > 0:
            neighbors.append([self.row - 1, self.col])
        if self.col > 0:
            neighbors.append([self.row, self.col - 1])
        if self.row < ROWS - 1:
            neighbors.append([self.row +1, self.col])
        if self.col < ROWS - 1:
            neighbors.append([self.row, self.col + 1])

        return neighbors


    def is_start(self):
        return self.color == START_COLOR

    def is_end(self):
        return self.color == END_COLOR

    def is_barrier(self):
        return self.color == BARRIER_COLOR
    
    def is_closed(self):
        return self.color == CLOSED_COLOR

    def is_neighbor(self):
        return self.color == NEIGHBOR_COLOR

    def make_neighbor(self):
        self.color = NEIGHBOR_COLOR
    
    def make_closed(self):
        self.color = CLOSED_COLOR

    def make_start(self):
        self.color = START_COLOR

    def make_end(self):
        self.color = END_COLOR
    
    def make_barrier(self):
        self.color = BARRIER_COLOR

    def make_route(self):
        self.color = ROUTE_COLOR

    def make_default(self):
        self.color = DEFAULT_COLOR

    def draw_block(self):
        rect = pygame.Rect(self.x, self.y, BLOCK_WIDTH, BLOCK_WIDTH)
        pygame.draw.rect(WIN, self.color, rect)


def get_block_pos(mouse_pos):
    row = mouse_pos[0]//BLOCK_WIDTH
    col = mouse_pos[1]//BLOCK_WIDTH

    return row, col
    

def draw_grid():
    for i in range(1, ROWS):
        pygame.draw.line(WIN, LINE_COLOR, (0, i*BLOCK_WIDTH), (WIDTH, i*BLOCK_WIDTH))
    for j in range(1, ROWS):
        pygame.draw.line(WIN, LINE_COLOR, (j*BLOCK_WIDTH, 0), (j*BLOCK_WIDTH, WIDTH))


def make_blocks():
    blocks = []
    for i in range(ROWS):
        blocks.append([])
        for j in range(ROWS):
            block = Block(i, j)
            blocks[i].append(block)
    return blocks


def draw(blocks):
    for row in blocks:
        for block in row:
            block.draw_block()

    draw_grid()
    pygame.display.update()


def get_distance_from_end(block, end):
    distance = abs(block.row - end.row) + abs(block.col - end.col)
    return distance


def astar_algorithm(draw, blocks, start, end):

    open_blocks = {}
    start.g_score = 0
    start.f_score = 0 + get_distance_from_end(start, end)
    open_blocks[start.f_score] = [start]
    came_from = {}


    while len(open_blocks) > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
   
        f_scores = list(open_blocks.keys())
        f_scores.sort() 
        current = open_blocks[f_scores[0]][0]
        open_blocks[f_scores[0]].pop(0)

        neighbors = current.get_neighbors()
        prev = None
        temp_curr = current

        for neighbor in neighbors:
            x, y = neighbor
            curr_neighbor = blocks[x][y]

            if curr_neighbor.is_end():
                while current != start:
                    current.make_route()
                    current = came_from[current]
                    draw()
                    clock.tick(FPS)
                return True

            if curr_neighbor.is_barrier():
                continue
            if curr_neighbor.is_closed():
                continue
            if curr_neighbor.is_start():
                continue
            if curr_neighbor.is_neighbor():
                continue

            curr_neighbor.make_neighbor()

            if (current.g_score + 1) < curr_neighbor.g_score:
                curr_neighbor.g_score = current.g_score + 1

            curr_neighbor.f_score = curr_neighbor.g_score + get_distance_from_end(curr_neighbor, end)

            if curr_neighbor.f_score not in open_blocks:
                open_blocks[curr_neighbor.f_score] = [curr_neighbor]

            open_blocks[curr_neighbor.f_score] += [curr_neighbor]

            if prev == None:
                prev = curr_neighbor

            if curr_neighbor.f_score <= prev.f_score:
                temp_curr = curr_neighbor
                came_from[temp_curr] = current

            prev = curr_neighbor


        if current != start:
            current.make_closed()

        if len(open_blocks[current.f_score]) < 1:
            open_blocks.pop(current.f_score)

        current = temp_curr
        
        draw()

        clock.tick(FPS)

    return False



def main(WIN, WIDTH):
    blocks = make_blocks()
    start = None
    end = None
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        if pygame.mouse.get_pressed()[0]: # left mouse button

            pos = pygame.mouse.get_pos()
            row, col = get_block_pos(pos)
            block = blocks[row][col]

            if start == None:
                start = block
                start.make_start()

            elif end == None and not block.is_start():
                end = block
                end.make_end()
                
            elif not block.is_start() and not block.is_end():
                block.make_barrier()

        elif pygame.mouse.get_pressed()[2]: # right mouse button

            pos = pygame.mouse.get_pos()
            row, col = get_block_pos(pos)
            block = blocks[row][col]

            if block.is_start():
                start = None

            if block.is_end():
                end = None

            block.make_default()

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_SPACE] == True: # space key

            blocks = make_blocks() # cleans screen/ makes all blocks default
            start = None
            end = None

        elif keys_pressed[pygame.K_RETURN] == True: # enter key

            if start != None and end != None:
                astar_algorithm(lambda: draw(blocks), blocks, start, end)

        draw(blocks)

main(WIN, WIDTH)
pygame.quit()

