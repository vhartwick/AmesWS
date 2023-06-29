import pandas as pd
import xarray as xr
import numpy as np
import plotly.express as px

def var_data():

   # define datafram for variable options based on variable (e.g. 'Ts' can't do 2D lat/altitude
   d = {'variable':['ts','ts','ts','ts','ts','ts','ts',
                   'ps','ps','ps','ps','ps','ps','ps',
                   'temp','temp','temp','temp','temp','temp','temp','temp','temp','temp','temp',
                   'ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp',
                   'vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp'],

        'unit': ['[K]','[K]','[K]','[K]','[K]','[K]','[K]',
                 '[Pa]','[Pa]','[Pa]','[Pa]','[Pa]','[Pa]','[Pa]',
                 '[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]',
                 '[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]',
                 '[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]'],
 
        'plot-type': ['2D_lon_lat','2D_time_lat','2D_time_lon','1D_time','1D_lat','1D_lon','1D_diurn',
                      '2D_lon_lat','2D_time_lat','2D_time_lon','1D_time','1D_lat','1D_lon','1D_diurn',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev','1D_diurn',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev','1D_diurn',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev','1D_diurn'],

        'label':['Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]',
                 'Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]',
                 'Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]',
                 'Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]',
                 'Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]'],

        'rdims':[['time','time_of_day_12'],['lon','time_of_day_12'],['lat','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lat','time'],
                ['time','time_of_day_12'],['lon','time_of_day_12'],['lat','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lat','time'],
                ['lev','lev2','lev3','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','lev2','lev3','time_of_day_12'],['lat','lev','lev2','lev3','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','lev2','lev3','time_of_day_12'],['lon','lev','lev2','lev3','time','time_of_day_12'],['lat','lev','lev2','lev3','time','time_of_day_12'],['lon','lat','time','time_of_day_12'],['lon','lat','lev','lev2','lev3','time'],
                ['lev','lev2','lev3','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','lev2','lev3','time_of_day_12'],['lat','lev','lev2','lev3','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','lev2','lev3','time_of_day_12'],['lon','lev','lev2','lev3','time','time_of_day_12'],['lat','lev','lev2','lev3','time','time_of_day_12'],['lon','lat','time','time_of_day_12'],['lon','lat','lev','lev2','lev3','time'],
                ['lev','lev2','lev3','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','lev2','lev3','time_of_day_12'],['lat','lev','lev2','lev3','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','lev2','lev3','time_of_day_12'],['lon','lev','lev2','lev3','time','time_of_day_12'],['lat','lev','lev2','lev3','time','time_of_day_12'],['lon','lat','time','time_of_day_12'],['lon','lat','lev','lev2','lev3','time']],

        'dimx':['lon','time','time','time','lat','lon','time_of_day_12',
                'lon','time','time','time','lat','lon','time_of_day_12',
                'lon','lat','lon','time','time','time','time','lat','lon','NaN','time_of_day_12',
                'lon','lat','lon','time','time','time','time','lat','lon','NaN','time_of_day_12',
                'lon','lat','lon','time','time','time','time','lat','lon','NaN','time_of_day_12'],
           
        'dimy':['lat','lat','lon','NaN','NaN','NaN','NaN',
                'lat','lat','lon','NaN','NaN','NaN','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','lev','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','lev','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','lev','NaN'],

        'xaxis_name':['Longitude','Ls','Ls','Ls','Latitude','Longitude','Local Time',
                      'Longitude','Ls','Ls','Ls','Latitude','Longitude','Local Time',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure','Local Time',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure','Local Time',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure','Local Time'],

        'yaxis_name':['Latitude','Latitude','Longitude','NaN','NaN','NaN','NaN',
                      'Latitude','Latitude','Longitude','NaN','NaN','NaN','NaN',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN','NaN',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN','NaN',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN','NaN'],

        'hover1': [['time','ts'],['time','ts'],['time','ts'],['time','ts'],['time','ts'],['time','ts'],['time','ts'],
                  ['time','ps'],['time','ps'],['time','ps'],['time','ps'],['time','ps'],['time','ps'],['time','ps'],
                  ['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],['time','temp'],
                  ['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],['time','ucomp'],
                  ['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp'],['time','vcomp']],
        'hover2': [['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],
                  ['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp']],   

        'cmap': ['Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r',
                 'RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r',],
        }
   df = pd.DataFrame(data=d)
   return df


def plotting_options():

   d = {'dim':['lon','lat','time','time_of_day_12','pstd','zstd','zagl'],
        'range': [[0,360],[-90,90],[0,360],[0,24],[2.845,-2],[0,120],[0,120]],
        'tick': [60,30,60,2,0.5,10,10],
        'unit': ['[°E]', '[°N]', '[°Ls]','[LT]','[Pa]','[m]','[m]'],
       }
   #d = {'dim':['lon','lat','time','time_of_day_12','lev'],
   #     'range': [[0,360],[-90,90],[0,360],[0,24],[[700,0.1],[0,120],[0,120]]],
   #     'tick': [60,30,60,2,[np.nan,10,10]],
   #    } 
   dp = pd.DataFrame(data=d)
   return dp

def variable_list():
   variable_list = [['ts','ps','temp','ucomp','vcomp'],
                    ['ts','ps'],
                    ['temp','ucomp','vcomp']]
   return variable_list


