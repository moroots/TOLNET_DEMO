import requests

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

print("Retrieving O3 data...")
url = "https://fluid.nccs.nasa.gov/cfapi/fcast/chm_p23/O3/"
response = requests.get(url)
data = response.json()
levels = data['schema']['lev']
values = []



# for some reason data['values'] doesn't include the very last value
# data['10'] has values that are 10x bigger than everything else so it messes up the graph
print("Creating graph...    ")
for i in levels[-12:-1]:
    values.append(data['values']['O3'][str(i)])
    
fig = plt.figure(figsize=(15, 8))
ax = plt.subplot(111)
ax.set_title('O3 levels over pressure')
ax.set_xlabel("Hours passed after " + data['time'][0])
ax.set_ylabel("Pressure level")
# I don't know what units the pressure uses

plt.imshow(np.array(values), interpolation='none', extent=[0, 10, 600, 975], aspect="auto")

cax = fig.add_axes([3, 3, 3, 3])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)
plt.colorbar(orientation='vertical')
plt.show()



"""
im = ax.pcolormesh(values)  


cbar = fig.colorbar(im, ax=ax, pad=0.01, ticks=[0.001, *np.arange(10, 101, 10), 200, 300])
cbar.set_label(label='Ozone ($ppb_v$)', size=16, weight="bold")
"""




"""
self.data[name] = self.data[name].fillna(value=np.nan)
X, Y, Z = (self.data[name].index, self.data[name].columns, self.data[name].to_numpy().T,)
im = ax.pcolormesh(X, Y, Z, cmap=ncmap, norm=nnorm, shading="nearest")


plt.show()
"""

#%% Maurice Roots

test = "https://fluid.nccs.nasa.gov/cfapi/aqc/fcast/o3/45.5x9.2/20200416/"






met_url = f'{base_url}/{collection}/{dataset}/{molecule}/{lat}x{lon}/{start_date}'

class GEOS_CF():
    
    def __initi__(self):
        self.base_url = "https://fluid.nccs.nasa.gov/cfapi/"
        self.schema = requests.get(self.base_url).json()
        return
    
    def _get_dat(molecule, lat, lon, start_date, collection="fcast"):
        
        return requests.get(url_query).json()
        
    
    
        #%% 
import requests
import numpy as np
from tqdm import tqdm


start_date = np.datetime64("2024-06-11")
# end_date = start_date - np.timedelta64(1,"Y")

valid = {}

def _api_test(url):
    return requests.get(url)
                    
# tqdm(as_completed(future_to_file), total=len(future_to_file)):
for i in tqdm(np.arange(0, 65)):
    date = str(start_date - np.timedelta64(i, "D")).replace("-", "")
    url = f"https://fluid.nccs.nasa.gov/cfapi/fcast/chm_p23/O3/39.0x-77.0/{date}"
    response = _api_test(url)
    if response.status_code == 200:
        if response.text == 'No data is available for this date.':
            valid[date] = False
        else:
            valid[date] = True
    
        


fixed_url = "https://fluid.nccs.nasa.gov/cfapi/assim/chm_p23/o3/39.0x-77.0/20230808/"
        
        
        
        
        
        
        
        
        