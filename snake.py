# Instruction:
# To start the game: press ENTER
# use W A S D to control the direction (W:up S:down A:left D:right)
# To pause: press SPACE
# To resume: press SPACE again
# To start again: press ENTER

import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
SIZE = 20

FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]


def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('JR Snake')

    light = (100, 100, 100)  # Color of Snake
    dark = (200, 200, 200)  # Color of food

    font1 = pygame.font.SysFont('freesasbold', 24)  # font of score
    font2 = pygame.font.Font(None, 72)  # "GAME OVER" font
    red = (200, 30, 30)                 # "GAME OVER" font color
    fwidth, fheight = font2.size('GAME OVER')
    line_width = 1                      # width of grid
    black = (0, 0, 0)                   # color of grid
    bgcolor = (40, 40, 60)              # background color

    # Direction, starts from the right
    pos_x = 1
    pos_y = 0
    b = True  # in case of the game goes wrong
    # Scope
    scope_x = (0, SCREEN_WIDTH // SIZE - 1)
    scope_y = (2, SCREEN_HEIGHT // SIZE - 1)
    # snake
    snake = deque()
    # food
    food_x = 0
    food_y = 0
    food_style = None

    # initialize
    def _init_snake():
        nonlocal snake
        snake.clear()
        snake.append((2, scope_y[0]))
        snake.append((1, scope_y[0]))
        snake.append((0, scope_y[0]))

    # food
    def _create_food():
        nonlocal food_x, food_y, food_style
        food_x = random.randint(scope_x[0], scope_x[1])
        food_y = random.randint(scope_y[0], scope_y[1])
        while (food_x, food_y) in snake:
            # to prevent that food appears on the snake
            food_x = random.randint(scope_x[0], scope_x[1])
            food_y = random.randint(scope_y[0], scope_y[1])
        food_style = FOOD_STYLE_LIST[random.randint(0, 2)]

    _init_snake()
    _create_food()

    game_over = True
    start = False
    score = 0
    orispeed = 0.2
    speed = orispeed
    last_move_time = None
    pause = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        _init_snake()
                        _create_food()
                        pos_x = 1
                        pos_y = 0
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                elif event.key in (K_w, K_UP):
                    if b and not pos_y:
                        pos_x = 0
                        pos_y = -1
                        b = False
                elif event.key in (K_s, K_DOWN):
                    if b and not pos_y:
                        pos_x = 0
                        pos_y = 1
                        b = False
                elif event.key in (K_a, K_LEFT):
                    if b and not pos_x:
                        pos_x = -1
                        pos_y = 0
                        b = False
                elif event.key in (K_d, K_RIGHT):
                    if b and not pos_x:
                        pos_x = 1
                        pos_y = 0
                        b = False

        # fill the background color
        screen.fill(bgcolor)
        # vertical grid
        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen, black, (x, scope_y[0] * SIZE), (x, SCREEN_HEIGHT), line_width)
        # horizontal grid
        for y in range(scope_y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen, black, (0, y), (SCREEN_WIDTH, y), line_width)

        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos_x, snake[0][1] + pos_y)
                    if next_s[0] == food_x and next_s[1] == food_y:
                        # if snake eats its food
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orispeed - 0.03 * (score // 100)
                        _create_food()
                    else:
                        if scope_x[0] <= next_s[0] <= scope_x[1] and scope_y[0] <= next_s[1] <= scope_y[1] \
                                and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True

        # food
        if not game_over:
            pygame.draw.rect(screen, food_style[1], (food_x * SIZE, food_y * SIZE, SIZE, SIZE), 0)

        # snake
        for s in snake:
            pygame.draw.rect(screen, dark, (s[0] * SIZE + line_width, s[1] * SIZE + line_width,
                                            SIZE - line_width * 2, SIZE - line_width * 2), 0)

        print_text(screen, font1, 30, 7, f'Speed: {score//100}')
        print_text(screen, font1, 450, 7, f'Score: {score}')

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER', red)

        pygame.display.update()
        # print(score)


if __name__ == '__main__':
    main()
