import json
import plotly.express as px

filename = r'E:\python源码\python工作区\lreaning\eq_data.json'

with open(filename, encoding='utf-8') as f:
    all_eq_data = json.load(f)

all_eq_dicts = all_eq_data['features']

mags, lons, lats, eq_titles = [], [], [], []
for eq_dict in all_eq_dicts:
    mag = eq_dict['properties']['mag']
    lon = eq_dict['geometry']['coordinates'][0]
    lat = eq_dict['geometry']['coordinates'][1]
    eq_title = eq_dict['properties']['title']

    mags.append(mag)
    lons.append(lon)
    lats.append(lat)
    eq_titles.append(eq_title)

fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=mags,
    color=mags,
    hover_name=eq_titles,
    color_continuous_scale='Viridis',
    title='Global Earthquakes',
    projection='natural earth'
)

fig.show()