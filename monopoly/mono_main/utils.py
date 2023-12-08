import random
from pathlib import Path
from typing import Any, List

from pydantic import BaseModel

# 定义类


class Building(BaseModel):
    name: str
    """名称或空地"""
    price: int
    """价值"""
    payment: int
    """收费价格"""
    location: str
    was_bought: bool = False
    """是否允许购买"""
    built_room: int = 0
    """小房子数量"""
    owner: str = 'no'
    """所有者名字"""


class Player(BaseModel):
    """用户信息"""

    name: str
    money: int = 10000
    """拥有资金"""
    isGoingToMove: bool = False
    """是处于行动回合"""
    movable: bool = True
    """是否可以行动"""
    image: Any
    position: int = 0
    """位置序号"""
    temp_position: bool = False
    dice_value: int = 0
    """骰子值"""
    locatedBuilding: Building
    """所在位置建筑"""
    showText: list = []
    """个人简介"""
    isPlayer: bool = False
    """判断玩家还是人机"""
    ownedBuildings: list = []
    """拥有地产"""
    isShowText: bool = False
    """是否展示简介"""
    caishen: int = 0
    """财神附体"""
    shuaishen: int = 0
    """衰神附体"""
    tudishen: int = 0
    """土地神附体"""
    pohuaishen: int = 0
    """破坏神附体"""

    def judgePosition(self, buildings: List[Building]):
        """位置判断 返回值是所在位置的建筑"""
        for each in buildings:
            for every in each.location:
                if self.position == every:
                    return each
            ''' 
            try:
                for every in each.location:
                    if self.position == every:
                        print(each.name)
            except:
                if self.position == every:
                    print(each.name)
            '''

    def buyaBuilding(self, isPressYes):
        """购买方法"""
        if self.locatedBuilding is None:
            return False
        if isPressYes and self.locatedBuilding.owner != self.name:
            self.locatedBuilding.owner = self.name
            self.locatedBuilding.was_bought = True
            self.ownedBuildings.append(self.locatedBuilding)
            self.money -= self.locatedBuilding.price
            self.showText = [
                self.name + '购买了' + self.locatedBuilding.name + '!'
            ]
            return True
        else:
            return False

    def move(self, buildings: List[Building], allplayers):
        """移动方法 返回值是所在的建筑位置"""
        self.dice_value = random.randint(1, 6)
        self.position += self.dice_value
        if self.position >= 16:
            self.position -= 16
        building = self.judgePosition(buildings)
        if building is None:
            return None
        self.locatedBuilding = building
        self.isShowText = True
        return self.eventInPosition(allplayers)

    def addaHouse(self, isPressYes: bool):  # 在建筑物上添加一个房子
        if self.locatedBuilding is None:
            return False
        try:
            if isPressYes and self.locatedBuilding.owner == self.name:
                self.locatedBuilding.built_room += 1
                self.money -= self.locatedBuilding.payment
                self.showText = [
                    self.name + '在' + self.locatedBuilding.name + '上!',
                    '盖了一座房子！',
                    '有%d' % self.locatedBuilding.built_room + '个房子了！',
                    "它的过路费是%d"
                    % (
                        self.locatedBuilding.payment
                        * (self.locatedBuilding.built_room + 1)
                    ),
                ]
                return True
            else:
                return False
        except Exception:
            pass

    def eventInPosition(self, allplayers):
        """判断在建筑位置应该发生的事件"""
        if self.locatedBuilding is None:
            return False
        building = self.locatedBuilding
        if building.name != '空地':
            if self.locatedBuilding.was_bought is False:
                """未购买的时候显示建筑的数据"""
                if self.isPlayer is True:
                    textLine0 = (
                        self.name + '扔出了' + '%d' % self.dice_value + '点！'
                    )
                    textLine1 = self.name + '来到了' + building.name + '!'
                    textLine2 = '购买价格：%d' % building.price
                    textLine3 = '过路收费：%d' % building.payment
                    textLine4 = '是否购买？'
                    self.showText = [
                        textLine0,
                        textLine1,
                        textLine2,
                        textLine3,
                        textLine4,
                    ]
                    return True
                else:
                    self.addaHouse(not self.buyaBuilding(True))

                # ----- 是否购买 ------
            elif building.owner == self.name:
                """路过自己的房子开始加盖建筑"""
                if self.pohuaishen == 1:
                    textLine0 = self.name + '破坏神附体！'
                    textLine1 = '摧毁了自己的房子！'
                    building.owner = 'no'
                    building.wasBought = False
                    self.showText = [textLine0, textLine1]
                    self.pohuaishen = 0
                else:
                    if self.isPlayer is True:
                        textLine0 = (
                            self.name + '扔出了' + '%d' % self.dice_value + '点！'
                        )
                        textLine1 = '来到了ta的' + self.locatedBuilding.name + '!'
                        textLine2 = '可以加盖小房子！'
                        textLine3 = '加盖收费：%d' % building.payment
                        textLine4 = '是否加盖？'
                        self.showText = [
                            textLine0,
                            textLine1,
                            textLine2,
                            textLine3,
                            textLine4,
                        ]
                        return True

                    else:
                        self.addaHouse(True)
            else:
                for each in allplayers:
                    """被收费"""
                    if (
                        self.locatedBuilding.owner == each.name
                        and each.name != self.name
                    ):
                        if self.caishen == 1:
                            textLine0 = self.name + '财神附体！'
                            textLine1 = '免除过路费%d！' % (
                                building.payment * (building.built_room + 1)
                            )
                            self.showText = [textLine0, textLine1]
                            self.caishen = 0
                        else:
                            if self.tudishen == 1:
                                textLine0 = self.name + '土地神附体！'
                                textLine1 = '强占土地！'
                                textLine2 = building.name + '现在属于' + self.name
                                self.locatedBuilding.owner = self.name
                                self.showText = [
                                    textLine0,
                                    textLine1,
                                    textLine2,
                                ]
                                self.tudishen = 0
                            else:
                                if self.pohuaishen == 1:
                                    textLine0 = self.name + '破坏神附体！'
                                    textLine1 = '摧毁了对手的房子！'
                                    building.owner = 'no'
                                    building.wasBought = False
                                    self.showText = [textLine0, textLine1]
                                    self.pohuaishen = 0
                                else:
                                    textLine0 = (
                                        self.name
                                        + '扔出了'
                                        + '%d' % self.dice_value
                                        + '点！'
                                    )
                                    textLine1 = (
                                        self.name + '来到了' + each.name + '的:'
                                    )
                                    textLine2 = building.name + '，被收费!'
                                    if self.shuaishen == 1:
                                        textLine3 = '过路收费：%d*2!' % (
                                            building.payment
                                            * (building.built_room + 1)
                                            * 2
                                        )
                                        self.shuaishen = 0
                                    else:
                                        textLine3 = '过路收费：%d' % (
                                            building.payment
                                            * (building.built_room + 1)
                                        )
                                    textLine4 = '哦！' + self.name + '好倒霉！'
                                    self.showText = [
                                        textLine0,
                                        textLine1,
                                        textLine2,
                                        textLine3,
                                        textLine4,
                                    ]
                                    # 收费！
                                    self.money -= building.payment * (
                                        building.built_room + 1
                                    )
                                    each.money += building.payment * (
                                        building.built_room + 1
                                    )
                                    # ----- 动画-------

        else:
            whichone = self.dice_value % 4
            textLine2 = ""
            textLine3 = ""
            if whichone == 0:
                self.caishen = 1
                textLine2 = '遇到了财神！'
                textLine3 = '免一次过路费！'
            if whichone == 1:
                self.shuaishen = 1
                textLine2 = '遇到了衰神！'
                textLine3 = '过路费加倍一次！'
            if whichone == 2:
                self.tudishen = 1
                textLine2 = '遇到了土地神！'
                textLine3 = '强占一次房子！'
            if whichone == 3:
                self.pohuaishen = 1
                textLine3 = '摧毁路过的房子！'
                textLine2 = '遇到了破坏神！'
            textLine0 = self.name + '扔出了' + '%d' % self.dice_value + '点！'
            textLine1 = '来到了运气地点！'
            self.showText = [textLine0, textLine1, textLine2, textLine3]


class userinfo(BaseModel):
    id: str
    name: str
    image: Path


class AllData(BaseModel):
    location_length: int = 30
    """地图长度"""
    sence_buildings: List[Building] = []
    """地图建筑信息"""
    players: List[Player]
    """玩家信息"""
