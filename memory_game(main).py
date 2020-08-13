import pygame
import random
import sys
from pygame.locals import *

FPS=30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARDWIDTH = 10
BOARDHEIGHT = 7
XMARGIN=int((WINDOWWIDTH - (BOARDWIDTH*(BOXSIZE + GAPSIZE))) / 2)
YMARGIN=int((WINDOWHEIGHT - (BOARDHEIGHT*(BOXSIZE + GAPSIZE))) / 2)

WHITE = (255, 255, 255)
NAVYBLUE = (60, 60, 100)
GRAY = (100, 100, 100)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)

BGCOLOR = NAVYBLUE
BOXCOLOR = WHITE
LIGHTBGCOLOR = GRAY
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINE = 'line'
OVAL = 'oval'

ALLCOLOR = (RED,GREEN,BLUE,YELLOW,ORANGE,PURPLE,CYAN)
ALLSHAPE = (DONUT,SQUARE,DIAMOND,LINE,OVAL)

def main():
    global FPSCLOCK
    global DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    firstselection = None
    pygame.display.set_caption('memory game')
    mainboard = getrandomizedicons()
    revealedboxes = generaterevealedboxes(False)
    gameanimation(mainboard,revealedboxes)
    gamewonanimation(mainboard)
    while True:
        mouseclicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawboxes(mainboard, revealedboxes)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseclicked = True
            boxx, boxy = checkifclickedonbox(mousex, mousey)
            if boxx != None or boxy != None:
                if not revealedboxes[boxx][boxy]:
                    drawhighlightbox(boxx, boxy)
                if not revealedboxes[boxx][boxy] and mouseclicked:
                    revealboxesanimation(mainboard, [(boxx, boxy)])
                    revealedboxes[boxx][boxy] = True
                    if firstselection == None:
                        firstselection = (boxx, boxy)
                    else:
                        icon1shape, icon1color = getshapecolor(mainboard, firstselection[0], firstselection[1])
                        icon2shape, icon2color = getshapecolor(mainboard, boxx, boxy)
                        if icon1shape != icon2shape or icon1color !=icon2color:
                            pygame.time.wait(1000)
                            coverboxesanimation(mainboard, [(firstselection[0], firstselection[1]), (boxx, boxy)])
                            revealedboxes[firstselection[0]][firstselection[1]] = False
                            revealedboxes[boxx][boxy] = False
                        elif haswon(revealedboxes):
                            gamewonanimation(mainboard)
                            pygame.time.wait(2000)
                            mainboard = getrandomizedicons()
                            revealedboxes = generaterevealedboxes(False)
                            drawboxes(mainboard, revealedboxes)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            gameanimation(mainboard, revealedboxes)
                        firstselection = None





        pygame.display.update()
        FPSCLOCK.tick(FPS)

def haswon(revealedboxes):
    for i in revealedboxes:
        if False in i:
            return False
    return True

def gamewonanimation(mainboard):
    coveredboxes = generaterevealedboxes(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawboxes(mainboard, coveredboxes)
        pygame.display.update()
        pygame.time.wait(300)


def drawhighlightbox(boxx, boxy):
    left, top = topleftcoor(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE + 10, BOXSIZE + 10), 4)

def checkifclickedonbox(mousex, mousey):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = topleftcoor(boxx, boxy)
            boxrect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxrect.collidepoint(mousex, mousey):
                return (boxx, boxy)
    return (None, None)

def drawboxes(mainboard, revealedboxes):
    for boxx in range(0, BOARDWIDTH):
        for boxy in range(0, BOARDHEIGHT):
            left,top = topleftcoor(boxx, boxy)
            if not revealedboxes[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape,color = getshapecolor(mainboard, boxx, boxy)
                drawicons(shape, color, boxx, boxy)

def getshapecolor(mainboard, boxx, boxy):
    shape = mainboard[boxx][boxy][0]
    color = mainboard[boxx][boxy][1]
    return (shape, color)

def drawicons(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    left,top = topleftcoor(boxx, boxy)
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
         pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE -1, top + half), (left + half, top + BOXSIZE -1), (left, top + half)))
    elif shape == LINE:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE -1), (left + BOXSIZE -1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))



def topleftcoor(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getrandomizedicons():
    icons=[]
    for color in ALLCOLOR:
        for shape in ALLSHAPE:
            icons.append((shape,color))
    random.shuffle(icons)
    numoficons=int((BOARDWIDTH * BOARDHEIGHT) / 2)
    icons = icons[:numoficons] * 2
    random.shuffle(icons)
    board=[]
    for x in range(BOARDWIDTH):
        column=[]
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def generaterevealedboxes(val):
    revealedboxes = []
    for x in range(BOARDWIDTH):
        revealedboxes.append([val] * BOARDHEIGHT)
    return revealedboxes

def splitintogroup(group, boxes):
    boxgroup=[]
    for x in range(0, len(boxes), group):
        boxgroup.append(boxes[x : x + group])
    return boxgroup

def drawboxcover(mainboard, boxgroup, coverage):
    for box in boxgroup:
        left,top = topleftcoor(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getshapecolor(mainboard, box[0], box[1])
        drawicons(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealboxesanimation(mainboard, boxgroup):
    for coverage in range(BOXSIZE, (-REVEALSPEED)-1, -REVEALSPEED):
        drawboxcover(mainboard, boxgroup, coverage)

def coverboxesanimation(mainboard, boxgroup):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawboxcover(mainboard, boxgroup, coverage)


def gameanimation(mainboard,coveredboxes):
     boxes=[]
     for x in range(BOARDWIDTH):
         for y in range(BOARDHEIGHT):
              boxes.append((x,y))
     random.shuffle(boxes)
     boxgroups = splitintogroup(8, boxes)
     drawboxes(mainboard, coveredboxes)
     for boxgroup in boxgroups:
         revealboxesanimation(mainboard, boxgroup)
         coverboxesanimation(mainboard, boxgroup)


if __name__=='__main__':
    main()
