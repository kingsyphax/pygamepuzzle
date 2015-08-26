#!/usr/bin/env python2.7

import pygame
import sys
from pygame.locals import *
import random
import math

pygame.init()

font = pygame.font.SysFont(None, 36)
 
def draw_text(display_string, font, surface, color, x, y):
    text_display = font.render(display_string, 1, color)
    text_rect = text_display.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_display, text_rect)

weights = [2] * 12
which = random.randrange(12)
heavier = random.randrange(0, 2) == 0
weights[which] = 1.5 + heavier

def totalweight(scale):
    total = 0
    for thing in scale:
        total += weights[thing]
    return total

colors = []

def colordist(first, second):
    return abs(first[0] - second[0]) / 180.0 + abs(first[1] - second[1]) / 180.0 + abs(first[2] - second[2]) / 180.0

for i in range(12):
    rand = (random.randrange(0, 180), random.randrange(0, 180), random.randrange(0, 180))
    while len(colors) > 0 and min([colordist(rand, color) for color in colors]) < 0.1:
        rand = (random.randrange(0, 180), random.randrange(0, 180), random.randrange(0, 180))
    colors.append(rand)

positions = [[x, 200] for x in range(230, 710, 40)]

scale1 = set()
scale2 = set()

screen = pygame.display.set_mode((900, 600))
screen.fill((255, 255, 255))
pygame.display.set_caption("Puzzle")

main_clock = pygame.time.Clock()

def dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def selection(x, y):
    for i in range(12):
        if dist([x, y], positions[i]) < 15:
            return i
    return -1

selected = -1
movingdown = -1

scale1y = 340
scale2y = 340

def inscale1(x, y):
    return 200 < x and x < 360 and scale1y - 80 < y and y < scale1y

def inscale2(x, y):
    return 540 < x and x < 700 and scale2y - 80 < y and y < scale2y

turn = 0
showing = 0
guessed = "neither"
correct = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            new_selection = selection(event.pos[0], event.pos[1])
            if turn < 5:
                if turn < 3 and selected > -1 and new_selection == -1: # moving
                    x, y = event.pos
                    positions[selected] = [x, y]

                    if selected in scale1:
                        scale1.remove(selected)
                    if selected in scale2:
                        scale2.remove(selected)
                    if inscale1(x, y):
                        movingdown = selected
                        scale1.add(selected)
                    if inscale2(x, y):
                        movingdown = selected
                        scale2.add(selected)

                    if turn == 0 and showing == 0:
                        showing = 0.1

                    selected = -1
                elif new_selection == selected: # deselecting
                    selected = -1
                    guessed = "neither"
                else: # switching selection
                    selected = new_selection
                if turn == 3 and guessed != "neither":
                    turn = 4
                    
        if event.type == KEYDOWN:
            if event.key == K_SPACE: # weighing!
                if turn < 3:
                    turn += 1
                    selected = -1
                    if totalweight(scale1) > totalweight(scale2):
                        scale1y = 370
                        scale2y = 310
                    elif totalweight(scale1) < totalweight(scale2):
                        scale1y = 310
                        scale2y = 370
                    else:
                        scale1y = 340
                        scale2y = 340
                elif turn == 4:
                    correct = (which == selected) and ((guessed == "heavier" and heavier) or (guessed == "lighter" and not heavier))
                    turn = 5
            if turn == 3 or turn == 4:
                if event.key == K_1:
                    guessed = "heavier"
                    if selected > -1:
                        turn = 4
                if event.key == K_2:
                    guessed = "lighter"
                    if selected > -1:
                        turn = 4
            if turn == 5 and event.key == K_RETURN:
                weights = [2] * 12
                which = random.randrange(12)
                heavier = random.randrange(0, 2) == 0
                weights[which - 1] = 1.5 + heavier

                colors = []

                for i in range(12):
                    rand = (random.randrange(0, 180), random.randrange(0, 180), random.randrange(0, 180))
                    while len(colors) > 0 and min([colordist(rand, color) for color in colors]) < 0.1:
                        rand = (random.randrange(0, 180), random.randrange(0, 180), random.randrange(0, 180))
                    colors.append(rand)

                positions = [[x, 200] for x in range(230, 710, 40)]

                scale1 = set()
                scale2 = set()

                selected = -1
                movingdown = -1

                scale1y = 340
                scale2y = 340

                turn = 0

    if movingdown > -1:
        if movingdown in scale1:
            if positions[movingdown][1] < scale1y - 12:
                positions[movingdown][1] += 5
            else:
                positions[movingdown][1] = scale1y - 12
        elif movingdown in scale2:
            if positions[movingdown][1] < scale2y - 12:
                positions[movingdown][1] += 5
            else:
                positions[movingdown][1] = scale2y - 12

    for i in range(0, 12):
        if i != movingdown:
            if i in scale1:
                positions[i][1] = scale1y - 12
            if i in scale2:
                positions[i][1] = scale2y - 12

    screen.fill((255, 255, 255))

    x_position = 230
    for i in range(12):
        if selected == i:
            pygame.draw.circle(screen, (230, 230, 0), positions[i], 14, 0)
        pygame.draw.circle(screen, colors[i], positions[i], 10, 0)
        x_position += 40

    pygame.draw.rect(screen, (0, 0, 0), Rect((200, scale1y), (160, 20)))
    pygame.draw.rect(screen, (0, 0, 0), Rect((540, scale2y), (160, 20)))

    if turn == 0:
        if showing == 0:
            draw_text("click marble to select", font, screen, (0, 0, 0), 320, 40)
            draw_text("then click above a scale", font, screen, (0, 0, 0), 310, 80)
        elif showing > 0 and showing < 1:
            draw_text("press space to weigh", font, screen, (255 - (255) * showing,) * 3, 320, 40)
            showing += 0.1
        elif showing >= 1:
            draw_text("press space to weigh", font, screen, (0, 0, 0), 320, 40)
    elif turn == 1 or turn == 2:
        draw_text("weighed %d times" % (turn), font, screen, (0, 0, 0), 360, 40)
    elif turn == 3:
        draw_text("click the odd ball!", font, screen, (0, 0, 0), 320, 40)
        draw_text("press 1 for heavier, 2 for lighter", font, screen, (0, 0, 0), 320, 80)
    elif turn == 4:
        draw_text("press space to check answer", font, screen, (0, 0, 0), 320, 40)
    elif turn == 5:
        if correct:
            draw_text("Correct!", font, screen, (0, 160, 0), 400, 40)
        else:
            draw_text("Incorrect", font, screen, (200, 0, 0), 400, 40)
        draw_text("press enter to play again", font, screen, (0, 0, 0), 320, 540)

    main_clock.tick(50)

    pygame.display.update()

