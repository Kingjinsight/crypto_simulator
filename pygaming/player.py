import pygame

screen = pygame.display.set_mode((1280, 960))

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.day = 0
        self.month = 1
        self.balance = 1000
        self.mood = 70

        self.image = pygame.Surface((80,80), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, (192,192,192), (40,40), 35)
        self.rect = self.image.get_rect()
        self.rect.center = route[self.day]

    @staticmethod
    def mood_to_word(mood):
        if mood <= 20:
            return "terrible"
        elif 20 < mood <= 40:
            return "bad"
        elif 40 < mood <= 60:
            return "average"
        elif 60 < mood <= 80:
            return "good"
        elif 80 < mood <= 100:
            return "amazing"

    def status(self):
        return f"You have £{self.balance} and are feeling {self.mood_to_word(self.mood)}."

    def date(self):
        return f"It is day {self.day+1} of month {self.month}."

    def advance(self):
        self.day += 1
        if self.day > 27:
            self.day %= 28
            self.month += 1

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.center = route[self.day % 28]
        if self.mood < 0:
            self.mood = 0
        if self.mood > 100:
            self.mood = 100