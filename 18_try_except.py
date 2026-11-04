class SmartCat:
    def __init__(self,name):
        self.name = name
    def jump(self,height):
        try:
            h = int(height)
            print(f"{self.name}跳了{h}厘米高！")

        except ValueError:
            print(f"❌ 错误：{self.name}听不懂'{height}'是什么高度，请输入数字！")

        except ZeroDivisionError:
            print("❌ 错误：分母不能为0！")
        finally:
            print(f"{self.name}的一次跳跃尝试结束了。\n")

my_cat = SmartCat("tom")
my_cat.jump("50")
my_cat.jump("很多")
my_cat.jump("-10")