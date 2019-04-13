from abc import *

# abstract class
from abc import ABC
import pygame

from ui.locals import Direction

"""
1. 导入模块
2. 类中metaclass=ABCMeta
3. @abstractmethod修饰方法
"""


class Display(metaclass=ABCMeta):
    """
    抽象类：规范显示行为
    """

    @abstractmethod
    def display(self):
        """显示"""
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Move(metaclass=ABCMeta):
    """移动的规范"""

    @abstractmethod
    def move(self, direction=Direction.NONE):
        pass

    @abstractmethod
    def is_blocked(self, block):
        pass


class Block(metaclass=ABCMeta):
    """阻塞的规范"""
    pass


class Order(metaclass=ABCMeta):
    """排序显示"""

    @abstractmethod
    def get_order(self):
        pass


class AutoMove(Move, ABC):
    """自动移动"""
    pass


class AutoFire(Move, ABC):
    """自动移动"""
    pass


class Destroy(metaclass=ABCMeta):
    """回收的规范"""

    @abstractmethod
    def is_destroyed(self):
        pass

    def display_destroy(self):
        return None


class Attack(metaclass=ABCMeta):
    """攻击能力"""

    def is_attacked(self, beaten):
        # 矩形和矩形的碰撞, 当前矩形
        return pygame.Rect.colliderect(self.get_rect(), beaten.get_rect())

    @abstractmethod
    def get_attack_power(self):
        pass

    @abstractmethod
    def receive_attack(self, hp):
        pass


class Beaten(metaclass=ABCMeta):
    """挨打的能力"""

    @abstractmethod
    def get_hp(self):
        pass

    @abstractmethod
    def receive_beaten(self, power):
        pass
