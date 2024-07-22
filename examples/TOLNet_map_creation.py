
import requests
import pandas as pd
import numpy as np
import geopandas, geodatasets
import pandas
import matplotlib.pyplot as plt
from pathlib import Path

def get_files_list():
    """
    Parameters
    ----------
    min_date : STR
        The starting date for the query, in YYYY-MM-DD format.
    max_date : STR
        The ending date for the query, in YYYY-MM-DD format.

    Returns
    -------
    A DataFrame containing all files from the TOLNet API that fall between the two provided dates.
    The DataFrame contains each file name as well as various descriptors.
    """
    dtypes = {"row": "int16",
             "count": "int16",
             "id": "int16",
             "file_name": "str",
             "file_server_location": "str",
             "author": "str",
             "instrument_group_id": "int16",
             "product_type_id": "int16",
             "file_type_id":"int16",
             "start_data_date": "datetime64[ns]",
             "end_data_date":"datetime64[ns]",
             "upload_date":"datetime64[ns]",
             "public": "bool",
             "instrument_group_name": "str",
             "folder_name": "str",
             "current_pi": "str",
             "doi": "str",
             "citation_url": "str",
             "product_type_name": "str",
             "processing_type_name": "str",
             "file_type_name": "str",
             "revision": "int16",
             "near_real_time": "str",
             "file_size": "int16",
             "latitude": "float16",
             "longitude": "float16",
             "altitude": "int16",
             "isAccessible": "bool"
             }

    i = 1
    url = f"https://tolnet.larc.nasa.gov/api/data/1?&order=data_date&order_direction=desc"
    response = requests.get(url)
    data_frames = []
    while response.status_code == 200:
        data_frames.append(pd.DataFrame(response.json()))
        i += 1
        url = f"https://tolnet.larc.nasa.gov/api/data/{i}?&order=data_date&order_direction=desc"
        response = requests.get(url)
        
        if i % 10 == 0:
            print(i)
            

    df = pd.concat(data_frames, ignore_index=True)
    df["start_data_date"] = pd.to_datetime(df["start_data_date"])
    df["end_data_date"] = pd.to_datetime(df["end_data_date"])
    df["upload_date"] = pd.to_datetime(df["upload_date"])
    return df.astype(dtypes)



all_files = get_files_list()
all_files['lat_long'] = [f"{all_files['latitude'].iloc[i]}_{all_files['longitude'].iloc[i]}" for i in range(len(all_files))]
unique_latlong = np.array(pd.unique(all_files['lat_long']))

lats, longs = [], []
for line in unique_latlong:
    lats.append(float(line.split('_')[0]))
    longs.append(float(line.split('_')[1]))

states = geopandas.read_file(Path(r"..\..\ne_110m_admin_1_states_provinces\ne_110m_admin_1_states_provinces.shp"))

earth = geopandas.read_file(geodatasets.get_path("naturalearth.land"))

xlims, ylims = [-125, -60], [20, 65]

stations = [
    {'name': 'ECCC', 'latitude': 44.371, 'longitude': -79.851},
    {'name': 'NASA GSFC', 'latitude': 38.99, 'longitude': -76.84},
    {'name': 'NOAA ESRL/CSL', 'latitude': 39.99, 'longitude': -105.26},
    {'name': 'UAH', 'latitude': 34.73, 'longitude': -86.65},
    {'name': 'CCNY', 'latitude': 40.821, 'longitude': -73.949},
    {'name': 'Hampton U', 'latitude': 37.02, 'longitude': -76.34},
    {'name': 'NASA JPL', 'latitude': 34.38, 'longitude': -117.68}]

homebases = pandas.DataFrame(stations)
fig, ax = plt.subplots(figsize=(20, 20), layout="tight")
plt.title("TOLNet Dataset Locations", fontsize=36, loc="center", y=1.05)
earth.plot(ax=ax, color="lightsteelblue")
states.boundary.plot(ax=ax, color="black")
plt.plot(longs, lats, "o", color="yellow", markersize=15, label="Campaign Data")
plt.plot(homebases['longitude'], homebases['latitude'], "o", color="red", markersize=15, label="Homebase Locations")

plt.ylim(ylims)
plt.xlim(xlims)
ax.legend(ncols=2, bbox_to_anchor=(0.5, 1.02), loc="center", fontsize=18)
plt.show()