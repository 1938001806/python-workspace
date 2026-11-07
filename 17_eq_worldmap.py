import json
filename = r'E:\python源码\python工作区\lreaning\eq_data.json'

with open(filename, encoding='utf-8') as f:
    all_eq_data = json.load(f)

all_eq_dicts = all_eq_data['features']

mags, lons, lats = [], [], []
for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]

    mags.append(mag)
    lons.append(lon)
    lats.append(lat)

print("提取到的震级", mags)
print("提取到的经度", lons)
print("提取到的维度", lats)
