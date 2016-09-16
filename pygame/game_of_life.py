from collections import OrderedDict
import pygame, random
from pygame.locals import *

from map_gui_widgets import Selector, CheckBoxArray, Button, ExclusiveCheckBoxArray

pygame.init()

font_size             = 30
myfont                = pygame.font.SysFont("monospace", font_size)

speed                 = 0.2 # how many iterations per second
squares               = 2 # size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size_x            = 25 # the width and height
map_size_y            = 40 # the width and height

n_types = 3

if squares == 0:
    imgs = ["res/alive_8.png","res/dead_8.png",8]
elif squares == 1:
    imgs = ["res/alive_16.png","res/dead_16.png",16]
elif squares == 2:
    imgs = ["res/alive_32_A.png", "res/alive_32_B.png", "res/alive_32_C.png", "res/dead_32.png", 32]
elif squares == 3:
    imgs = ["res/alive_64.png","res/dead_64.png",64]

size_id      = 4
dead_cell_id = 3

type_C_id    = 2
type_B_id    = 1
type_A_id    = 0

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

checkbox_selector_values = [ True, False, False ]

regex_mode = False

regex_death_neighbors = ("0", "1", "2",
                         "3",      "4",
                         "5", "6", "7")

regex_spawn_neighbors = ("0", "1", "2",
                         "3",      "4",
                         "5", "6", "7")



#-----CONFIG-----

width       = map_size_y * imgs[size_id]
height      = map_size_x * imgs[size_id]
screen_size = width, height + 60
screen      = pygame.display.set_mode(screen_size)
clock       = pygame.time.Clock()
alive       = [pygame.image.load(imgs[type_A_id]).convert(),
               pygame.image.load(imgs[type_B_id]).convert(),
               pygame.image.load(imgs[type_C_id]).convert()]
dead        = pygame.image.load(imgs[dead_cell_id]).convert()
done        = False

checkbox_start_selector = (50, height)
checkbox_start_spawn = (10, height + 20)
checkbox_start_death = (10, height + 40)

checkbox_space       = (20, 0)

checkbox_spawn       = [CheckBoxArray(spawn_neighbors, conway_spawn_rules[0], checkbox_start_spawn, checkbox_space),
                        CheckBoxArray(spawn_neighbors, conway_spawn_rules[1], checkbox_start_spawn, checkbox_space),
                        CheckBoxArray(spawn_neighbors, conway_spawn_rules[2], checkbox_start_spawn, checkbox_space)
                       ]

checkbox_death       = [CheckBoxArray(death_neighbors, conway_death_rules[0], checkbox_start_death, checkbox_space),
                        CheckBoxArray(death_neighbors, conway_death_rules[1], checkbox_start_death, checkbox_space),
                        CheckBoxArray(death_neighbors, conway_death_rules[2], checkbox_start_death, checkbox_space)
                       ]

