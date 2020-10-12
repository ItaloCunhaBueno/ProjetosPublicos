import pygame
import time
import random

screenW = 200
screenH = 200

def comi(x, y):
    return pygame.draw.rect(screen, RED, [x, y, 10, 10])

def drawcobra(corpo):
    def qua(x, y):
        return pygame.draw.rect(screen, WHITE, [x, y, 10, 10])
    for x in corpo:
        qua(x[0], x[1])


pygame.init()
screen = pygame.display.set_mode((screenW, screenH))
WHITE = (0, 255, 0)
RED = (255, 0, 0)
cobra = [[200,200], [190, 200], [180, 200], [170, 200]]

comidaposx = random.randrange(0, screenW, 10)
comidaposy = random.randrange(0, screenH, 10)
directionx = 10
directiony = 0
comi(comidaposx, comidaposy)
drawcobra(cobra)

while True:
    if (cobra[0][0], cobra[0][1]) == (comidaposx, comidaposy):
        comidaposx = random.randrange(0, screenW, 10)
        comidaposy = random.randrange(0, screenH, 10)
        ultimaposx, ultimaposy = cobra[-1][0], cobra[-1][1]
        for part in cobra[::-1][:-1]:
            index = cobra.index(part)
            cobra[index][0] = cobra[index-1][0]
            cobra[index][1] = cobra[index-1][1]
            screen.fill((0,0,0))
            drawcobra(cobra)
            comi(comidaposx, comidaposy)
            pygame.display.flip()

        cabeca = cobra[0]
        cabeca[0] += directionx
        cabeca[1] += directiony
        if cabeca[0] >= screenW:
            cabeca[0] = 0
        if cabeca[0] < 0:
            cabeca[0] = screenW-10
        if cabeca[1] >= screenH:
            cabeca[1] = 0
        if cabeca[1] < 0:
            cabeca[1] = screenH-10
        for part3 in cobra[1:]:
            if [cabeca[0], cabeca[1]] == part3:
                cobra = cobra[:4]
                break
        cobra.append([ultimaposx, ultimaposy])
        screen.fill((0,0,0))
        drawcobra(cobra)
        comi(comidaposx, comidaposy)
        pygame.display.flip()
    
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.KEYDOWN:
        if event.key == 273:
            if directiony == 10:
                pass
            else:
                directiony = -10
                directionx = 0
        elif event.key == 274:
            if directiony == -10:
                pass
            else:
                directiony = 10
                directionx = 0
        elif event.key == 276:
            if directionx == 10:
                pass
            else:
                directiony = 0
                directionx = -10
        elif event.key == 275:
            if directionx == -10:
                pass
            else:
                directiony = 0
                directionx = 10
    for part in cobra[::-1][:-1]:
        index = cobra.index(part)
        cobra[index][0] = cobra[index-1][0]
        cobra[index][1] = cobra[index-1][1]
        screen.fill((0,0,0))
        drawcobra(cobra)
        comi(comidaposx, comidaposy)
        pygame.display.flip()

    cabeca = cobra[0]
    cabeca[0] += directionx
    cabeca[1] += directiony
    if cabeca[0] >= screenW:
        cabeca[0] = 0
    if cabeca[0] < 0:
        cabeca[0] = screenW-10
    if cabeca[1] >= screenH:
        cabeca[1] = 0
    if cabeca[1] < 0:
        cabeca[1] = screenH-10
    for part3 in cobra[1:]:
        if [cabeca[0], cabeca[1]] == part3:
            cobra = cobra[:4]
            break
    screen.fill((0,0,0))
    drawcobra(cobra)
    comi(comidaposx, comidaposy)
    pygame.display.flip()
    time.sleep(0.08)
