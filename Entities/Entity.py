import pygame
from enum import Enum

vec2 = pygame.math.Vector2


class TAG(Enum):
    PLAYER = 1,
    ENEMY = 2,
    TILE = 3,
    BULLET = 4,


class Entity:

    def __init__(self, win, width: int, height: int, position: vec2, vel: vec2, color: tuple, tag: TAG):
        self.width = width
        self.height = height
        self.position = position
        self.win = win
        self.vel = vel
        self.tag = tag
        self.color = color
        self.alive: bool = True

        self.texture = pygame.image.load("Texture/asteroid/as1.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()


    def draw(self) -> None:
        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
    # def draw(self) -> None:
    #     pygame.draw.rect(self.win, self.color,
    #                      (self.position.x, self.position.y, self.width, self.height))
