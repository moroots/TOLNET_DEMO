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