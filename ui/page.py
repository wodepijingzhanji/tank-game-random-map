from pygame.locals import *
from ui.container import *
from ui.locals import *
import pygame

# 0代表start页面1代表game页面
__current = 1


def getCurrent():
    return __current


def setCurrent(value):
    global __current
    __current = value


class StartPage:
    def __init__(self, surface):
        self.surface = surface

    def graphic(self):
        """渲染"""
        self.surface.fill((0xff, 0x00, 0x00))

    def keydown(self, key):
        """按下事件"""
        print(key)
        if key == K_RETURN:
            # 显示game
            setCurrent(1)

    def keypress(self, keys):
        """长按事件"""
        pass


class GamePage:
    def __init__(self, surface):
        # 暂停标记
        self.pause = False
        self.surface = surface
        self.gameSurface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.infoSurface = pygame.Surface((INFO_WIDTH, INFO_HEIGHT))
        self.reset()

        # 文字
        self.noticeFont = pygame.font.Font("./font/happy.ttf", 50)
        self.tongJiFont = pygame.font.Font("./font/happy.ttf", 16)
        self.text1 = self.noticeFont.render('游戏结束', True, (255, 0, 0))
        self.text2 = self.noticeFont.render('点击Enter重新开始', True, (255, 0, 0))
        self.text3 = self.noticeFont.render('您胜利了', True, (255, 0, 0))

    def reset(self):
        self.gameContainer = GameContainer(self.gameSurface)
        self.infoContainer = InfoContainer(self.infoSurface)

        # 游戏信息存储变量
        self.setXinXi()

    def setXinXi(self):
        self.__xinXi = self.gameContainer.getXinXi()

    def switchPause(self):
        self.pause = not self.pause

    def graphic(self):
        """渲染"""
        if self.pause:
            pass
        else:
            self.surface.fill((0x77, 0x77, 0x77))

            self.setXinXi()
            if self.__xinXi['Game Over']:
                self.surface.blit(self.text1, (260, 280))
                self.surface.blit(self.text2, (150, 350))
            elif self.__xinXi['剩余敌军'] < 1 and self.__xinXi['敌军数量'] < 1:
                self.surface.blit(self.text3, (260, 280))
                self.surface.blit(self.text2, (150, 350))
            else:
                # 渲染游戏区
                self.surface.blit(self.gameSurface, (WINDOW_PADDING, WINDOW_PADDING))
                self.gameContainer.graphic()

            # 渲染信息区
            self.surface.blit(self.infoSurface, (2 * WINDOW_PADDING + GAME_WIDTH, WINDOW_PADDING))
            self.infoContainer.graphic(self.__xinXi)

    def keydown(self, key):
        """按下事件"""
        if self.__xinXi['Game Over'] or (self.__xinXi['剩余敌军'] < 1):
            if key == pygame.K_RETURN:
                self.reset()
        else:
            if key == pygame.K_SPACE:
                self.switchPause()
            else:
                if not self.pause:
                    self.gameContainer.keydown(key)

    def keypress(self, keys):
        """长按事件"""
        if self.__xinXi['Game Over'] or (self.__xinXi['剩余敌军'] < 1):
            if keys[K_RETURN]:
                self.reset()
        else:
            if not self.pause:
                self.gameContainer.keypress(keys)
        # 试验
        # else :
        #     if keys[K_SPACE]:
        #         self.switchPause()
        #     else:
        #         self.gameContainer.keypress(keys)
