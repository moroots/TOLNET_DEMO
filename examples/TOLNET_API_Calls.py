 # -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:32:30 2023

@author: meroo
"""

import requests
import pandas as pd
import numpy as np
import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.units as munits

from dateutil import tz

from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor, as_completed

#%% Function Space

class filter_files:
    def __init__(self, df):
        self.df = df
        pass

    def daterange(self, min_date: str = None, max_date: str = None, **kwargs) -> pd.DataFrame:
        try:
            self.df = self.df[(self.df["start_data_date"] >= min_date) & (self.df["start_data_date"] <= max_date)]
        except:
            pass
        return self

    def instrument_group(self, instrument_group: list = None, **kwargs) -> pd.DataFrame:
        try:
            self.df = self.df[self.df["instrument_group_id"].isin(instrument_group)]
        except:
            pass
        return self

    def product_type(self, product_type: list = None, **kwargs) -> pd.DataFrame:
        try:
            self.df = self.df[self.df["product_type_id"].isin(product_type)]
        except:
            pass
        return self

    def file_type(self, file_type: list = None, **kwargs) -> pd.DataFrame:
        try:
            self.df = self.df[self.df["file_type_id"].isin(file_type)]
        except:
            pass
        return self
    
    def processing_type(self, processing_type: list = None, **kwargs) -> pd.DataFrame:
        """
        id 1 = centrally proccessed
        id 2 = in-house 
        id 3 = unprocessed
        """
        
        
        
        
        try:
            processing_type_names = []
            types = tolnet.processing_types
            for process in processing_type:
                processing_type_names.append(
                    list(types["processing_type_name"][types["id"] == process])[0])
                    
            self.df = self.df[self.df["processing_type_name"].isin(processing_type_names)]
        except:
            pass
        return self

class TOLNet:

    def __init__(self):
        self.products = self.get_product_types()
        self.file_types = self.get_file_types()
        self.instrument_groups = self.get_instrument_groups()
        self.processing_types = self.get_processing_types()
        # self.files = self.get_files_list()
        return
    
    def products(self): 
        print("TOLNET product IDs:")
        print(self.products[["id", "product_type_name"]].to_string(index=False))
        return 
    
    
    def file_types(self):
        print("File Types:")
        print(self.file_types[["id", "file_type_name"]].to_string(index=False))

    def insturment_groups(self):
        print("Instrument Groups:")
        print(self.instrument_groups[["id", "instrument_group_name"]].to_string(index=False))
        return
        
    def processing_types(self):
        print("Processing Types:")
        print(self.processing_types[["id", "processing_type_name"]].to_string(index=False))
        return
    
    @staticmethod
    def get_product_types():
        return pd.DataFrame(requests.get("https://tolnet.larc.nasa.gov/api/data/product_types").json()).sort_values(by=["id"])

    @staticmethod
    def get_file_types():
        return pd.DataFrame(requests.get("https://tolnet.larc.nasa.gov/api/data/file_types").json()).sort_values(by=["id"])

    @staticmethod
    def get_instrument_groups():
        return pd.DataFrame(requests.get("https://tolnet.larc.nasa.gov/api/instruments/groups").json()).sort_values(by=["id"])
    
    @staticmethod
    def get_processing_types():
        return pd.DataFrame(requests.get("https://tolnet.larc.nasa.gov/api/data/processing_types").json()).sort_values(by=["id"])

    @staticmethod
    def get_files_list(min_date, max_date):
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
                 "latitude": "int16",
                 "longitude": "int16",
                 "altitude": "int16",
                 "isAccessible": "bool"
                 }

        i = 1
        url = f"https://tolnet.larc.nasa.gov/api/data/1?min_date={min_date}&max_date={max_date}&order=data_date&order_direction=desc"
        response = requests.get(url)
        data_frames = []
        while response.status_code == 200:
            data_frames.append(pd.DataFrame(response.json()))
            i += 1
            url = f"https://tolnet.larc.nasa.gov/api/data/{i}?min_date={min_date}&max_date={max_date}&order=data_date&order_direction=desc"
            response = requests.get(url)

        df = pd.concat(data_frames, ignore_index=True)
        df["start_data_date"] = pd.to_datetime(df["start_data_date"])
        df["end_data_date"] = pd.to_datetime(df["end_data_date"])
        df["upload_date"] = pd.to_datetime(df["upload_date"])
        return df.astype(dtypes)

    def _add_timezone(self, time):
        return [utc.replace(tzinfo=tz.gettz('UTC')) for utc in time]

    def change_timezone(self, timezone: str):
        to_zone = tz.gettz(timezone)

        for key in self.data.keys():
            time = self.data[key].index.to_list()
            self.data[key].index = [t.astimezone(to_zone) for t in time]

        return self

    def _json_to_dict(self, file_id: int) -> pd.DataFrame:
        try:
            url = f"https://tolnet.larc.nasa.gov/api/data/json/{file_id}"
            response = requests.get(url).json()
        except:
            print(f"Error with pulling {file_id}")
        return response

    def _json_to_curtain(self) -> pd.DataFrame:

        for key in self.data.keys():
            response = self.data[key]
            data = np.array(response["value"]["data"], dtype=float)
            time = np.array(response["datetime"]["data"])
            alt = np.array(response["altitude"]["data"], dtype=float)

            dataset = pd.DataFrame(data=data, index=time, columns=alt)
            dataset.index = pd.to_datetime(dataset.index)
            dataset.index = TOLNet()._add_timezone(dataset.index.to_list())
            self.data[key] = dataset

        return self
    
    def _unpack_data(self, meta_data):
        df = pd.DataFrame(meta_data["value"]["data"], 
                          columns = meta_data["altitude"]["data"],
                          index = pd.to_datetime(meta_data["datetime"]["data"])
                          )
        return df


    def import_data_json(self, min_date, max_date, **kwargs):
        self.files = self.get_files_list(min_date, max_date)
        file_info = filter_files(self.files).daterange(**kwargs).instrument_group(**kwargs).product_type(**kwargs).file_type(**kwargs).processing_type(**kwargs).df
        if file_info.size == self.files.size:
            prompt = input("You are about to download ALL TOLNet JSON files available... Would you like to proceed? (yes | no)")
            if prompt.lower() != "yes":
                return
        self.data = {}; self.meta_data = {}
        for file_name, file_id in tqdm(zip(file_info["file_name"], file_info["id"]), total=len(file_info)):
            self.meta_data[file_name] = self._json_to_dict(file_id)
            self.data[file_name] = self._unpack_data(self.meta_data[file_name])
        return self
    
    def _import_data_json(self, min_date, max_date, **kwargs):
        
        def process_file(file_name, file_id):
            meta_data = self._json_to_dict(file_id)
            data = self._unpack_data(meta_data)
            return file_name, meta_data, data
        
        self.files = self.get_files_list(min_date, max_date)
        file_info = filter_files(self.files).daterange(**kwargs).instrument_group(**kwargs).product_type(**kwargs).file_type(**kwargs).processing_type(**kwargs).df
    
        if file_info.size == self.files.size:
            prompt = input("You are about to download ALL TOLNet JSON files available... Would you like to proceed? (yes | no)")
            if prompt.lower() != "yes":
                return
    
        self.data = {}
        self.meta_data = {}
        
        
        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_to_file = {
                executor.submit(process_file, file_name, file_id): file_name
                for file_name, file_id in zip(file_info["file_name"], file_info["id"])
            }
    
            for future in tqdm(as_completed(future_to_file), total=len(future_to_file)):
                file_name = future_to_file[future]
                try:
                    file_name, meta_data, data = future.result()
                    
                    key = (meta_data["fileInfo"]["instrument_group_name"], 
                           meta_data["fileInfo"]["processing_type_name"])
                    
                    if key not in self.data.keys() or self.meta_data.keys(): 
                        self.data[key] = {}
                        self.meta_data[key] = {}
                        
                    self.data[key][file_name] = data
                    self.meta_data[key][file_name] = meta_data

                except Exception as e:
                    print(f"Error processing file {file_name}: {e}")
    
        return self

    

    @staticmethod
    def O3_curtain_colors():

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

    def tolnet_curtains(self, smooth: bool=True, timezone: int =None, **kwargs):
        """


        Parameters
        ----------
        smooth : BOOL, optional
            DESCRIPTION. The default is True.
        timezone : INT, optional
            DESCRIPTION. The default is None.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        
        inst_grp_names = self.instrument_groups["instrument_group_name"].to_list()
        
        group_names = []
        
        for name in self.meta_data.keys():
            group_name = self.meta_data[name]["fileInfo"]["instrument_group_name"]
            if group_name not in group_names:
                group_names.append(group_name)
            
        
        # if meta_data["fileInfo"]["insturment_group_name"] not in inst_grp_names:
        #     self.data["instrument_groups"].append(meta_data["fileInfo"]["insturment_group_name"])
                        
                        
        fig = plt.figure(figsize=(15, 8))
        ax = plt.subplots(layout="tight")
        # fig, ax = plt.subplot_mosaic([[x] for x in group_names], 
        #                              figsize=(15, 25), 
        #                              layout="tight")
        
        ncmap, nnorm = self.O3_curtain_colors()

        for name in self.data.keys():
            self.data[name] = self.data[name].fillna(value=np.nan)
            X, Y, Z = (self.data[name].index, self.data[name].columns, self.data[name].to_numpy().T,)
            gn = self.meta_data[name]["fileInfo"]["instrument_group_name"]
            im = ax[gn].pcolormesh(X, Y, Z, cmap=ncmap, norm=nnorm, shading="nearest")

            cbar = fig.colorbar(im, ax=ax[gn], pad=0.01, ticks=[0.001, *np.arange(10, 101, 10), 200, 300])
            cbar.set_label(label='Ozone ($ppb_v$)', size=16, weight="bold")
    
            # if "title" in kwargs.keys():
            #     plt.title(kwargs["title"], fontsize=18)
            # else: plt.title(r"$O_3$ Mixing Ratio Profile ($ppb_v$)", fontsize=20)
    
            if "ylabel" in kwargs.keys():
                ax[gn].set_ylabel(kwargs["ylabel"], fontsize=18)
            else: ax[gn].set_ylabel("Altitude (km AGL)", fontsize=18)
    
            if "xlabel" in kwargs.keys():
                ax[gn].set_xlabel(kwargs["xlabel"], fontsize=20)
            else: ax[gn].set_xlabel("Datetime (UTC)", fontsize=18)
    
            if "xlims" in kwargs.keys():
                lim = kwargs["xlims"]
                lims = [np.datetime64(lim[0]), np.datetime64(lim[-1])]
                ax[gn].set_xlim(lims)
    
            if "ylims" in kwargs.keys():
                ax[gn].set_ylim(kwargs["ylims"])
    
            if "yticks" in kwargs.keys():
                ax[gn].set_yticks(kwargs["yticks"], fontsize=20)
    
            if "surface" in kwargs.keys():
                X, Y, C = kwargs["surface"]
                ax.scatter(X, Y, c=C, cmap=ncmap, norm=nnorm)
    
            if "sonde" in kwargs.keys():
                X, Y, C = kwargs["sonde"]
                ax.scatter(X, Y, c=C, cmap=ncmap, norm=nnorm)
    
            converter = mdates.ConciseDateConverter()
            munits.registry[datetime.datetime] = converter
    
            ax[gn].xaxis_date(timezone)
    
            # fonts
            plt.setp(ax[gn].get_xticklabels(), fontsize=16)
            plt.setp(ax[gn].get_yticklabels(), fontsize=16)
            cbar.ax.tick_params(labelsize=16)

        # plt.tight_layout()

        if "savefig" in kwargs.keys():
            plt.savefig(f"{kwargs['savefig']}", dpi=600)

        plt.show()

        return self


#%% Example
date_start = "2023-08-08"
date_end = "2023-08-11"


if __name__ == "__main__":
    tolnet = TOLNet()
    print("Created TOLNET intance")
    
    # data = tolnet.import_data_json(min_date="2023-07-01", max_date="2023-08-31", product_type=[4])
    # data = tolnet._import_data_json(min_date="2023-08-08", max_date="2023-08-11", 
    #                                product_type=[4]).tolnet_curtains()
    print(f"Retrieving all HIRES files from {date_start} to {date_end} that were centrally processed:")
    data = tolnet._import_data_json(min_date=date_start, max_date=date_end, product_type=[4])
    # data.tolnet_curtains()
    
    
    # test = tolnet.get_files_list(min_date="2023-07-01", max_date="2023-08-31") 
#%% Notes

""" Tasks For Arthus


"""