checkbox_selector    = ExclusiveCheckBoxArray(["A", "B", "C"], checkbox_selector_values, checkbox_start_selector, checkbox_space)

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
                    a = random.randint(0, 1)
                    if a == 0:
                        self.map[i].insert(g, cell((i, g), True, random.randint(0, n_types - 1)))
                    else:
                        self.map[i].insert(g, cell((i, g)))
                else:
                    self.map[i].insert(g, cell((i, g)))

    def draw(self, rec_timer):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell = self.map[i][g]
                loc = cell.location
                if cell.alive == True:
                    screen.blit(alive[cell.cell_type], (loc[0]*imgs[4],loc[1]*imgs[4]))
                else:
                    screen.blit(dead,(loc[0]*imgs[4],loc[1]*imgs[4]))

        checkbox_selector.draw(screen)

        for i in range(len(checkbox_selector.checkboxes)):
            if checkbox_selector.checkboxes[i].checked:
                checkbox_spawn[i].draw(screen)
                checkbox_death[i].draw(screen)
                break

        rec_width = (width - 220) * rec_timer
        pygame.draw.rect(screen, (255, 165, 0), (200, height + 54, rec_width, 4))

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

        if cell.alive == True:
            original_type = cell.cell_type
            checkbox_index = str(len(live_neighbors[cell.cell_type]))
            for checkbox in checkbox_death[cell.cell_type].checkboxes:
                if checkbox.name == checkbox_index and checkbox.checked:
                    cell.to_be = False

            for i in range(n_types):
                if i != original_type:
                    checkbox_index = str(len(live_neighbors[i]))
                    for checkbox in checkbox_spawn[i].checkboxes:
                        if checkbox.name == checkbox_index and checkbox.checked:
                            cell.to_be = True
                            cell.set_type(i)

        else:
            for i in range(n_types):
                checkbox_index = str(len(live_neighbors[i]))
                for checkbox in checkbox_spawn[i].checkboxes:
                    if checkbox.name == checkbox_index and checkbox.checked:
                        cell.to_be = True
                        cell.set_type(i)

    def update_frame(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell = self.map[i][g]
                self.get_cells(cell)

    def update(self, rec_timer):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell           = self.map[i][g]
                loc            = cell.location
                if cell.to_be != None:
                    cell.alive = cell.to_be
                if self.map[i][g].alive == True:
                    screen.blit(alive[cell.cell_type],(loc[0]*imgs[4],loc[1]*imgs[4]))
                else:
                    screen.blit(dead,(loc[0]*imgs[4],loc[1]*imgs[4]))
                cell.to_be = None

        checkbox_selector.draw(screen)

        for i in range(len(checkbox_selector.checkboxes)):
            if checkbox_selector.checkboxes[i].checked:
                checkbox_spawn[i].draw(screen)
                checkbox_death[i].draw(screen)
                break

        rec_width = (width - 220) * rec_timer
        pygame.draw.rect(screen, (255, 165, 0), (200, height + 54, rec_width, 4))

def cell_list():
    lst = []
    for i in xrange(map_size_y):
        lst.append([])
        for g in xrange(map_size_x): lst[i].append((board.map[i][g].location[0] * imgs[4],
                                                  board.map[i][g].location[1] * imgs[4]))
    return lst

board = board()
board.fill(False)

tp            = 0
milliseconds  = clock.tick(60)
seconds       = milliseconds / 1000.0
tp           += milliseconds

if tp > (1000/speed):
    tp = 1000/speed

timer = tp / (1000/speed)

board.draw(timer)
run   = False

while done == False:
    milliseconds  = clock.tick(60)
    seconds       = milliseconds / 1000.0
    tp           += milliseconds

    if tp > (1000/speed):
        tp = 1000/speed

    timer = tp / (1000/speed)

    print tp

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
                board.update(timer)

        if event.type == MOUSEBUTTONUP:
            for i in xrange(map_size_y):
                for g in xrange(map_size_x):
                    board.map[i][g].pressed = False

        checkbox_selector.get_event(event)

        for i in range(len(checkbox_selector.checkboxes)):
            if checkbox_selector.checkboxes[i].checked:
                checkbox_spawn[i].get_event(event)
                checkbox_death[i].get_event(event)
                break

    pressed = pygame.key.get_pressed()
    mouse   = pygame.mouse.get_pressed()
    pos     = pygame.mouse.get_pos()

    if pressed[K_r]:
        board.map = []
        board.fill(False)
        board.draw(timer)

    if pressed[K_a]:
        board.map = []
        board.fill(True)
        board.draw(timer)

    board.update(timer)
    if run == True:
        board.update(timer)

        if tp >= 1000/speed :
            tp = 0
            board.update_frame()
            board.update(timer)

    if mouse[0]: # makes cells alive
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and \
                pos[0] < rects[i][g][0] + imgs[4] and \
                pos[1] >= rects[i][g][1] and \
                pos[1] < rects[i][g][1] + imgs[4] and \
                board.map[i][g].pressed == False:

                    board.map[i][g].alive   = True
                    for j in range(len(checkbox_selector.checkboxes)):
                        if checkbox_selector.checkboxes[j].checked:
                            board.map[i][g].cell_type = j
                            break
                    board.map[i][g].pressed = True
                    board.update(timer)

    if mouse[2]: # kills cells
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and \
                pos[0] < rects[i][g][0] + imgs[4] and \
                pos[1] >= rects[i][g][1] and \
                pos[1] < rects[i][g][1] + imgs[4] and \
                board.map[i][g].pressed == False:

                    board.map[i][g].alive   = False
                    board.map[i][g].pressed = False
                    board.update(timer)

    pygame.display.flip()

pygame.quit()
