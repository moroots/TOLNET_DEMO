import requests

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# met_url = f'{base_url}/{collection}/{dataset}/{molecule}/{lat}x{lon}/{start_date}'

class GEOS_CF():
    
    def __init__(self):
        # self.base_url = "https://fluid.nccs.nasa.gov/cfapi"
        self.base_url = "https://dphttpdev01.nccs.nasa.gov/data-services/cfapi"
        self.times = []
        self.schema = requests.get(self.base_url).json()
        return
    
    def _get_dat(self, collection, molecule, lat, lon, date_start, date_end):
        url_query = f'{self.base_url}/{collection}/chm/p23/{molecule}/{lat}x{lon}/{date_start}/{date_end}'
        print(url_query)
        response = requests.get(url_query).json()
        
        self.meta_data = response['schema']
        self.times += response['time']
        
        # Tweak later when querying multiple files
        self.data = pd.DataFrame.from_dict(response['values'][molecule])
        
        self.data.index = [pd.to_datetime(time, format="%Y-%m-%dT%H:%M:%S") for time in self.times]
        self.data.columns = self.data.columns.astype(float)
        self.data.sort_index(axis=1, inplace=True)
        # self.data = np.flipud(self.data)
        return self
    
        
    
        
    @staticmethod
    def O3_curtain_colors():
        """
        Returns
        -------
        The color scheme used in the O3 curtain plots on the TOLNet website.

        """
        ncolors = [np.array([255,  140,  255]) / 255.,
           np.array([221,  111,  242]) / 255.,
           np.array([187,  82,  229]) / 255.,
           np.array([153,  53,  216]) / 255.,
           np.array([119,  24,  203]) / 255.,
           np.array([0,  0,  187]) / 255.,
           np.array([0,  44,  204]) / 255.,
           np.array([0,  88,  221]) / 255.,
           np.array([0,  132,  238]) / 255.,
           np.array([0,  165,  255]) / 255.,
           np.array([0,  235,  255]) / 255.,
           np.array([39,  255,  215]) / 255.,
           np.array([99,  255,  150]) / 255.,
           np.array([163,  255,  91]) / 255.,
           np.array([211,  255,  43]) / 255.,
           np.array([255,  255,  0]) / 255.,
           np.array([250,  200,  0]) / 255.,
           np.array([255,  159,  0]) / 255.,
           np.array([255,  111,  0]) / 255.,
           np.array([255,  63,  0]) / 255.,
           np.array([255,  0,  0]) / 255.,
           np.array([216,  0,  15]) / 255.,
           np.array([178,  0,  31]) / 255.,
           np.array([140,  0,  47]) / 255.,
           np.array([102,  0,  63]) / 255.,
           np.array([200,  200,  200]) / 255.,
           np.array([140,  140,  140]) / 255.,
           np.array([80,  80,  80]) / 255.,
           np.array([52,  52,  52]) / 255.,
           np.array([0,0,0]) ]

        ncmap = mpl.colors.ListedColormap(ncolors)
        ncmap.set_under([1,1,1])
        ncmap.set_over([0,0,0])
        bounds =   [0.001, *np.arange(5, 110, 5), 120, 150, 200, 300, 600]
        nnorm = mpl.colors.BoundaryNorm(bounds, ncmap.N)
        return ncmap, nnorm
        
    def curtain_plot(self):
        
        ncmap, nnorm = self.O3_curtain_colors()
        fig, ax = plt.subplots(1, 1, figsize=(15, 8), layout="tight")
        X, Y, Z = (self.data.index, 
                           self.data.columns, 
                           self.data.to_numpy().T,)
        im = ax.pcolormesh(X, Y, Z, cmap=ncmap, norm=nnorm, shading="nearest")
        cbar = fig.colorbar(im, ax=ax, pad=0.01, ticks=[0.001, *np.arange(10, 101, 10), 200, 300])
        cbar.set_label(label='Ozone ($ppb_v$)', size=16, weight="bold")
        
        
        plt.setp(ax.get_xticklabels(), fontsize=16)
        plt.setp(ax.get_yticklabels(), fontsize=16)
        
        plt.gca().invert_yaxis()
        
        cbar.ax.tick_params(labelsize=16)
        plt.title(
            f"$O_3$ Mixing Ratio Profile (assim dataset)", fontsize=20)
        ax.set_ylabel("Pressure Level", fontsize=18)
        ax.set_xlabel("Datetime (UTC)", fontsize=18)
        plt.show()
        return self
    
if __name__ == "__main__":
    geos = GEOS_CF()
    print("Created GEOS intance")
    geos._get_dat("assim", "O3", "39.0", "-77.0", "20230805", "20230808")
    geos.curtain_plot()
        
        
        
        
        
        
        