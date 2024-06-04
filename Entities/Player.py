import pygame
from Entities.Entity import *

vec2 = pygame.math.Vector2

class Player(Entity):

    def __init__(self, win, width: int, height: int, position: vec2, vel: vec2, color: tuple, tag: TAG):
        super().__init__(win, width, height, position, vel, (0, 0, 0), TAG.PLAYER)

        self.texture = pygame.image.load("Texture/sships/spaceship0.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))
        self.rect = self.texture.get_rect()

        self.saved_pos: int = 0

    def draw(self) -> None:
        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    def move(self, keys):
        if keys[pygame.K_w] and self.position.y > 0:
            self.position.y -= self.vel.y
        if keys[pygame.K_s] and self.position.y < 1080 - self.height:
            self.position.y += self.vel.y
        if keys[pygame.K_a] and self.position.x > 0:
            self.position.x -= self.vel.x
        if keys[pygame.K_d] and self.position.x < 1920 - self.width:
            self.position.x += self.vel.x
