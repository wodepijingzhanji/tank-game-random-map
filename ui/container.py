from ui.view import *
from pygame.locals import *
from util_.util_ import *


class GameContainer:
    """

    """

    # 1. 可以通过列表去管理所有的显示元素
    # 2.

    def __init__(self, surface):
        self.startTime = time.perf_counter()  # 计时开始
        self.nowTime = self.startTime
        self.timelimit = 180
        self.props = []
        self.obtainProps = {'静止符': False, '加时符': False, '爆炸符': False, '防弹符': False}
        self.surface = surface
        self.views = []
        self.displays = []
        self.positionEs = []
        self.positionEa = ()
        self.positionAirs = []  # 符文诞生地
        self.numbers = []
        # 随机生成一个地图
        self.mapTB = MapTB()
        print(self.mapTB.getName())
        f = open('./map/' + self.mapTB.getName(), 'w', encoding='UTF-8')
        f.write(str(self.mapTB))
        f.close()
        m = self.mapTB.map
        for row, line in enumerate(m):
            texts = line
            for column, text in enumerate(texts):
                # print("row:{} column:{} text:{}".format(row, column, text))
                x = column * BLOCK
                y = row * BLOCK
                if text == "砖":
                    self.views.append(Wall(surface=self.surface, x=x, y=y))
                if text == "铁":
                    self.views.append(Steel(surface=self.surface, x=x, y=y))
                if text == "水":
                    self.views.append(Water(surface=self.surface, x=x, y=y))
                if text == "草":
                    self.views.append(Grass(surface=self.surface, x=x, y=y))
                    self.positionAirs.append((x + BLOCK / 2, y + BLOCK / 2))
                if text == '空':
                    self.positionAirs.append((x + BLOCK / 2, y + BLOCK / 2))
                if text == "主":
                    self.player1 = PlayerTank(surface=self.surface, x=x, y=y, hp=20)
                    self.views.append(self.player1)
                    self.positionAirs.append((x + BLOCK / 2, y + BLOCK / 2))
                if text == "副":
                    self.player2 = PlayerTank(surface=self.surface, x=x, y=y, hp=20)
                    self.views.append(self.player2)
                    self.positionAirs.append((x + BLOCK / 2, y + BLOCK / 2))
                if text == '敌':
                    self.positionEs.append((x, y))
                    self.positionAirs.append((x + BLOCK / 2, y + BLOCK / 2))
                if text == '鹰':
                    self.eagle = Eagle(surface=self.surface, x=x, y=y)
                    self.views.append(self.eagle)
                    self.positionEa = (x + BLOCK / 2, y + BLOCK / 2)
                # if ' 一二三四五六七八'.find(text):
                # #注意字符串的find函数当在索引为0的位置找到text时会返回0，而被当成False处理，所以' 一二三四五六七八'前面加了空格来避免此bug
                if text in '一二三四五六七八':
                    # if '一' == text \
                    #         or '二' == text \
                    #         or '三' == text \
                    #         or '四' == text \
                    #         or '五' == text \
                    #         or '六' == text \
                    #         or '七' == text \
                    #         or '八' == text:
                    self.numbers.append(text)
        # 创建老鹰（基地）的护甲
        self.armor = Armor(surface=self.surface, x=self.positionEa[0], y=self.positionEa[1], numbers=self.numbers)
        self.views.append(self.armor)
        # 重置信息
        self.resetXinXi()

    def __sort(self, view):
        # if isinstance(view, Order):
        #     return view.get_order()
        # else:
        #     return 0
        return view.get_order() if isinstance(view, Order) else 0

    def getXinXi(self):
        return self.__XinXi

    def resetXinXi(self):
        self.__XinXi = {'Game Over': False, \
                        '玩家数量': 0, \
                        "敌军数量": 0, \
                        '鹰死亡': False, \
                        '剩余敌军': 20, \
                        '敌军军营': self.mapTB.enemyNum, \
                        '剩余时间': self.timelimit - time.perf_counter(), \
                        '玩家无敌': '否', \
                        '玩家1血量': self.player1.get_hp(), \
                        '玩家2血量': self.player2.get_hp(), \
                        '基地血量': self.eagle.get_hp(), \
                        '护甲血量': self.armor.get_hp()}

    def resetNumbers(self):
        self.__XinXi['玩家数量'] = 0
        self.__XinXi["敌军数量"] = 0

    def graphic(self):
        """渲染"""
        # 剩余时间计算
        self.nowTime = time.perf_counter()
        self.__XinXi['剩余时间'] = self.timelimit - (self.nowTime - self.startTime)
        if self.__XinXi['剩余时间'] < 0:
            self.__XinXi['剩余时间'] = 0
            self.__XinXi['Game Over'] = True
        # 获取玩家血量
        self.__XinXi['玩家1血量'] = self.player1.get_hp()
        self.__XinXi['玩家2血量'] = self.player2.get_hp()
        self.__XinXi['基地血量'] = self.eagle.get_hp()
        if self.armor:
            self.__XinXi['护甲血量'] = self.armor.get_hp()
        # 一定概率重置静止符
        if random.randint(1, 1000) == 1:
            self.obtainProps['静止符'] = False
        # 一定概率重置防弹符
        if random.randint(1, 2000) == 1:
            self.obtainProps['防弹符'] = False
            self.__XinXi['玩家无敌'] = '否'
            self.armor.invincible = False
            self.eagle.invincible = False
            for player in self.views:
                if isinstance(player, PlayerTank) and (not isinstance(player, EnemyTank)):
                    player.invincible = False
        self.obtainProps[random.choice(['防弹符'])] = False
        # 利用类属性获取玩家数量
        if PlayerTank.playerNum < 1:
            self.__XinXi['Game Over'] = True
        # 重新计算玩家和敌军数量
        self.resetNumbers()
        # 统计各种view数量
        haveEagle = False
        for view in self.views:
            if isinstance(view, PlayerTank) and not isinstance(view, EnemyTank):
                self.__XinXi['玩家数量'] += 1
            if isinstance(view, EnemyTank) or isinstance(view, Born):
                self.__XinXi['敌军数量'] += 1
            if isinstance(view, Eagle):
                haveEagle = True
        else:
            self.__XinXi['鹰死亡'] = not haveEagle
        if self.__XinXi['鹰死亡']:
            self.__XinXi['Game Over'] = True
        # 清屏
        self.surface.fill((0x00, 0x00, 0x00))

        # 制造道具
        if random.randint(1, 100) == 1:
            n = random.randint(0, len(self.positionAirs) - 1)
            x = self.positionAirs[n][0]
            y = self.positionAirs[n][1]
            aProp = random.choice(['Timer', 'BlowUp', 'Star'])
            prop = eval(aProp)(x=x, y=y, surface=self.surface)
            for oldProp in self.props:
                if prop.get_rect().colliderect(oldProp.get_rect()):
                    oldProp.setDestroyed()
                    self.props.remove(oldProp)
            self.views.append(prop)
            self.props.append(prop)
        # 制造敌方坦克
        if random.randint(1, 200) == 1:
            n = random.randint(0, len(self.positionEs) - 1)
            x = self.positionEs[n][0]
            y = self.positionEs[n][1]
            for block in self.views:
                vRect = pygame.Rect(block.x, block.y, block.width, block.height)
                if vRect.colliderect(pygame.Rect(x, y, BLOCK, BLOCK)) and isinstance(block, Block):
                    # if block.get_rect().colliderect(pygame.Rect(x, y, BLOCK, BLOCK)) and isinstance(block, Block):    #利用Display的get_rect()方法更简介
                    break
            else:
                if self.getXinXi()['敌军数量'] < 6 and self.getXinXi()['敌军数量'] < self.getXinXi()['剩余敌军']:
                    born = Born(x=x + BLOCK / 2, y=y + BLOCK / 2, surface=self.surface)
                    self.views.append(born)

        # 对列表进行排序，排序的标准
        # self.views.sort(key=lambda view: view.get_order() if isinstance(view, Order) else 0)
        self.views.sort(key=self.__sort)
        # self.views = sorted(self.views,key=self.__sort)
        # print(len(self.views))

        # 判断玩家是否吃到辅助道具
        for player in self.views[:]:
            if isinstance(player, PlayerTank) and (not isinstance(player, EnemyTank)):
                for prop in self.props[:]:
                    if player.isEat(prop):
                        if isinstance(prop, Timer):
                            self.obtainProps[random.choice(['静止符', '加时符'])] = True
                            if self.obtainProps['加时符']:
                                self.timelimit += 30
                                self.obtainProps['加时符'] = False
                                print('吃到加时符')
                            else:
                                print('吃到静止符')
                            prop.setDestroyed()
                            self.props.remove(prop)
                        elif isinstance(prop, BlowUp):
                            print('吃到爆炸符')
                            self.obtainProps['爆炸符'] = True
                            prop.setDestroyed()
                            self.props.remove(prop)
                            for enemyTank in self.views:
                                if isinstance(enemyTank, EnemyTank):
                                    enemyTank.hp = 0
                            self.obtainProps['爆炸符'] = False
                        elif isinstance(prop, Star):
                            print('吃到防弹符')
                            self.obtainProps['防弹符'] = True
                            self.__XinXi['玩家无敌'] = '是'
                            self.armor.invincible = True
                            self.eagle.invincible = True
                            for anotherPlayer in self.views:
                                if isinstance(anotherPlayer, PlayerTank) and (not isinstance(anotherPlayer, EnemyTank)):
                                    anotherPlayer.invincible = True
                            prop.setDestroyed()
                            self.props.remove(prop)

        # 判断物体是否需要回收
        for view in list(self.views):
            if isinstance(view, Destroy) and view.is_destroyed():
                self.views.remove(view)
                if isinstance(view, PlayerTank) and (not isinstance(view, EnemyTank)):
                    self.getXinXi()['玩家数量'] -= 1
                if isinstance(view, EnemyTank):
                    self.getXinXi()['剩余敌军'] -= 1
                    self.getXinXi()['敌军数量'] -= 1
                if isinstance(view, Born):
                    self.views.append(EnemyTank(surface=self.surface, x=view.x, y=view.y, hp=6))
                if isinstance(view, Armor):
                    self.positionAirs.extend(view.ceters)
                elif isinstance(view, Wall):
                    self.positionAirs.append((view.x + BLOCK / 2, view.y + BLOCK / 2))
                self.__add_view(view.display_destroy())

        # 遍历列表，让所有的元素显示
        for view in self.views:
            view.display()

        # 判断墙和坦克是否发生碰撞
        # 判断 可移动的物体 是否和 可阻挡移动的物体 发生了碰撞
        # for view in self.views:
        #     if isinstance(view, Wall):
        #         # 墙
        #         if self.player.is_blocked(view):
        #             # 墙和坦克碰撞
        #             break

        # for block in self.views:
        #     # 找出所有可阻塞移动的物体
        #     if isinstance(block, Block):
        #         for move in self.views:
        #             if isinstance(move, Move):
        #                 if move.is_blocked(block):
        #                     # 移动的物体被阻塞的物体挡住了
        #                     break

        # 移动和阻塞的碰撞检测
        for move in self.views:
            if isinstance(move, Move):
                for block in self.views:
                    # 找出所有可阻塞移动的物体
                    if isinstance(block, Block) and move != block:
                        if move.is_blocked(block):
                            # 移动的物体被阻塞的物体挡住了
                            break

        # 具备自动移动的物体，让他自己移动
        for autoMove in self.views:
            if isinstance(autoMove, AutoMove):
                if isinstance(autoMove, EnemyTank) and self.obtainProps['静止符']:
                    continue
                autoMove.move()
        # 具备自动发子弹的物体，让他自己发子弹
        for autoFire in self.views:
            if self.obtainProps['静止符']:
                continue
            if isinstance(autoFire, AutoFire) and random.randint(1, 50) == 1:
                self.__add_view(autoFire.fire(missile='img/enemymissile.gif'))
        # 子弹和砖墙的碰撞
        # for bullet in self.views:
        #     if isinstance(bullet, Bullet):
        #         for wall in self.views:
        #             if isinstance(wall, Wall) and bullet.is_blocked(wall):
        #                 # 判断子弹和墙是否发生碰撞
        #
        #                 # 根据子弹的杀伤力和墙的生命值
        #                 # 杀伤力
        #                 power = bullet.get_attack_power()
        #                 # 生命值
        #                 hp = wall.get_hp()
        #
        #                 # 子弹杀伤力会减弱
        #                 bullet.receive_attack(hp)
        #                 # 墙的生命值也会减少
        #                 wall.receive_beaten(power)
        #
        #                 break

        # 子弹和砖墙的碰撞
        # 具备 攻击能力的物体 和 具备挨打能力的物体 发生碰撞
        for attack in self.views:
            if isinstance(attack, Attack):
                for beaten in self.views:
                    if isinstance(beaten, Beaten) and attack.is_attacked(beaten):
                        # 判断子弹和墙是否发生碰撞

                        # 根据子弹的杀伤力和墙的生命值
                        # 杀伤力
                        power = attack.get_attack_power()
                        # 生命值
                        hp = beaten.get_hp()

                        # 子弹杀伤力会减弱
                        attack.receive_attack(hp)
                        # 墙的生命值也会减少
                        beaten.receive_beaten(power)

                        break

    def keydown(self, key):
        """按下事件"""
        pass

    def keypress(self, keys):
        """长按事件"""
        if keys[K_a]:
            # 向左移动
            self.player1.move(Direction.LEFT)
        if keys[K_d]:
            # 向右移动
            self.player1.move(Direction.RIGHT)
        if keys[K_w]:
            self.player1.move(Direction.UP)
        if keys[K_s]:
            self.player1.move(Direction.DOWN)
        if keys[K_q] or keys[K_e]:
            self.__add_view(self.player1.fire())
        if keys[K_LEFT]:
            # 向左移动
            self.player2.move(Direction.LEFT)
        if keys[K_RIGHT]:
            # 向右移动
            self.player2.move(Direction.RIGHT)
        if keys[K_UP]:
            self.player2.move(Direction.UP)
        if keys[K_DOWN]:
            self.player2.move(Direction.DOWN)
        if keys[K_KP1] or keys[K_RSHIFT]:
            self.__add_view(self.player2.fire())

    def __add_view(self, view):
        if isinstance(view, Display):
            self.views.append(view)


