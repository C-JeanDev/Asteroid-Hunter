from enum import Enum
import pygame
from Entities.Entity import Entity

asteroid_str = "Texture/asteroid/as1.png"

# Global Fonts and Sizes
pygame.init()
title_size: int = 80
desc_size: int = 50
com_size: int = 30
title = pygame.font.Font('Fonts/retro.ttf', title_size)
desc = pygame.font.Font('Fonts/retro.ttf', desc_size)
com = pygame.font.Font('Fonts/retro.ttf', com_size)

vec2 = pygame.math.Vector2

class MODE(Enum):
    SIMPLE = 0,
    MEDIUM = 1,
    HARD = 2,
    SHOP = 3,
    MENU = 4,
    DEFAULT = 5,

    def __int__(self):
        return self.value[0]

class SHOP(Enum):
    BG = 0,
    SP_SHIP = 1,
    ASTEROID = 2,
    BACK = 3,
    DEFAULT = 4,

    def __int__(self):
        return self.value[0]

def load_coin(win,x: float, y: float):
        texture = pygame.image.load("Texture/coin.png").convert_alpha()
        texture = pygame.transform.scale(texture,(50,50))
        rect = texture.get_rect()
        rect.x = x
        rect.y = y
        win.blit(texture,rect)

def int_to_option(n: int) -> SHOP:
    if n == 0:
        return SHOP.BG
    if n == 1:
        return SHOP.SP_SHIP
    if n == 2:
        return SHOP.ASTEROID
    if n == 3:
        return SHOP.BACK
    if n == 4:
        return SHOP.DEFAULT

def int_to_mode(n: int) -> MODE:
    if n == 0:
        return MODE.SIMPLE
    if n == 1:
        return MODE.MEDIUM
    if n == 2:
        return MODE.HARD
    if n == 4:
        return MODE.MENU
    if n == 3:
        return MODE.SHOP

def getOverlap(e1: Entity, e2: Entity):
    x1 = e1.position.x
    y1 = e1.position.y

    x2 = e2.position.x
    y2 = e2.position.y

    w1 = e1.width
    h1 = e1.height

    w2 = e2.width
    h2 = e2.height

    delta =vec2(abs(x1-x2),abs(y1-y2))
    ox = w1/2 + w2/2 - delta.x
    oy = h1/2 + h2/2 - delta.y


    if ox < 0 : ox = 0
    if oy < 0 : oy = 0

    return vec2(ox,oy)