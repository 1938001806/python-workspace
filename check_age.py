def check_age(age):
    return "已成年" if age >= 18 else "未成年"

assert check_age(18) == "已成年" 
assert check_age(17) == "未成年"

print("全部通过")

