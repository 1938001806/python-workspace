import csv
from datetime import datetime
from matplotlib import pyplot as plt

filename = r'E:\python源码\python工作区\lreaning\sitka_weather_07-2014.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    highs, lows, dates = [], [], []
    for row in reader:
        current_date = datetime.strptime(row[0], "%Y-%m-%d")
        dates.append(current_date)

        high = int(row[1])
        highs.append(high)
        low = int(row[3])
        lows.append(low)

fig = plt.figure(dpi=128,figsize=(10, 6))
plt.plot(dates, highs, c='red', alpha=0.6)
plt.plot(dates, lows, c='blue', alpha=0.6)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)
plt.title("Daily High and low Temperatures, july 2014", fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Temperature(f)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)


plt.show()