class InfoContainer:
    def __init__(self, surface):
        self.surface = surface
        # 文字
        self.noticeFont = pygame.font.Font("./font/SIMHEI.ttf", 45)
        self.tongJiFont = pygame.font.Font("./font/SIMHEI.ttf", 30)
        self.hpFont = pygame.font.Font("./font/SIMHEI.ttf", 20)

    def graphic(self, xinXi):
        """渲染"""
        self.surface.fill((0xbb, 0xbb, 0xbb))
        colour = (255, 0, 0)
        self.text1 = self.noticeFont.render('时间：%d' % xinXi['剩余时间'], True, colour)
        self.text2 = self.tongJiFont.render('玩家数量：%d' % xinXi['玩家数量'], True, colour)
        self.text3 = self.tongJiFont.render('玩家无敌：%s' % xinXi['玩家无敌'], True, colour)
        self.text4 = self.tongJiFont.render('敌军数量：%d' % xinXi['敌军数量'], True, colour)
        self.text5 = self.tongJiFont.render('剩余敌军：%d' % xinXi['剩余敌军'], True, colour)
        self.text6 = self.tongJiFont.render('敌军军营：%d' % xinXi['敌军军营'], True, colour)
        self.text7 = self.hpFont.render('玩家1血量：%d' % xinXi['玩家1血量'], True, colour)
        self.text8 = self.hpFont.render('玩家2血量：%d' % xinXi['玩家2血量'], True, colour)
        self.text9 = self.hpFont.render('基地血量：%d' % xinXi['基地血量'], True, colour)
        self.text10 = self.hpFont.render('护甲血量：%d' % xinXi['护甲血量'], True, colour)
        self.surface.blit(self.text1, (20, 40))
        self.surface.blit(self.text2, (20, 120))
        self.surface.blit(self.text7, (20, 170))
        self.surface.blit(self.text8, (20, 220))
        self.surface.blit(self.text9, (20, 270))
        self.surface.blit(self.text10, (20, 320))
        self.surface.blit(self.text3, (20, 400))
        self.surface.blit(self.text4, (20, 480))
        self.surface.blit(self.text5, (20, 560))
        self.surface.blit(self.text6, (20, 640))
