from collections import OrderedDict
import pygame,random
from pygame.locals import *

pygame.init()

font_size             = 30
myfont                = pygame.font.SysFont("monospace", font_size)

speed                 = 10 # how many iterations per second
squares               = 2 # size of squares: 0 = 8X8, 1 = 16X16, 2 = 32X32, 3 = 64X64
map_size_x            = 32 # the width and height
map_size_y            = 58 # the width and height

death_lower_threshold = 3
death_upper_threshold = 2

spawn_lower_threshold = 2
spawn_upper_threshold = 4

if squares == 0:
    imgs = ["res/alive_8.png","res/dead_8.png",8]
if squares == 1:
    imgs = ["res/alive_16.png","res/dead_16.png",16]
if squares == 2:
    imgs = ["res/alive_32_A.png","res/alive_32_B.png","res/alive_32_C.png","res/alive_32_D.png","res/dead_32.png",32]
if squares == 3:
    imgs = ["res/alive_64.png","res/dead_64.png",64]

#-----CONFIG-----

width       = map_size_y * imgs[5]
height      = map_size_x * imgs[5]
screen_size = width,height
screen      = pygame.display.set_mode(screen_size)
clock       = pygame.time.Clock()
alive       = [pygame.image.load(imgs[0]).convert(),
               pygame.image.load(imgs[1]).convert(),
               pygame.image.load(imgs[2]).convert(),
               pygame.image.load(imgs[3]).convert()]
dead        = pygame.image.load(imgs[4]).convert()
done        = False

class cell:
    def __init__(self, location, alive = False):
        self.to_be     = None
        self.alive     = alive
        self.pressed   = False
        self.location  = location
        self.cell_type = random.randint(0,3)

    def set_type(self):
        self.cell_type = random.randint(0,3)

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

        label_x = 10
        label_y = 10
        label = myfont.render("death_upper_threshold = {0} (g: - | h: +)".format(death_upper_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y))
        label = myfont.render("death_lower_threshold = {0} (v: - | b: +)".format(death_lower_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 1))
        label = myfont.render("spawn_upper_threshold = {0} (n: - | m: +)".format(spawn_upper_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 2))
        label = myfont.render("spawn_lower_threshold = {0} (j: - | k: +)".format(spawn_lower_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 3))

    def get_cells(self,cell):# gets the cells around a cell
        mapa = self.map
        a = []
        b = []
        c = 0
        cell_loc = cell.location
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]-1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1])].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1])].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]-1)][abs(cell_loc[1]+1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0])][abs(cell_loc[1]+1)].location)
        except Exception: pass
        try: a.append(mapa[abs(cell_loc[0]+1)][abs(cell_loc[1]+1)].location)
        except Exception: pass
        num = len(list(OrderedDict.fromkeys(a)))# removes duplicates
        for i in xrange(len(a)):
            b.append(mapa[a[i][0]][a[i][1]].alive)
        for i in b:# c houses how many cells are alive around it
            if i == True:
                c += 1

        if cell.alive == True:
            if death_lower_threshold >= death_upper_threshold:
                if c > death_lower_threshold:
                    cell.to_be = False
                    cell.set_type()
                if c < death_upper_threshold:
                    cell.to_be = False
                    cell.set_type()
            else:
                if c > death_lower_threshold and c < death_upper_threshold:
                    cell.to_be = False
                    cell.set_type()
        else:
            if spawn_lower_threshold >= spawn_upper_threshold:
                if c > spawn_lower_threshold:
                    cell.to_be = True
                if c < spawn_upper_threshold:
                    cell.to_be = True
            else:
                if c > spawn_lower_threshold and c < spawn_upper_threshold:
                    cell.to_be = True

    def update_frame(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell = self.map[i][g]
                self.get_cells(cell)

    def update(self):
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                cell                     = self.map[i][g]
                loc                      = cell.location
                if cell.to_be           != None:
                    cell.alive = cell.to_be
                if self.map[i][g].alive == True:
                    screen.blit(alive[cell.cell_type],(loc[0]*imgs[5],loc[1]*imgs[5]))
                else:
                    screen.blit(dead,(loc[0]*imgs[5],loc[1]*imgs[5]))
                cell.to_be               = None

        label_x = 10
        label_y = 10
        label = myfont.render("death_upper_threshold = {0} (g: - | h: +)".format(death_upper_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y))
        label = myfont.render("death_lower_threshold = {0} (v: - | b: +)".format(death_lower_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 1))
        label = myfont.render("spawn_upper_threshold = {0} (n: - | m: +)".format(spawn_upper_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 2))
        label = myfont.render("spawn_lower_threshold = {0} (j: - | k: +)".format(spawn_lower_threshold), 1, (255,255,0))
        screen.blit(label, (label_x, label_y + font_size * 3))

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

            if event.key == K_g:
                if death_upper_threshold >= 0:
                    death_upper_threshold -= 1
            if event.key == K_h:
                if death_upper_threshold <= 9 :
                    death_upper_threshold += 1

            if event.key == K_v:
                if death_lower_threshold >= 0:
                    death_lower_threshold -= 1
            if event.key == K_b:
                if death_lower_threshold <= 9 :
                    death_lower_threshold += 1

            if event.key == K_j:
                if spawn_lower_threshold >= 0:
                    spawn_lower_threshold -= 1
            if event.key == K_k:
                if spawn_lower_threshold <= 9 :
                    spawn_lower_threshold += 1

            if event.key == K_n:
                if spawn_upper_threshold >= 0:
                    spawn_upper_threshold -= 1
            if event.key == K_m:
                if spawn_upper_threshold <= 9 :
                    spawn_upper_threshold += 1

        if event.type == KEYUP:
            if event.key == K_q:
                run = False
                board.update_frame()
                board.update()

        if event.type == MOUSEBUTTONUP:
            for i in xrange(map_size_y):
                for g in xrange(map_size_x):
                    board.map[i][g].pressed = False

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

    if mouse[0]:# makes cells alive
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and \
                pos[0] < rects[i][g][0] + imgs[5] and \
                pos[1] >= rects[i][g][1] and \
                pos[1] < rects[i][g][1] + imgs[5] and \
                board.map[i][g].pressed == False:

                    board.map[i][g].alive = True
                    board.map[i][g].pressed = True
                    board.update()

    if mouse[2]: # kills cells
        rects = cell_list()
        for i in xrange(map_size_y):
            for g in xrange(map_size_x):
                if pos[0] >= rects[i][g][0] and pos[0] < rects[i][g][0]+imgs[5] and pos[1] >= rects[i][g][1] and pos[1] < rects[i][g][1]+imgs[5] and board.map[i][g].pressed == False:
                    board.map[i][g].alive = False
                    board.map[i][g].pressed = False
                    board.update()

    pygame.display.flip()

pygame.quit()
