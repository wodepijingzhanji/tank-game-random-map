import random
import time


class MapUtilTB:
    # 坦克大战地图生成和校验器工具类
    @staticmethod
    def floodFill(outset, r):
        '''仿floodfill函数，判断r的outset侧是否单连通'''
        area = [outset]
        room = r[:]
        while area:
            point = area.pop(0)
            for around in room[:]:
                if MapUtilTB.isNeighbor(point, around):
                    area.append(around)
                    room.remove(around)
        if room:
            return False
        else:
            return True

    @staticmethod
    def isNeighbor(center, around):
        '''判断around=(row,column)是否在center=row,column)周围（四路），rowMax为行数，columnMax为列数'''
        if (center[0] - around[0]) ** 2 + (center[1] - around[1]) ** 2 > 1:  # 四路
            return False
        else:
            return True


class MapTB:
    def __init__(self, rowMax=13, columnMax=13, funcFlag='2'):
        self.rowMax = rowMax
        self.columnMax = columnMax
        self.funcFlag = funcFlag
        self.kinds = ['空', '草', '水', '砖', '铁']
        self.blocksKinds = ['水', '铁']
        self.movables = ['主', '副', '鹰']
        self.enemyNum = random.randint(2, 10)
        self.movables.extend(['敌' for i in range(0, self.enemyNum)])

        while True:
            self.reset()
            self.creatMap()
            if self.checkMap():
                break

    def reset(self):
        self.map = []
        self.heroNum = 0
        self.steelNum = 0
        self.wallNum = 0
        self.waterNum = 0
        self.grassNum = 0
        self.airNum = 0
        self.leadP = ()

    def creatMap(self):
        for i in range(0, self.rowMax):
            row = []
            for j in range(0, self.columnMax):
                row.append(random.choice(self.kinds))
            self.map.append(row)
        for movable in self.movables:
            while True:
                i = random.randint(0, self.rowMax - 1)
                j = random.randint(0, self.columnMax - 1)
                if self.map[i][j] not in self.movables:
                    self.map[i][j] = movable
                    break
        #鹰的左上定义为1，顺时针+1
        for i in range(0, self.rowMax):
            for j in range(0, self.columnMax):
                if self.map[i][j] == '鹰':
                    if i > 0 and j > 0:
                        self.map[i - 1][j - 1] = '一'
                    if i > 0:
                        self.map[i - 1][j] = '二'
                    if i > 0 and j < self.columnMax - 1:
                        self.map[i - 1][j + 1] = '三'
                    if j < self.columnMax - 1:
                        self.map[i][j + 1] = '四'
                    if i < self.rowMax - 1 and j < self.columnMax - 1:
                        self.map[i + 1][j + 1] = '五'
                    if i < self.rowMax - 1:
                        self.map[i + 1][j] = '六'
                    if i < self.rowMax - 1 and j > 0:
                        self.map[i + 1][j - 1] = '七'
                    if j > 0:
                        self.map[i][j - 1] = '八'

    def checkMap(self):
        room = []
        self.enemyNum = 0
        for i in range(0, self.rowMax):
            for j in range(0, self.columnMax):
                if self.map[i][j] == '主':
                    self.heroNum += 1
                    self.leadP = (i, j)
                elif self.map[i][j] == '副':
                    self.heroNum += 1
                    room.append((i, j))
                elif self.map[i][j] == '敌':
                    self.enemyNum += 1
                    room.append((i, j))
                elif self.map[i][j] == '铁':
                    self.steelNum += 1
                elif self.map[i][j] == '水':
                    self.waterNum += 1
                elif self.map[i][j] == '砖':
                    self.wallNum += 1
                    room.append((i, j))
                elif self.map[i][j] == '草':
                    self.grassNum += 1
                    room.append((i, j))
                elif self.map[i][j] == '空':
                    self.airNum += 1
                    room.append((i, j))
                else:
                    room.append((i, j))
        if self.heroNum<2 or self.enemyNum<2:
            return False
        else:
            return MapUtilTB.floodFill(self.leadP, room)

    def __str__(self):
        s = ''
        for i in range(0, self.rowMax):
            for j in range(0, self.columnMax):
                s += self.map[i][j]
            s += '\n'
        # return str(self.map)
        return s

    def getName(self):
        '''生成地图文件名称'''
        # 地图名称为mapTB+英雄位置数+初始敌人位置数+不可穿越的障碍物数+时间标记
        return 'mapTB%dH%dE%dB%s.map' % (
            self.heroNum, self.enemyNum, self.steelNum + self.waterNum, str(int(time.time())))


if __name__ == '__main__':
    # 试验
    myMap = MapTB()
    print(myMap)
    f = open('../map/' + myMap.getName(), 'w', encoding='UTF-8')
    f.write(str(myMap))
    f.close()
