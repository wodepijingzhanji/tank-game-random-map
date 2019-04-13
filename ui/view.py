import pygame
from ui.locals import *
from ui.action import *
import time
import random


class PlayerTank(Display, Move, Block, Destroy, Beaten):
    playerNum = 0
    maxNum = 2

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        # surface
        self.surface = kwargs["surface"]
        PlayerTank.playerNum += 1
        # self.id=PlayerTank.playerNum
        if PlayerTank.playerNum > PlayerTank.maxNum:
            PlayerTank.playerNum = 1
        self.reset("img/p{}tank".format(PlayerTank.playerNum), hp=kwargs["hp"])
        print(PlayerTank.playerNum)

    def get_hp(self):
        return self.hp

    def is_destroyed(self):
        return self.hp <= 0

    def receive_beaten(self, power):
        """power 打我者的杀伤力"""
        if not self.invincible:
            self.hp -= power
        if self.hp < 0:
            self.hp = 0

    def display_destroy(self):
        x = self.x + self.width / 2
        y = self.y + self.height / 2
        if not isinstance(self, EnemyTank):
            PlayerTank.playerNum -= 1
            print(PlayerTank.playerNum)
        return Blast(x=x, y=y, surface=self.surface)

    def reset(self, nameL, hp):
        self.invincible = False  # 当self.invincible为True时，玩家无敌（被子弹打中不掉血）
        self.isDestroyed = False  # 坦克被摧毁的标志
        self.images = [
            pygame.image.load(nameL + 'U.gif'),
            pygame.image.load(nameL + 'D.gif'),
            pygame.image.load(nameL + 'L.gif'),
            pygame.image.load(nameL + 'R.gif')
        ]
        self.direction = Direction.UP
        # speed
        self.speed = 4
        # 错误的方向
        self.bad_direction = Direction.NONE
        # width,height
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.bullets = []
        self.__fire_start = 0
        self.__fire_delay = 0.4
        self.__move_start = 0
        self.__move_delay = 0.03
        self.hp = hp

    def display(self):
        image = None
        if self.direction == Direction.UP:
            image = self.images[0]
        elif self.direction == Direction.DOWN:
            image = self.images[1]
        elif self.direction == Direction.LEFT:
            image = self.images[2]
        elif self.direction == Direction.RIGHT:
            image = self.images[3]

        self.surface.blit(image, (self.x, self.y))

    def move(self, direction):
        """移动"""
        now = time.time()
        if now - self.__move_start < self.__move_delay:
            return
        self.__move_start = now

        # 如果当前的方向和要去走的方向是不同的
        # 1. 只是转方向
        # 2. 转方向+移动
        # 如果是错误的方向就不移动了
        if direction == self.bad_direction:
            return

        if self.direction != direction:
            # 1.只是转方向
            # 改变方向
            self.direction = direction
        else:
            # 方向相同
            if direction == Direction.UP:
                self.y -= self.speed
                if self.y < 0:
                    self.y = 0
            elif direction == Direction.DOWN:
                self.y += self.speed
                if self.y > GAME_HEIGHT - self.height:
                    self.y = GAME_HEIGHT - self.height
            elif direction == Direction.LEFT:
                self.x -= self.speed
                if self.x < 0:
                    self.x = 0
            elif direction == Direction.RIGHT:
                self.x += self.speed
                if self.x > GAME_WIDTH - self.width:
                    self.x = GAME_WIDTH - self.width

    def fire(self, missile='img/tankmissile.gif'):
        now = time.time()

        if now - self.__fire_start < self.__fire_delay:
            return None
        self.__fire_start = now

        # print("fire")
        # 创建子弹
        x = 0
        y = 0
        if self.direction == Direction.UP:
            x = self.x + self.width / 2
            y = self.y
        elif self.direction == Direction.DOWN:
            x = self.x + self.width / 2
            y = self.y + self.height
        elif self.direction == Direction.LEFT:
            x = self.x
            y = self.y + self.height / 2
        elif self.direction == Direction.RIGHT:
            x = self.x + self.width
            y = self.y + self.height / 2
        return Bullet(x=x, y=y, direction=self.direction, surface=self.surface, missile=missile)

    def isEat(self, prop):
        '''判断坦克是否吃到符'''
        return self.get_rect().colliderect(prop.get_rect())

    def is_blocked(self, block):
        # 判断坦克和墙是否碰撞

        # 判断坦克下一步的矩形和现在的墙是否碰撞
        next_x = self.x
        next_y = self.y

        if self.direction == Direction.UP:
            next_y -= self.speed
            if next_y < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.DOWN:
            next_y += self.speed
            if next_y > GAME_HEIGHT - self.height:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.LEFT:
            next_x -= self.speed
            if next_x < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.RIGHT:
            next_x += self.speed
            if next_x > GAME_WIDTH - self.width:
                self.bad_direction = self.direction
                return True

        # 矩形和矩形的碰撞, 当前矩形
        rect_self = pygame.Rect(next_x, next_y, self.width, self.height)
        rect_wall = pygame.Rect(block.x, block.y, block.width, block.height)

        collide = pygame.Rect.colliderect(rect_self, rect_wall)
        if collide:
            # 碰撞了,当的方向是错误的方向
            self.bad_direction = self.direction
            return True
        else:
            # 没有错误方向
            self.bad_direction = Direction.NONE
            return False


