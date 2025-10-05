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
in_event = 0
money_to_add = 0

while running:
    # EVENTS
    for event in pygame.event.get():
        # EXIT CLAUSE
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(f'in_event = {in_event}')
            # MOVE TO NEXT DAY
            if money_to_add == 0 and event.key == pygame.K_RETURN:
                waiting = False
            # ANSWER EVENT QUESTIONS
            if event.key == pygame.K_y and money_to_add > 0:
                print("I am being called")
                # MONEY = determine_how_much_money_to_receive(pass in y or n)
                player.balance += money_to_add
                money_to_add = 0
                in_event = 0
                waiting = False
            if event.key == pygame.K_n and money_to_add > 0:
                money_to_add = 0
                in_event = 0
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

    # if in_event:
    #     case
    else:
        # GAME LOGIC UPDATE
        if board.spaces[player.day].type == boardclass.SpaceType.SALARY:
            player.balance += 210

        if board.spaces[player.day].type == boardclass.SpaceType.RAND_EVENT:
            in_event = random.randint(1,3)
            money_to_add = events.rand_event(player, in_event)
            print(money_to_add)

    # UPDATE SCREEN
    pygame.display.flip()
    clock.tick(30)

# MOVE PLAYER
    player.advance()
    player.update()

    waiting = True
    
pygame.quit()
sys.exit()