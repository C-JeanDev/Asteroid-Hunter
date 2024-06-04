import Utils
from Entities.Entity import *
from enum import Enum


class SIZE(Enum):
    SMALL = 1,
    MEDIUM = 2,
    LARGE = 3,
    DEFAULT = 4,


class Asteroid(Entity):

    def __init__(self, win, width: int, height: int, position: vec2, vel: vec2,):
        super().__init__(win, width, height, position, vel, (0, 0, 0), TAG.ENEMY)

        self.texture = pygame.image.load(Utils.asteroid_str).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()
        self.size: SIZE = self.set_size()

        # print(self.size, self.width)

    def set_size(self) -> SIZE:
        if self.width < 40:
            return SIZE.SMALL
        elif self.width < 75:
            return SIZE.MEDIUM
        elif self.width < 101:
            return SIZE.LARGE

    def draw(self) -> None:
        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y


class Fireball(Entity):

    def __init__(self, win, width: int, height: int, position: vec2, vel: vec2,):
        super().__init__(win, width, height, position, vel, (0, 0, 0), TAG.ENEMY)

        self.texture = pygame.image.load("Texture/fireball.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()


    def draw(self) -> None:
        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y