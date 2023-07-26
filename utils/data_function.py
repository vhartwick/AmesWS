import pandas as pd
import xarray as xr
import numpy as np
import plotly.express as px

def var_data():

   # define datafram for variable options based on variable (e.g. 'Ts' can't do 2D lat/altitude
   d = {'variable':['ts','ts','ts','ts','ts','ts','ts','ts',
                   'ps','ps','ps','ps','ps','ps','ps','ps',
                   'temp','temp','temp','temp','temp','temp','temp','temp','temp','temp',
                   'ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp','ucomp',
                   'vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp','vcomp'],

        'unit': ['[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]',
                 '[Pa]','[Pa]','[Pa]','[Pa]','[Pa]','[Pa]','[Pa]','[Pa]',
                 '[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]','[K]',
                 '[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]',
                 '[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]','[m/s]'],
 
        'plot-type': ['2D_lon_lat','2D_time_lat','2D_time_lon','1D_time','1D_lat','1D_lon','1D_diurn','1D_daily',
                      '2D_lon_lat','2D_time_lat','2D_time_lon','1D_time','1D_lat','1D_lon','1D_diurn','1D_daily',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev',
                      '2D_lon_lat','2D_lat_lev','2D_lon_lev','2D_time_lat','2D_time_lon','2D_time_lev','1D_time','1D_lat','1D_lon','1D_lev'],

        'label':['Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]','Surface Temperature [K]',
                 'Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]','Surface Pressure [Pa]',
                 'Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]','Temperature [K]',
                 'Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]','Zonal Wind [m/s]',
                 'Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]','Meridional Wind [m/s]'],

        'rdims':[['time','time_of_day_12'],['lon','time_of_day_12'],['lat','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lat','time'],['lon','lat','time'],
                ['time','time_of_day_12'],['lon','time_of_day_12'],['lat','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lat','time'],['lon','lat','time'],
                ['lev','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','time_of_day_12'],['lat','lev','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','time_of_day_12'],['lon','lev','time','time_of_day_12'],['lat','lev','time','time_of_day_12'],['lon','lat','time','time_of_day_12'],
                ['lev','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','time_of_day_12'],['lat','lev','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','time_of_day_12'],['lon','lev','time','time_of_day_12'],['lat','lev','time','time_of_day_12'],['lon','lat','time','time_of_day_12'],
                ['lev','time','time_of_day_12'],['lon','time','time_of_day_12'],['lat','time','time_of_day_12'],['lon','lev','time_of_day_12'],['lat','lev','time_of_day_12'],['lon','lat','time_of_day_12'],['lon','lat','lev','time_of_day_12'],['lon','lev','time','time_of_day_12'],['lat','lev','time','time_of_day_12'],['lon','lat','time','time_of_day_12']],

        'dimx':['lon','time','time','time','lat','lon','time_of_day_12','time_of_day_12',
                'lon','time','time','time','lat','lon','time_of_day_12','time_of_day_12',
                'lon','lat','lon','time','time','time','time','lat','lon','lev',
                'lon','lat','lon','time','time','time','time','lat','lon','lev',
                'lon','lat','lon','time','time','time','time','lat','lon','lev'],
           
        'dimy':['lat','lat','lon','NaN','NaN','NaN','NaN','NaN',
                'lat','lat','lon','NaN','NaN','NaN','NaN','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','NaN',
                'lat','lev','lev','lat','lon','lev','NaN','NaN','NaN','NaN'],

        'xaxis_name':['Longitude','Ls','Ls','Ls','Latitude','Longitude','Local Time','Local Time',
                      'Longitude','Ls','Ls','Ls','Latitude','Longitude','Local Time','Local Time',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure',
                      'Longitude','Latitude','Longitude','Ls','Ls','Ls','Ls','Latitude','Longitude','Pressure'],

        'yaxis_name':['Latitude','Latitude','Longitude','NaN','NaN','NaN','NaN','NaN',
                      'Latitude','Latitude','Longitude','NaN','NaN','NaN','NaN','Nan',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN',
                      'Latitude','Pressure','Pressure','Latitude','Longitude','Pressure','NaN','NaN','NaN','NaN'],

        'hover2': [['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],['lev','temp'],
                  ['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],['lev','ucomp'],
                  ['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp'],['lev','vcomp']],   

        'cmap': ['Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel','Oryel',
                 'RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r',
                 'RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r','RdBu_r',],
        }
   df = pd.DataFrame(data=d)
   return df


def plotting_options():

   d = {'dim':['lon','lat','time','time_of_day_12','pstd','zstd','zagl'],
        'range': [[0,360],[-90,90],[0,360],[0,24],[2.845,-2],[0,110],[0,110]],
        'tick': [60,30,60,2,0.5,10,10],
        'unit': ['[°E]', '[°N]', '[°Ls]','[LT]','[Pa]','[km]','[km]'],
       }
   dp = pd.DataFrame(data=d)
   return dp

def variable_list():
   variable_list = [['ts','ps','temp','ucomp','vcomp'],
                    ['ts','ps'],
                    ['temp','ucomp','vcomp']]
   return variable_list

def file_options():
   # Dictioray of Text Options for different file types
   file_options = {
        "sim1": {
           "name": "Data Release 1 (c) Kahre+2023",
           "spatial_resolution": "2x2",
           "vertical_resolution": "56",
           "vertical_grid":"sigma hybrid pressure grid",
           "dust_scenario":"a prescribed background dust climatology (citation)",
           "water_scenario":"The model is dry",
           "aerosol_scenario":"Description of tracers",
           "rt_scenario": "Description of RT",
        },
        "atmos_ave": "Model results are averaged over 5 sols",
        "atmos_diurn": " Model results are averaged over 5 sols and discretized into 2 hour increments",
        "atmos_daily": "No temporal averaging is performed on model output",
        "pstd": 'Vertical interpolation to a 44 level pressure grid [1000-0.00001Pa] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing',
        "zagl": "Vertical interpolation to a 42 level altitude grid [0-13km] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing.",
        "zstd": "Vertical interpolation to a 48 level altitude grid [-7.5-13km] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."}
   return file_options
