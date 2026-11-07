import matplotlib.pyplot as plt
from random import randint

class Die:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return  randint(1, self.num_sides)

die_1 = Die(10)
die_2 = Die()

results = []
for roll_num in range(10000):
    result = die_1.roll() + die_2.roll()
    results.append(result)

frequencies = []
max_result = die_1.num_sides + die_2.num_sides

for value in range(2, max_result + 1):
    frequency = results.count(value)
    frequencies.append(frequency)

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

x_values = list(range(2, max_result + 1))

plt.bar(x_values, frequencies, color='skyblue', edgecolor='black')

plt.title("两个骰子点数之和的概率分布", fontsize=18)
plt.xlabel("点数之和", fontsize=14)
plt.ylabel("出现次数", fontsize=14)

plt.xticks(x_values)

plt.show()