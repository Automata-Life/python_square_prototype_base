from collections import OrderedDict
import pygame,random
from pygame.locals import *

from map_gui_widgets import Selector, CheckBoxArray, Button

pygame.init()

font_size             = 30
myfont                = pygame.font.SysFont("monospace", font_size)

speed                 = 10 # how many iterations per second
squares               = 2 # size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size_x            = 25 # the width and height
map_size_y            = 40 # the width and height

n_types = 3

if squares == 0:
    imgs = ["res/alive_8.png","res/dead_8.png",8]
if squares == 1:
    imgs = ["res/alive_16.png","res/dead_16.png",16]
if squares == 2:
    imgs = ["res/alive_32_A.png","res/alive_32_B.png","res/alive_32_C.png","res/dead_32.png",32]
if squares == 3:
    imgs = ["res/alive_64.png","res/dead_64.png",64]

death_neighbors = ("0", "1", "2",
                   "3", "4", "5",
                   "6", "7", "8")

spawn_neighbors = ("0", "1", "2",
                   "3", "4", "5",
                   "6", "7", "8")

conway_death_rules = [ [ True, True, False, False, True, True, True, True, True ],
                       [ True, True, False, False, True, True, True, True, True ],
                       [ True, True, False, False, True, True, True, True, True ]
                     ]

conway_spawn_rules = [ [ False, False, False, True, False, False, False, False, False ],
                       [ False, False, False, True, False, False, False, False, False ],
                       [ False, False, False, True, False, False, False, False, False ]
                     ]

#-----CONFIG-----

width       = map_size_y * imgs[4]
height      = map_size_x * imgs[4]
screen_size = width,height + 40
screen      = pygame.display.set_mode(screen_size)
clock       = pygame.time.Clock()
alive       = [pygame.image.load(imgs[0]).convert(),
               pygame.image.load(imgs[1]).convert(),
               pygame.image.load(imgs[2]).convert()]
dead        = pygame.image.load(imgs[3]).convert()
done        = False

checkbox_start_spawn = (10,height)
checkbox_start_death = (10,height+20)
checkbox_space       = (20,0)
checkbox_spawn       = CheckBoxArray(spawn_neighbors, conway_spawn_rules, checkbox_start_spawn, checkbox_space)
checkbox_death       = CheckBoxArray(death_neighbors, conway_death_rules, checkbox_start_death, checkbox_space)

class cell:
    def __init__(self, location, alive = False, cell_type = 0):
        self.to_be     = None
        self.alive     = alive
        self.pressed   = False
        self.location  = location
        self.cell_type = cell_type

    def set_type(self, cell_type):
        self.cell_type = cell_type

class board:
    def __init__(self):
        self.map = []

    def fill(self,ran):
        for i in xrange(map_size_y):
            self.map.append([])
            for g in xrange(map_size_x):
                if ran == True:
                    a = random.randint(0,4)
                    if a == 0: self.map[i].insert(g,cell((i,g),True))
                    else: self.map[i].insert(g,cell((i,g)))
                else: self.map[i].insert(g,cell((i,g)))

    def draw(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell = self.map[i][g]
                loc = cell.location
                if cell.alive == True:
                    screen.blit(alive[cell.cell_type], (loc[0]*imgs[5],loc[1]*imgs[5]))
                else:
                    screen.blit(dead,(loc[0]*imgs[5],loc[1]*imgs[5]))

        checkbox_spawn.draw(screen)
        checkbox_death.draw(screen)

    def neighbors(self, cell):
        cell_x = cell.location[0]
        cell_y = cell.location[1]

        neighbors  = []
        directions = [(-1, -1), (-1,  0), (-1,  1),
                      ( 0, -1),           ( 0,  1),
                      ( 1, -1), ( 1,  0), ( 1,  1)]

        for direction in directions:
            try:
                neighbors.append(self.map[cell_x + direction[0]][cell_y + direction[1]])
            except:
                pass

        return neighbors

    def get_cells(self, cell):
        neighbors      = self.neighbors(cell)
        live_neighbors = []

        for i in range(n_types):
            live_neighbors.append([n for n in neighbors if n.alive and n.cell_type == i])

        checkbox_index = str(len(live_neighbors))

        if cell.alive == True:
            for checkbox in checkbox_death.checkboxes:
                if checkbox.name == checkbox_index and checkbox.checked:
                    cell.to_be = False
                    cell.set_type(cell.cell_type)
        else:
            for checkbox in checkbox_spawn.checkboxes:
                if checkbox.name == checkbox_index and checkbox.checked:
                    cell.to_be = True
                    cell.set_type(cell.cell_type)

    def update_frame(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell = self.map[i][g]
                self.get_cells(cell)

    def update(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell           = self.map[i][g]
                loc            = cell.location
                if cell.to_be != None:
                    cell.alive = cell.to_be
                if self.map[i][g].alive == True:
                    screen.blit(alive[cell.cell_type],(loc[0]*imgs[5],loc[1]*imgs[5]))
                else:
                    screen.blit(dead,(loc[0]*imgs[5],loc[1]*imgs[5]))
                cell.to_be               = None

        checkbox_spawn.draw(screen)
        checkbox_death.draw(screen)

def cell_list():
    lst = []
    for i in xrange(map_size_y):
        lst.append([])
        for g in xrange(map_size_x): lst[i].append((board.map[i][g].location[0] * imgs[5],
                                                  board.map[i][g].location[1] * imgs[5]))
    return lst

board = board()
board.fill(False)
board.draw()
tp    = 0
run   = False

while done == False:
    milliseconds  = clock.tick(60)
    seconds       = milliseconds / 1000.0
    tp           += milliseconds

    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                run = not run

        if event.type == KEYUP:
            if event.key == K_q:
                run = False
                board.update_frame()
                board.update()

        if event.type == MOUSEBUTTONUP:
            for i in xrange(map_size_y):
                for g in xrange(map_size_x):
                    board.map[i][g].pressed = False

        checkbox_spawn.get_event(event)
        checkbox_death.get_event(event)

    pressed = pygame.key.get_pressed()
    mouse   = pygame.mouse.get_pressed()
    pos     = pygame.mouse.get_pos()

    if pressed[K_r]:
        board.map = []
        board.fill(False)
        board.draw()

    if pressed[K_a]:
        board.map = []
        board.fill(True)
        board.draw()

    if run == True and tp >= 1000/speed :
        tp = 0
        board.update_frame()
        board.update()

    if mouse[0]: # makes cells alive
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and \
                pos[0] < rects[i][g][0] + imgs[5] and \
                pos[1] >= rects[i][g][1] and \
                pos[1] < rects[i][g][1] + imgs[5] and \
                board.map[i][g].pressed == False:

                    board.map[i][g].alive   = True

                    board.map[i][g].cell_type += 1
                    board.map[i][g].cell_type %= n_types

                    board.map[i][g].pressed = True
                    board.update()

    if mouse[2]: # kills cells
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and \
                pos[0] < rects[i][g][0] + imgs[5] and \
                pos[1] >= rects[i][g][1] and \
                pos[1] < rects[i][g][1] + imgs[5] and \
                board.map[i][g].pressed == False:

                    board.map[i][g].alive   = False
                    board.map[i][g].pressed = False
                    board.update()

    pygame.display.flip()

pygame.quit()
