

while True:
    password = input("请输入密码").strip()
    if password == "123":
        print("密码正确")
        break
    else:
         print("请重新输入密码")

data = [1,2,3]

for i in data:
    if i == 2:
        print(f"{i}")
