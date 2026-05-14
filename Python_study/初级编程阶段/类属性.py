class Shabi(object):
    shabi_list = []
    count = 0
    def __init__(self,name,age,telephone):
        self.name = name
        self.age = age
        self.telephone = telephone
        Shabi.count += 1
        Shabi.shabi_list.append(self.__str__())
    def __str__(self):
        return f"me:{self.name}, am {self.age} this year, wocaonima"
sb1 = Shabi("xiaojie",18,1145)
sb2 = Shabi("yuhuaichun",18,11451)
print(Shabi.shabi_list)
print(Shabi.count)