import pygame, random

import boardclass, player

pygame.init()

screen = pygame.display.set_mode((1280, 960))

font = pygame.font.SysFont('Arial', 30)

board = boardclass.Board()
player = player.Player()

def draw_all():
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

def rand_event(player, event_id):
    money = 0
    match event_id:
        case 1:
            x = random.randint(10,50)
            player.balance += x
            player.mood += round(x/2.5)
            text = font.render(f"You find £{x} on the street. Lucky you!", True, (255,255,255))
            text_rect = text.get_rect(center=(640,480+150))
            screen.blit(text, text_rect.topleft)

        case 2:
            x = random.randint(10,50)
            player.balance -= x
            player.mood -= round(x/2.5)
            text = font.render(f"You are robbed by some seagulls. You lose £{x}.", True, (255,255,255))
            text_rect = text.get_rect(center=(640,480+150))
            screen.blit(text, text_rect.topleft)

        case 3:
            x = random.randint(1,5)
            text = font.render(f"Marnix asks you to invest £50 in TrumpCoin. Do you accept? (Y/N)", True, (255,255,255))
            text_rect = text.get_rect(center=(640,480+150))
            screen.blit(text,text_rect.topleft)
            money = 100
    return money
