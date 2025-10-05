import pygame
import random
import sys

import boardclass, player, events

# initialising pygame engine
pygame.init()

# setting screen size for our game
screen = pygame.display.set_mode((1280, 960))

# setting up clock for frame rate
clock = pygame.time.Clock()

# setup board, player and font (for the HUD) objects
board = boardclass.Board()
player = player.Player()
font = pygame.font.SysFont('Arial', 30)

# main game loop
running = True
waiting = True

while running:
    # EVENTS
    for event in pygame.event.get():
        # EXIT CLAUSE
        if event.type == pygame.QUIT:
            running = False
        # MOVE TO NEXT DAY
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False

    # BACKGROUND
    screen.fill((0,0,0))

    # BOARD AND PLAYER
    board.draw()
    player.draw()

    # HUD (Money, Balance, Date)
    status_text = font.render(player.status(), True, (255,255,255))
    status_text_rect = status_text.get_rect(center=(640,480-150))
    screen.blit(status_text, status_text_rect.topleft)

    date_text = font.render(player.date(), True, (255,255,255))
    date_text_rect = date_text.get_rect(center=(640,480-150+font.get_linesize()))
    screen.blit(date_text, date_text_rect.topleft)

    # WAIT FOR USER TO PRESS ENTER KEY
    if waiting:
        continue

    # GAME LOGIC UPDATE
    if board.spaces[player.day].type == boardclass.SpaceType.SALARY:
        player.balance += 200

    if board.spaces[player.day].type == boardclass.SpaceType.RAND_EVENT:
        event_text = font.render(events.event(player, random.randint(1,2)), True, (255,255,255))
        event_text_rect = event_text.get_rect(center=(640,480+150))
        screen.blit(event_text, event_text_rect.topleft)

    # UPDATE SCREEN
    pygame.display.flip()
    clock.tick(30)

    # MOVE PLAYER
    player.advance()
    player.update()

    waiting = True
    
pygame.quit()
sys.exit()