class Wall(Display, Block, Destroy, Beaten):

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.image = pygame.image.load("img/walls.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # 生命值
        self.hp = 5

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_hp(self):
        return self.hp

    def receive_beaten(self, power):
        """power 打我者的杀伤力"""
        self.hp -= power

    def is_destroyed(self):
        return self.hp <= 0

    def display_destroy(self):
        x = self.x + self.width / 2
        y = self.y + self.height / 2
        return Blast(x=x, y=y, surface=self.surface)


class Eagle(Wall):
    """鹰"""

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.image = pygame.image.load("img/camp.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # 生命值
        self.hp = 20
        self.invincible = False

    def receive_beaten(self, power):
        """power 打我者的杀伤力"""
        if not self.invincible:
            self.hp -= power
        if self.hp < 0:
            self.hp = 0


class Armor(Wall):
    '''鹰的护甲'''

    def __init__(self, **kwargs):
        self.invincible = False
        self.ceter_x = kwargs["x"]
        self.ceter_y = kwargs["y"]
        self.image = pygame.image.load("img/steel.gif")
        self.image_width = self.image.get_width()
        self.image_height = self.image.get_height()
        self.surface = kwargs["surface"]
        self.numbers = kwargs["numbers"]
        self.positions = []  # 小墙坐标
        self.ceters = []  # 鹰周围不超过八块的区域的中心，护甲被摧毁后可以生成符文时需要用到这个参数
        for number in self.numbers:
            if number == '一':
                self.positions.append(
                    (self.ceter_x - BLOCK / 2 - self.image_width, self.ceter_y - BLOCK / 2 - self.image_height))
                self.ceters.append((self.ceter_x - BLOCK, self.ceter_y - BLOCK))
            if number == '二':
                self.positions.append((self.ceter_x - BLOCK / 2, self.ceter_y - BLOCK / 2 - self.image_height))
                self.positions.append((self.ceter_x, self.ceter_y - BLOCK / 2 - self.image_height))
                self.ceters.append((self.ceter_x, self.ceter_y - BLOCK))
            if number == '三':
                self.positions.append((self.ceter_x + BLOCK / 2, self.ceter_y - BLOCK / 2 - self.image_height))
                self.ceters.append((self.ceter_x + BLOCK, self.ceter_y - BLOCK))
            if number == '四':
                self.positions.append((self.ceter_x + BLOCK / 2, self.ceter_y - BLOCK / 2))
                self.positions.append((self.ceter_x + BLOCK / 2, self.ceter_y))
                self.ceters.append((self.ceter_x + BLOCK, self.ceter_y ))
            if number == '五':
                self.positions.append((self.ceter_x + BLOCK / 2, self.ceter_y + BLOCK / 2))
                self.ceters.append((self.ceter_x + BLOCK, self.ceter_y + BLOCK))
            if number == '六':
                self.positions.append((self.ceter_x, self.ceter_y + BLOCK / 2))
                self.positions.append((self.ceter_x - BLOCK / 2, self.ceter_y + BLOCK / 2))
                self.ceters.append((self.ceter_x, self.ceter_y + BLOCK))
            if number == '七':
                self.positions.append((self.ceter_x - BLOCK / 2 - self.image_width, self.ceter_y + BLOCK / 2))
                self.ceters.append((self.ceter_x - BLOCK, self.ceter_y + BLOCK))
            if number == '八':
                self.positions.append((self.ceter_x - BLOCK / 2 - self.image_width, self.ceter_y))
                self.positions.append((self.ceter_x - BLOCK / 2 - self.image_width, self.ceter_y - BLOCK / 2))
                self.ceters.append((self.ceter_x - BLOCK, self.ceter_y))
        self.x = min([position[0] for position in self.positions])
        self.y = min([position[1] for position in self.positions])
        # print(self.numbers)
        # print(self.positions)
        self.width = max([position[0] for position in self.positions]) - min(
            [position[0] for position in self.positions]) + self.image_width
        self.height = max([position[1] for position in self.positions]) - min(
            [position[1] for position in self.positions]) + self.image_height
        # 生命值
        self.hp = 20

    def display(self):
        for position in self.positions:
            self.surface.blit(self.image, (position[0], position[1]))

    def receive_beaten(self, power):
        """power 打我者的杀伤力"""
        if not self.invincible:
            self.hp -= power
        if self.hp < 11:
            self.image = pygame.image.load("img/wall.gif")
        if self.hp < 0:
            self.hp = 0


class Steel(Display, Block, Beaten):
    """铁墙"""

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.image = pygame.image.load("img/steels.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hp = 1000

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_hp(self):
        self.hp += 10
        return self.hp

    def receive_beaten(self, power):
        pass


class Water(Display, Block):
    """水"""

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.image = pygame.image.load("img/water.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class Grass(Display, Order):
    """丛林"""

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.image = pygame.image.load("img/grass.png")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_order(self):
        return 100


class Timer(Display, Order, Destroy):
    """静止器/加时符"""

    def is_destroyed(self):
        return self.__is_destroyed

    def setDestroyed(self):
        self.__is_destroyed = True

    def __init__(self, **kwargs):
        self.image = pygame.image.load("img/timer.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2
        # 是否回收的状态
        self.__is_destroyed = False

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_order(self):
        return 200


class BlowUp(Display, Order, Destroy):
    """爆炸符"""

    def is_destroyed(self):
        return self.__is_destroyed

    def setDestroyed(self):
        self.__is_destroyed = True

    def __init__(self, **kwargs):
        self.image = pygame.image.load("img/bomb.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2
        # 是否回收的状态
        self.__is_destroyed = False

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_order(self):
        return 300


class Star(Display, Order, Destroy):
    """无敌符"""

    def is_destroyed(self):
        return self.__is_destroyed

    def setDestroyed(self):
        self.__is_destroyed = True

    def __init__(self, **kwargs):
        self.image = pygame.image.load("img/star.gif")
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2
        # 是否回收的状态
        self.__is_destroyed = False

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_order(self):
        return 400


class Bullet(Display, AutoMove, Destroy, Attack):

    def __init__(self, **kwargs):
        self.image = pygame.image.load(kwargs["missile"])
        self.surface = kwargs["surface"]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = kwargs["direction"]
        self.speed = 5
        # x,y
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2
        if self.direction == Direction.UP:
            self.y -= self.height / 2
        elif self.direction == Direction.DOWN:
            self.y += self.height / 2
        elif self.direction == Direction.LEFT:
            self.x -= self.width / 2
        elif self.direction == Direction.RIGHT:
            self.x += self.width / 2
        # 是否回收的状态
        self.__is_destroyed = False
        # 杀伤力
        self.power = 4

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def move(self):
        # 方向相同
        if self.direction == Direction.UP:
            self.y -= self.speed
            if self.y < - self.height:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.DOWN:
            self.y += self.speed
            if self.y > GAME_HEIGHT:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
            if self.x < - self.width:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
            if self.x > GAME_WIDTH:
                self.x = GAME_WIDTH - self.width
                # 出屏幕了，回收
                self.__is_destroyed = True

    def is_blocked(self, block):
        pass

    def is_destroyed(self):
        if self.power <= 0:
            return True
        return self.__is_destroyed

    def get_attack_power(self):
        return self.power

    def receive_attack(self, hp):
        """hp 被打者的生命值"""
        self.power -= hp


class Blast(Display, Destroy):

    def __init__(self, **kwargs):
        self.surface = kwargs["surface"]

        self.images = []
        for i in range(1, 33):
            self.images.append(pygame.image.load("img/blast_%d.png" % i))
        self.index = 0

        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        # x,y
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2

    def display(self):
        if self.index >= len(self.images):
            return

        image = self.images[self.index]
        self.surface.blit(image, (self.x, self.y))
        self.index += 1

    def is_destroyed(self):
        return self.index >= len(self.images)


class Born(Display, Destroy, Block):
    '''敌军诞生动画'''

    def __init__(self, **kwargs):
        self.surface = kwargs["surface"]

        self.images = []
        for i in range(1, 5):
            self.images.append(pygame.image.load("img/born%d.gif" % i))
        self.index = 0

        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        # x,y
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2

    def display(self):
        if self.index >= len(self.images):
            return
        if random.randint(1, 50) == 1:
            image = self.images[self.index]
            self.surface.blit(image, (self.x, self.y))
            self.index += 1

    def is_destroyed(self):
        return self.index >= len(self.images)


class EnemyTank(PlayerTank, AutoMove, AutoFire):
    def __init__(self, **kwargs):
        EnemyTank.maxNum = 3
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        # surface
        self.surface = kwargs["surface"]
        EnemyTank.playerNum += 1
        # self.id=PlayerTank.playerNum
        if EnemyTank.playerNum > EnemyTank.maxNum:
            EnemyTank.playerNum = 1
        self.reset("img/enemy{}".format(EnemyTank.playerNum), hp=kwargs["hp"])

    def display(self):
        super().display()

    def move(self, d=Direction.NONE):
        """自动移动"""
        if self.bad_direction != self.direction and random.randint(1, 5) == 1:
            super().move(self.direction)
        if random.randint(1, 50) == 1:
            super().move(random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]))
