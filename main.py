"""
创建窗体
"""

import pygame
import sys
from pygame.locals import *
from ui.locals import *
from ui.page import *

if __name__ == '__main__':
    pygame.init()

    h = 11 * 60
    w = int(h * 1044 / 796)

    # 窗体
    window = pygame.display.set_mode((w, h))
    screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    # print(WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_caption("坦克大战")

    # 两个页面
    start = StartPage(screen)
    game = GamePage(screen)

    while True:
        current = getCurrent()
        # 判断页面
        page = None
        if current == 0:
            page = start
        elif current == 1:
            page = game

        # 渲染页面
        page.graphic()

        pygame.transform.scale(screen, (w, h), window)
        pygame.display.flip()

        events = pygame.event.get()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == KEYDOWN:
                # 为页面传递事件
                page.keydown(event.key)

        keys = pygame.key.get_pressed()
        # 为页面传递事件
        page.keypress(keys)
