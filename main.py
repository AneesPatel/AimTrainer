"""
Anees Patel

Create a game that gives you points for clicking on souls

3/8/22
"""


import pygame, time, sys, random
from pygame.locals import *


pygame.init()
FPS = 30

STATE = "game_over"
GAME_OVER = "game_over"
GAME_START = "game_start"
GAME_PLAY = "game_play"

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 640
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
SOUL_SIZE = 30
SOULS = []
FONT_SIZE = 32
FONT_OBJ = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
BIGGER_FONT_OBJ = pygame.font.Font('freesansbold.ttf', FONT_SIZE + 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


def main():
    global STATE, SOULS, DISPLAYSURF
    pygame.display.set_caption('Soul Reaper')
    total_score = 0
    highscore = 0
    time_left = 60
    fps_clock = pygame.time.Clock()
    mouse_x = 0
    mouse_y = 0
    accuracy = 0
    clicks_total = -1
    clicks_hit = 0
    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True
                clicks_total += 1

        if STATE == GAME_OVER:
            SOULS = []
            DISPLAYSURF.fill(BLACK)
            text_highscore = BIGGER_FONT_OBJ.render('Highscore: {}'.format(highscore), True, WHITE)
            font_obj_rect = text_highscore.get_rect()
            font_obj_rect.center = (WINDOW_WIDTH/2, FONT_SIZE)
            DISPLAYSURF.blit(text_highscore, font_obj_rect)
            text_surface = FONT_OBJ.render('GAME OVER: click', True, WHITE)
            DISPLAYSURF.blit(text_surface, (WINDOW_WIDTH/2 - 140, WINDOW_HEIGHT/2 - 20))
            if mouse_clicked == True:
                STATE = GAME_START
                total_score = 0
                time_left = 60
                accuracy = 0
                clicks_total = 0
                clicks_hit = 0
        elif STATE == GAME_START:
            pygame.mixer.music.load('sounds/reaper.mp3')
            pygame.mixer.music.set_volume(.1)
            pygame.mixer.music.play(-1, 0.0)
            spawn_souls(10)
            time_left = 60
            STATE = GAME_PLAY
        elif STATE == GAME_PLAY:
            if clicks_total != 0:
                accuracy = clicks_hit / clicks_total
                display_accuracy(accuracy)
            display_time_score(time_left, total_score)
            if int(time_left) != int(time_left - 1/FPS):
                spawn_soul()
            time_left -= 1/FPS
            if len(SOULS) == 0:
                total_score += 10
                spawn_souls(10)

        for x in SOULS:
            pygame.draw.rect(DISPLAYSURF, WHITE, x)

        if pygame.Rect(mouse_x, mouse_y, 1, 1).collidelist(SOULS) != -1 and mouse_clicked == True:
            del(SOULS[pygame.Rect(mouse_x, mouse_y, 1, 1).collidelist(SOULS)])
            total_score += 1
            clicks_hit += 1
            soundObj = pygame.mixer.Sound('sounds/Osu hit sound aimlab(1).wav')
            soundObj.play()
        if int(time_left) == 0 and not STATE == GAME_OVER:
            if total_score > highscore:
                highscore = total_score
            pygame.mixer.music.stop()
            soundObj = pygame.mixer.Sound('sounds/gameover.wav')
            soundObj.play()
            STATE = GAME_OVER
            time.sleep(3)
            pygame.event.clear()

        pygame.display.update()
        fps_clock.tick(FPS)


def spawn_soul():
    global SOULS
    spawned = False
    while not spawned:
        current_soul = pygame.Rect(random.randint(0, WINDOW_WIDTH - SOUL_SIZE), random.randint(FONT_SIZE, WINDOW_HEIGHT - SOUL_SIZE), SOUL_SIZE, SOUL_SIZE)
        if current_soul.collidelist(SOULS) == -1:
            SOULS.append(current_soul)
            spawned = True


def spawn_souls(count):
    for x in range(count):
        spawn_soul()


def display_time_score(time, score):
    text_surface = FONT_OBJ.render('Score: {}'.format(score), True, WHITE)
    text_time = FONT_OBJ.render('Time: {}'.format(int(time)), True, WHITE)
    font_obj_rect = text_surface.get_rect()
    font_obj_rect.topleft = (0, 0)
    font_time_rect = text_time.get_rect()
    font_time_rect.topright = (WINDOW_WIDTH - 10, 0)
    DISPLAYSURF.blit(text_surface, font_obj_rect)
    DISPLAYSURF.blit(text_time, font_time_rect)

def display_accuracy(accuracy):
    if accuracy*100 >= 80:
        text_accuracy = FONT_OBJ.render('Accuracy: {:.2f}%'.format(100*accuracy), True, GREEN)
    elif accuracy * 100 >= 60:
        text_accuracy = FONT_OBJ.render('Accuracy: {:.2f}%'.format(100*accuracy), True, YELLOW)
    else:
        text_accuracy = FONT_OBJ.render('Accuracy: {:.2f}%'.format(100*accuracy), True, RED)

    font_obj_rect = text_accuracy.get_rect()
    font_obj_rect.center = (WINDOW_WIDTH/2, FONT_SIZE - 15)
    DISPLAYSURF.blit(text_accuracy, font_obj_rect)


if __name__ == '__main__':
    main()



