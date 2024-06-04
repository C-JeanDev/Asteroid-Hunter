from Utils import *
import rsa

(pub, priv) = rsa.newkeys(512)


class Coin:

    def __init__(self):
        self.coin = None
        self.read()

    def read(self) -> int:
        file = open("game_saves/coin.txt", "r")
        self.coin = int(str(file.read()).replace('\n', ''))
        file.close()

    def write(self, x):
        file = open("game_saves/coin.txt", "w")
        file.write(str(x))
        file.close()

class Shop:

    def __init__(self):
        self.spaceships: list = []
        self.bgs: list = []
        self.asteroids: list = []


class Item:

    def __init__(self, win, position: vec2, texture: str ,price: str):
        self.win = win
        self.position: vec2 = position
        self.str_texture: str = texture
        self.price: str = price
        self.purchased: bool = False
        self.texture_str: str = texture
        self.texture = pygame.image.load(texture).convert_alpha()
        self.texture = pygame.transform.scale(self.texture, (200, 200))
        self.rect = self.texture.get_rect()
        self.rect.width = 220
        self.rect.width = 220
        self.upload()

    def upload(self) -> None:
        file = open("game_saves/purchased.txt", "r")
        # print(type(file.read()))
        purchased: list = []
        for i in file:
            purchased.append(i.replace('\n',''))
        if self.texture_str in purchased:
            self.purchased = True
        file.close()

    def handle_item(self, keys, coin) -> str | None:
            if keys[pygame.K_p] and self.purchased:
                self.win.blit(com.render("Selected", True, "green"), (self.position.x, self.position.y - 70))
                return self.str_texture
            elif self.purchased:
                self.win.blit(com.render("Purchased", True, "green"), (self.position.x, self.position.y - 70))
            else:
                if keys[pygame.K_p]:
                    if coin.coin < int(self.price):
                        self.win.blit(com.render("Not enough money", True, "red"),
                                      (self.position.x, self.position.y - 70))
                    elif coin.coin > int(self.price):
                        coin.write(coin.coin - int(self.price))
                        coin.read()
                        self.purchased = True
                        self.win.blit(com.render("Purchased", True, "green"), (self.position.x, self.position.y - 70))
                        file = open("game_saves/purchased.txt", "a")
                        file.write(self.texture_str+'\n')
                        file.close()
                        return self.str_texture


    def draw(self, keys,coin: Coin) -> str | None:
        mx, my = pygame.mouse.get_pos()
        color = (255, 255, 255)
        if self.position.x < mx < self.position.x + self.rect.width and self.position.y < my < self.position.y+self.rect.height:
            color = (123,123,123)
            if (x := self.handle_item(keys,coin)) is not None:
                return x

        # Border
        for i in range(4):
            pygame.draw.rect(self.win, color, (self.position.x - i - 10, self.position.y - i - 10, self.rect.width + 5, self.rect.width + 5), 4)

        self.win.blit(com.render(self.price, True, "white"),(self.position.x + self.rect.width / 4, self.position.y + self.rect.width + 20))

        self.win.blit(self.texture, self.rect)
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        return None