class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def sit(self):
        print(f"{self.name}乖乖坐下了。")
    def bark(self):
        print(f"{self.name}汪汪叫！它今年{self.age}岁了。")

my_dog = Dog("旺财", 3)
your_dog = Dog("大黄", 5)

my_dog.bark()
your_dog.sit()