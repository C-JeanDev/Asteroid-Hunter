
from Entities.Entity import *

vec2 = pygame.math.Vector2

class Bullet(Entity):

    def __init__(self, win, position: vec2, vel: vec2, radius: int, angle: float):
        super().__init__(win, radius, radius, position, vel, (255,255,255), TAG.BULLET)
        self.texture = pygame.image.load("Texture/bullet1.png").convert_alpha()
        self.texture = pygame.transform.scale(self.texture,(radius/2,radius*1.5))
        self.rect = self.texture.get_rect()
        self.angle = angle
        self.texture = pygame.transform.rotate(self.texture, angle*70)




    def draw(self) -> None:
        # colour = (255, 255, 255)  # green
        # pos = (self.position.x, self.position.y)
        # circle_radius = 12
        # border_width = 0  # 0 = filled circle
        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        # pygame.draw.circle(self.win, colour, pos, circle_radius, border_width)