import pandas as pd
import xarray as xr
import numpy as np
import plotly.express as px

def var_data():
   d = {'variable': ['temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'temp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'ucomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'vcomp', 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', 'ps', 'ts', 'ts', 'ts', 'ts', 'ts', 'ts', 'ts', 'ts'], 'unit': ['[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[m/s]', '[Pa]', '[Pa]', '[Pa]', '[Pa]', '[Pa]', '[Pa]', '[Pa]', '[Pa]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]', '[K]'], 'plot-type': ['2D_lon_lat', '2D_lat_lev', '2D_lon_lev', '2D_time_lat', '2D_time_lon', '2D_time_lev', '1D_time', '1D_lat', '1D_lon', '1D_lev', '2D_lon_lat', '2D_lat_lev', '2D_lon_lev', '2D_time_lat', '2D_time_lon', '2D_time_lev', '1D_time', '1D_lat', '1D_lon', '1D_lev', '2D_lon_lat', '2D_lat_lev', '2D_lon_lev', '2D_time_lat', '2D_time_lon', '2D_time_lev', '1D_time', '1D_lat', '1D_lon', '1D_lev', '2D_lon_lat', '2D_time_lat', '2D_time_lon', '1D_time', '1D_lat', '1D_lon', '1D_diurn', '1D_daily', '2D_lon_lat', '2D_time_lat', '2D_time_lon', '1D_time', '1D_lat', '1D_lon', '1D_diurn', '1D_daily'], 'label': ['Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Temperature [K]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Zonal Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Meridional Wind [m/s]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Pressure [Pa]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]', 'Surface Temperature [K]'], 'dimx': ['lon', 'lat', 'lon', 'time', 'time', 'time', 'time', 'lat', 'lon', 'lev', 'lon', 'lat', 'lon', 'time', 'time', 'time', 'time', 'lat', 'lon', 'lev', 'lon', 'lat', 'lon', 'time', 'time', 'time', 'time', 'lat', 'lon', 'lev', 'lon', 'time', 'time', 'time', 'lat', 'lon', 'time_of_day_12', 'time', 'lon', 'time', 'time', 'time', 'lat', 'lon', 'time_of_day_12', 'time'], 'dimy': ['lat', 'lev', 'lev', 'lat', 'lon', 'lev', 'NaN', 'NaN', 'NaN', 'NaN', 'lat', 'lev', 'lev', 'lat', 'lon', 'lev', 'NaN', 'NaN', 'NaN', 'NaN', 'lat', 'lev', 'lev', 'lat', 'lon', 'lev', 'NaN', 'NaN', 'NaN', 'NaN', 'lat', 'lat', 'lon', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'lat', 'lat', 'lon', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], 'xaxis_name': ['Longitude', 'Latitude', 'Longitude', 'Ls', 'Ls', 'Ls', 'Ls', 'Latitude', 'Longitude', 'Pressure', 'Longitude', 'Latitude', 'Longitude', 'Ls', 'Ls', 'Ls', 'Ls', 'Latitude', 'Longitude', 'Pressure', 'Longitude', 'Latitude', 'Longitude', 'Ls', 'Ls', 'Ls', 'Ls', 'Latitude', 'Longitude', 'Pressure', 'Longitude', 'Ls', 'Ls', 'Ls', 'Latitude', 'Longitude', 'Local Time', 'Ls', 'Longitude', 'Ls', 'Ls', 'Ls', 'Latitude', 'Longitude', 'Local Time', 'Ls'], 'yaxis_name': ['Latitude', 'Pressure', 'Pressure', 'Latitude', 'Longitude', 'Pressure', 'NaN', 'NaN', 'NaN', 'NaN', 'Latitude', 'Pressure', 'Pressure', 'Latitude', 'Longitude', 'Pressure', 'NaN', 'NaN', 'NaN', 'NaN', 'Latitude', 'Pressure', 'Pressure', 'Latitude', 'Longitude', 'Pressure', 'NaN', 'NaN', 'NaN', 'NaN', 'Latitude', 'Latitude', 'Longitude', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'Latitude', 'Latitude', 'Longitude', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'], 'hover2': [['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'ucomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'vcomp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp'], ['lev', 'temp']], 'cmap': ['Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'RdBu_r', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel', 'Oryel']}
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

def file_options():
   # Dictioray of Text Options for different file types
   file_options = {
        "sim1": {
           "name": "Data Release 1 (Kahre+2023)",
           "spatial_resolution": "2x2",
           "vertical_resolution": "56",
           "vertical_grid":"hybrid sigma pressure grid",
           "dust_scenario":"a prescribed background dust climatology",
           "water_scenario":"The model is dry",
           "aerosol_scenario":"Description of tracers",
           "rt_scenario": "Description of RT",
        },
        "atmos_ave": "Model results are averaged over 5 sols",
        "atmos_diurn": "Model results are averaged over 5 sols and discretized into 2 hour increments",
        "atmos_daily": "No temporal averaging is performed on model output",
        "pstd": 'Vertical interpolation to a 36 level pressure grid [1000-0.01Pa] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing',
        "zagl": "Vertical interpolation to a 34 level altitude grid [0-11km] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing.",
        "zstd": "Vertical interpolation to a 45 level altitude grid [-7-100km] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."}
   return file_options
