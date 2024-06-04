import random
import time
import threading
import math
import Utils
from Utils import *
from Shop import Coin, Shop, Item
from Entities.Entity import *
from Entities.Bullet import Bullet
from Entities.Player import Player
from EntityManager import EntityManager
from Entities.Asteroid import Asteroid, Fireball


class GameEngine:

    def __init__(self):

        self.run: bool = True

        # Window Creation
        self.width: int = 1920
        self.height: int = 1080
        self.WIN_SIZE: tuple = (self.width, self.height)
        self.win = pygame.display.set_mode(self.WIN_SIZE, pygame.FULLSCREEN)

        # background
        self.bg = pygame.image.load("Texture/bg1.jpg")

        # Entity Manager
        self.em = EntityManager()

        # Player Creation
        self.player = Player(self.win, 125, 125, vec2(self.width / 2, self.height / 2), vec2(10, 10), (), TAG.PLAYER)
        self.em.add(self.player)

        self.coin = Coin()

        self.line: int = 0
        self.point: int = 0

        # Scenes
        self.mode = MODE.MENU
        self.opt = SHOP.DEFAULT

        self.shop = Shop()

        self.t = threading.Thread(target=self.stopWatchSeconds).start()

    def stopWatchSeconds(self):
        start_time = time.time()
        x = 0
        while self.run:
            elapsed = 1 - (time.time() - start_time)
            time.sleep(elapsed)
            start_time = time.time()
            x += 1
            try:
                if self.mode == MODE.SIMPLE or self.mode == MODE.MEDIUM or self.mode == MODE.HARD:
                    if x % abs(self.mode.__int__() - 5 + self.mode.__int__()) == 0:
                        self.em.add(self.create_enemy())
                    if self.point > 1000 and x % 2 == 0:
                        y = random.randint(100, 700)
                        self.em.add(Fireball(self.win, 160, 85, vec2(100, y), vec2(-8, 0)))
            except ZeroDivisionError:
                pass

    def create_enemy_pos(self, x: int, y: int) -> Entity:
        r: int = random.randint(50, 255)
        g: int = random.randint(50, 255)
        b: int = random.randint(50, 255)

        return Entity(self.win, 40, 40, vec2(x, y), vec2(5, 5), (r, g, b), TAG.ENEMY)

    def create_enemy(self) -> Entity:
        x: int = random.randint(1, self.width - self.player.width)
        y: int = random.randint(1, self.height - self.player.height)
        size: int = random.randint(30, 100)
        # r: int = random.randint(50, 255)
        # g: int = random.randint(50, 255)
        # b: int = random.randint(50, 255)

        return Asteroid(self.win, size, size, vec2(x, y), vec2(5, 5))

    def enemy_movement(self) -> None:
        for e in self.em.entities:
            # i.x += i.vel
            if e.tag == TAG.ENEMY:
                e.position.y += e.vel.y
                e.position.x -= e.vel.x

        for e in self.em.entities:
            if e.tag == TAG.BULLET:
                e.position.x += e.vel.x
                e.position.y += e.vel.y

    def collision(self) -> None:

        def check(entity):
            if entity.tag == TAG.BULLET:
                entity.alive = False
            elif entity.tag == TAG.ENEMY:
                entity.texture = pygame.transform.rotate(entity.texture, 180)

        # COLLISION  --- BULLET <-> ENEMY

        for e in self.em.entities:
            if e.tag == TAG.BULLET:
                for e1 in self.em.entities:
                    if e1.tag == TAG.ENEMY:
                        ol = getOverlap(e, e1)
                        if ol.x > 1 and ol.y > 1:
                            self.point += e1.width * 1
                            self.coin.coin += e1.width * 1
                            e.alive = False
                            e1.alive = False

        # COLLISION  --- PLAYER <-> ENEMY

        for e in self.em.entities:
            if e.tag != TAG.PLAYER and e.tag != TAG.BULLET:
                ol = getOverlap(self.player, e)
                if ol.x > 5 and ol.y > 5:
                    self.player.position.x = self.width / 2
                    self.player.position.y = self.height / 2
                    self.point = 0
                    e.alive = False

        for e in self.em.entities:
            if e.tag != TAG.PLAYER:
                if e.position.y > self.height - e.width:
                    e.vel.y *= -1
                    check(e)
                if e.position.y < 0:
                    e.vel.y *= -1
                    check(e)
                if e.position.x < 0:
                    e.vel.x *= -1
                    check(e)
                if e.position.x > self.width - e.width:
                    e.vel.x *= -1
                    check(e)

    def game_scene(self, keys) -> None:
        self.win.blit(desc.render("Score : " + str(self.point), True, "white"), (100, (desc_size + 10)))
        self.enemy_movement()
        self.player.move(keys)
        self.collision()
        self.em.write()

    def shop_scene(self) -> None:

        t1 = title.render("SHOP", True, "white")

        color1: str = "white"
        color2: str = "white"
        color3: str = "white"
        color4: str = "white"

        if self.line == 0:
            color1 = "blue"
        if self.line == 1:
            color2 = "blue"
        if self.line == 2:
            color3 = "blue"
        if self.line == 3:
            color4 = "blue"
        # if keys[pygame.K_UP]:

        t2 = desc.render("Background", True, color1)
        t3 = desc.render("Spaceship", True, color2)
        t4 = desc.render("Asteroids", True, color3)
        t5 = desc.render("<- Back", True, color4)

        self.win.blit(t1, (self.width / 2 - title_size, title_size))
        self.win.blit(t2, (self.width / 2 - desc_size, 400))
        self.win.blit(t3, (self.width / 2 - desc_size, 500))
        self.win.blit(t4, (self.width / 2 - desc_size, 600))
        self.win.blit(t5, (self.width / 2 - desc_size, 700))

        self.win.blit(com.render("W = UP        S = DOWN        SPACE = ENTER", True, "white"),
                      (50, self.height - (com_size + 10)))

    def menu_scene(self) -> None:

        t1 = title.render("Menu", True, "white")

        color1: str = "white"
        color2: str = "white"
        color3: str = "white"
        color4: str = "white"

        if self.line == 0:
            color1 = "blue"
        if self.line == 1:
            color2 = "blue"
        if self.line == 2:
            color3 = "blue"
        if self.line == 3:
            color4 = "blue"

        t2 = desc.render("Simple", True, color1)
        t3 = desc.render("Medium", True, color2)
        t4 = desc.render("Hard", True, color3)
        t5 = desc.render("Shop", True, color4)

        self.win.blit(t1, (self.width / 2 - title_size, title_size))
        self.win.blit(t2, (self.width / 2 - desc_size, 400))
        self.win.blit(t3, (self.width / 2 - desc_size, 500))
        self.win.blit(t4, (self.width / 2 - desc_size, 600))
        self.win.blit(t5, (self.width / 2 - desc_size, 700))

        self.win.blit(com.render("W = UP        S = DOWN        SPACE = ENTER", True, "white"),
                      (50, self.height - (com_size + 10)))

    def bg_scene(self, keys) -> None:
        self.win.blit(title.render("BACKGROUNDS", True, "white"), (self.width / 2 - title_size * 4, title_size))
        self.coin.read()
        self.win.blit(com.render(str(self.coin.coin), True, "white"), (self.width - self.width / 10, title_size * 1.5))

        load_coin(self.win, self.width - self.width / 10 + 100, title_size * 1.4)
        for i in self.shop.bgs:
            if (x := i.draw(keys, self.coin)) is not None:
                self.bg = pygame.image.load(x)

        self.win.blit(com.render("B = BACK      P = PURCHASE/SELECT", True, "white"),
                      (50, self.height - (com_size + 10)))

    def spaceship_scene(self, keys) -> None:
        self.win.blit(title.render("SPACESHIPS", True, "white"), (self.width / 2 - title_size * 4, title_size))
        self.coin.read()
        self.win.blit(com.render(str(self.coin.coin), True, "white"), (self.width - self.width / 10, title_size * 1.5))
        load_coin(self.win, self.width - self.width / 10 + 100, title_size * 1.4)

        for i in self.shop.spaceships:
            if (x := i.draw(keys, self.coin)) is not None:
                self.player.texture = pygame.image.load(x)
                self.player.texture = pygame.transform.scale(self.player.texture,
                                                             (self.player.width, self.player.height))

        self.win.blit(com.render("B = BACK      P = PURCHASE/SELECT", True, "white"),
                      (50, self.height - (com_size + 10)))

    def asteroid_scene(self, keys) -> None:
        self.win.blit(title.render("ASTEROIDS", True, "white"), (self.width / 2 - title_size * 4, title_size))
        self.coin.read()
        self.win.blit(com.render(str(self.coin.coin), True, "white"), (self.width - self.width / 10, title_size * 1.5))
        load_coin(self.win, self.width - self.width / 10 + 100, title_size * 1.4)
        for i in self.shop.asteroids:
            if (x := i.draw(keys, self.coin)) is not None:
                Utils.asteroid_str = x

        self.win.blit(com.render("B = BACK      P = PURCHASE/SELECT", True, "white"),
                      (50, self.height - (com_size + 10)))

    def command(self, keys, mouse: int = 0):
        if self.opt == SHOP.BG or self.opt == SHOP.SP_SHIP or self.opt == SHOP.ASTEROID:
            if keys[pygame.K_b]:
                self.opt = SHOP.DEFAULT
                self.mode = MODE.SHOP
        if self.mode == MODE.MENU:
            if keys[pygame.K_w]:
                if self.line != 0:
                    self.line -= 1
                else:
                    self.line = 3
            elif keys[pygame.K_s]:
                if self.line != 3:
                    self.line += 1
                else:
                    self.line = 0
            if keys[pygame.K_SPACE]:
                self.mode = int_to_mode(self.line)
        elif self.mode == MODE.SHOP:
            if keys[pygame.K_w]:
                if self.line != 0:
                    self.line -= 1
                else:
                    self.line = 3
            elif keys[pygame.K_s]:
                if self.line != 3:
                    self.line += 1
                else:
                    self.line = 0
            elif keys[pygame.K_SPACE]:
                self.mode = MODE.DEFAULT
                self.opt = int_to_option(self.line)
                # print(self.opt, self.mode)
        elif self.mode == MODE.SIMPLE or self.mode == MODE.MEDIUM or self.mode == MODE.HARD:
            if keys[pygame.K_b]:
                self.mode = MODE.MENU
                self.coin.write(self.coin.coin)
            if mouse == 1:
                # SPAWN BULLET
                mouse_x, mouse_y = pygame.mouse.get_pos()

                distance_x = mouse_x - self.player.position.x
                distance_y = mouse_y - self.player.position.y

                angle = math.atan2(distance_y, distance_x)

                speed_x = 20 * math.cos(angle)
                speed_y = 20 * math.sin(angle)

                self.em.add(Bullet(self.win, vec2(self.player.position.x + self.player.width / 2,
                                                  self.player.position.y + self.player.height / 2),
                                   vec2(speed_x, speed_y), 52, angle))

    def load_shop(self) -> None:
        for i in range(3):
            self.shop.bgs.append(
                Item(self.win, vec2(430 * (i + 1), self.height / 2 - 110), "Texture/bg" + str(i + 1) + ".jpg",
                     str(5000 + (i * 1150))))

        for i in range(5):
            self.shop.spaceships.append(
                Item(self.win, vec2(290 * (i + 1), self.height / 2 - 110), "Texture/sships/spaceship" + str(i) + ".png",
                     str(7000 + (i * 750))))

        for i in range(3):
            self.shop.asteroids.append(
                Item(self.win, vec2(430 * (i + 1), self.height / 2 - 110), "Texture/asteroid/as" + str(i + 1) + ".png",
                     str(8000 + (i * 560))))

    def render(self) -> None:

        clock = pygame.time.Clock()

        self.load_shop()

        mouse: int = 0
        while self.run:
            bg = pygame.transform.scale(self.bg, (1920, 1080))
            # BLACK: tuple = (0, 0, 0)
            # self.win.fill(BLACK)
            clock.tick(60)
            # Set Background
            self.win.blit(bg, (0, 0))

            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse = 1
                else:
                    mouse = 0
                if event.type == pygame.QUIT:
                    self.run = False
                if keys[pygame.K_ESCAPE]:
                    # file = open("coin.txt","w")
                    # file.write(str(self.coin))
                    # file.close()
                    self.coin.write(self.coin.coin)
                    self.run = False
                self.command(keys, mouse)

            if self.mode == MODE.MENU:
                self.menu_scene()
            elif self.mode == MODE.SHOP:
                self.shop_scene()
            else:
                if self.opt == SHOP.BACK:
                    self.mode = MODE.MENU
                    self.opt = SHOP.DEFAULT
                elif self.opt == SHOP.BG:
                    self.bg_scene(keys)
                elif self.opt == SHOP.SP_SHIP:
                    self.spaceship_scene(keys)
                elif self.opt == SHOP.ASTEROID:
                    self.asteroid_scene(keys)
                elif self.mode == MODE.SIMPLE or self.mode == MODE.MEDIUM or self.mode == MODE.HARD:
                    self.game_scene(keys)

            pygame.display.update()
