import time
start = time.time()
class House(object):
#初始化
    def __init__(self,name,add,area):
        self.name = name
        self.address = add
        self.or_area = 85
        self.free_area = self.or_area
        self.contain_items = []

#定义添加家具方法
    def add_fur(self,Item):
        if self.free_area >= Item.GetUsedArea():
            self.free_area -= Item.GetUsedArea()
            self.contain_items.append(Item)
        else:
            print("家里边装不下了！！")
#定义打印方法
    def __str__(self):
        mf = self.name + " is in " + self.address + "," +" house square is " + str(self.or_area) + ",the existing furniture is:"
        if len(self.contain_items) > 0:
            for i in self.contain_items:
                mf = mf + i.gettype() + ","
        else:
            mf += "nothing"
        mf = mf.strip(",")
        return mf
    def list_fur(self):
        return self.contain_items

#定义家具类
class Furniture(object):
    def __init__(self,type,need_area):
        self.type = type
        self.need_area = need_area
    def gettype(self):
        return str(self.type)
    def GetUsedArea(self):
        return self.need_area

my_house = House("my house","ChongQing YuBei",85)
f1 = Furniture("bed",5)
f2 = Furniture("refrigerator",1)
f3 = Furniture("television",2)
my_house.add_fur(f1)
print(my_house)
print(list(my_house.list_fur()))
finish = time.time()
