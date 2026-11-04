class Cat:
    def __init__(self,name,color):
        self.name = name
        self.color = color
    def neow(self):
        print(f"{self.color}的，{self.name}喵喵叫！")
    def sleep(self):
        print(f"{self.color}的，{self.name}睡觉了！")

my_cat = Cat("优米", "黄色")
your_cat = Cat("悠米","白色")

print(f"优米原来的颜色：{my_cat.color}")
my_cat.color = "黑色"
print(f"优米现在的颜色：{my_cat.color}")
my_cat.neow()
your_cat.sleep()

class ElectricCat(Cat):
    def __init__(self,name,color):
        super().__init__(name,color)
        self.age = 3
    def drink_milk(self):
        print(f"{self.name}正在喝奶，它才{self.age}个月大！")
    def sleep(self):
        print(f"🔋{self.name}正在充电，不睡觉！")
my_cat_age = ElectricCat("悠悠米", "暖色")

my_cat_age.drink_milk()

my_cat_age.neow()
my_cat_age.sleep()