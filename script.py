import pygame
import sys
from time import sleep

# initialising pygame engine
pygame.init()

# setting screen size for our game
screen = pygame.display.set_mode((1280, 960))

# setting up clock for frame rate
clock = pygame.time.Clock()

# setting up board
class Space(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill((255,0,0))
        pygame.draw.rect(self.image, (0,0,0), self.image.get_rect(), 3)
        self.rect = self.image.get_rect()
        self.rect.center = pos

x_pos = [290,390,490,590,690,790,890,990]
y_pos = [130,230,330,430,530,630,730,830]

route = []

for x in x_pos:
    route.append((x, y_pos[0]))
for y in y_pos[1:]:
    route.append((x_pos[-1], y))
for x in reversed(x_pos[:-1]):
    route.append((x, y_pos[-1]))
for y in reversed(y_pos[1:-1]):
    route.append((x_pos[0], y))

spaces = []

for position in route:
    spaces.append(Space(position))

board_sprite = pygame.sprite.Group(spaces)

# setting up player character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80,80), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, (192,192,192), (40,40), 35)
        self.rect = self.image.get_rect()
        self.rect.center = route[0]

player_sprite = Player()
player_position = 0

# main game loop
running = True
waiting = True

while running:
    # EXIT CLAUSE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False

    # DRAWING ON SCREEN
    screen.fill((0,0,0))
    board_sprite.draw(screen)
    screen.blit(player_sprite.image, player_sprite.rect)

    # UPDATING SCREEN
    pygame.display.flip()
    clock.tick(30)

    # WAITING FOR USER TO PRESS ENTER KEY
    if waiting:
        continue

    # MOVE PLAYER
    player_sprite.rect.center = route[(player_position+1)%28]
    player_position += 1
    waiting = True


pygame.quit()
sys.exit()