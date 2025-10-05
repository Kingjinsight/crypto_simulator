from enum import Enum, auto
import pygame

screen = pygame.display.set_mode((1280, 960))

class SpaceType(Enum):
    SALARY = auto()
    RAND_EVENT = auto()

class Space(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        self.image = pygame.Surface((100,100))
        self.image.fill((255,0,0))
        pygame.draw.rect(self.image, (0,0,0), self.image.get_rect(), 3)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.type = type

route = []

x_pos = [290,390,490,590,690,790,890,990]
y_pos = [130,230,330,430,530,630,730,830]

for x in x_pos:
    route.append((x, y_pos[0]))
for y in y_pos[1:]:
    route.append((x_pos[-1], y))
for x in reversed(x_pos[:-1]):
    route.append((x, y_pos[-1]))
for y in reversed(y_pos[1:-1]):
    route.append((x_pos[0], y))

class Board(pygame.sprite.Sprite):
    def __init__(self):
        self.spaces = []
        for i in range(28):
            self.spaces.append(Space(route[i], SpaceType.SALARY if i % 7 == 0 else SpaceType.RAND_EVENT))

    def draw(self):
        pygame.sprite.Group(self.spaces).draw(screen)