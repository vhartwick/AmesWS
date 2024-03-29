import pandas as pd
import xarray as xr
import numpy as np
import json
from utils import data_function as df


# Load Database
dv = df.var_data()

def fv3_data():
   dataDIR = '/Users/vhartwic/Desktop/amesWS/Data/00668.atmos_average_pstd.nc'
   ds = xr.open_dataset(dataDIR, decode_times=False)
   ds_sub = ds.ts.mean('time')
   df =ds_sub.to_pandas()
   return df


def file_path(model_input,plot_input,tod_input,vcords_input):
  if tod_input != 'ALL' and plot_input != '1D_daily':  # load atmos_diurn
     if vcords_input == "pstd" : # load pstd
       f_path = f'/Users/vhartwic/Desktop/amesWS/{model_input}/Data/02004.atmos_diurn_T_pstd.nc'
     elif vcords_input == "zagl":  # load zagl
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_diurn_T_zagl.nc'
     else:  # load atmos_average_zstd
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_diurn_T_zstd.nc'
  elif plot_input == '1D_daily':  # load atmos_daily
     if vcords_input == "pstd" : 
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_daily_extract.nc'
     elif vcords_input == "zagl":  # load zagl
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_daily_extract.nc'
     else:  # load atmos_average_zstd
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_daily_extract.nc'
  else: # load atmos_average
     if vcords_input == "pstd" : # load atmos_average_pstd
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_average_extract_pstd.nc'
     elif vcords_input == "zagl":  # load atmos_average_zagl
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_average_extract_zagl.nc'
     else:  # load atmos_average_zstd
       f_path = f'/Users/vhartwic/Desktop/amesWS/Data/{model_input}/02004.atmos_average_extract_zstd.nc'
  
  return f_path

def load_dims(model_input,plot_input,var_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

  # SPECIFY FILE PATH BASED ON MODEL_INPUT, TOD_INPUT, PLOT_INPUT, VCORDS_INPUT
  f_path = file_path(model_input,plot_input,tod_input,vcords_input)

  # LOAD DATA
  # order : plot_input, array dimensions, specified lat,lon,lev,areo

  # reset saved variables
  dim1,dim2,time_dim,vert_dim = None,None,None,None

  with xr.open_dataset(f_path,decode_times=False) as f:

     # REPLACE TIME COORD WITH AREO
     areo_coord = np.array(f.areo[:,0]%360)
     f.coords['time'] = areo_coord

     # DEFINE DIMENSIONS & VARIBLES
     dim1,dim2,time_dim,vert_dim = define_dims(f,dv,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input)

     # return the loaded variables in the specified format
     return json.dumps(dim1.to_dict()), json.dumps(dim2.to_dict()), json.dumps(time_dim.to_dict()), json.dumps(vert_dim.to_dict())

def load_data(model_input,plot_input,var_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

  # SPECIFY FILE PATH BASED ON MODEL_INPUT, PLOT_INPUT, TOD_INPUT, VCORDS_INPUT
  f_path = file_path(model_input,plot_input,tod_input,vcords_input)

  # LOAD DATA
  # order : plot_input, array dimensions, specified lat,lon,lev,areo

  # reset saved variables
  var = []

  with xr.open_dataset(f_path,decode_times=False) as f:
   
     # REPLACE TIME COORD WITH AREO
     areo_coord = np.array(f.areo[:,0]%360)
     f.coords['time'] = areo_coord

     # DEFINE VARIBLES
     if "1D" in str(plot_input):
        var = define_1D(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input)
     else:
        var = define_2D(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input)

     # return the loaded variables in the specified format
     return json.dumps(var.to_dict()) 

def select_timeseries_hover_var(dv,plot_input,var1_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover):

    # FIRST LOAD DATA
    # SPECIFY FILE PATH BASED ON MODEL_INPUT, PLOT_INPUT, TOD_INPUT, VCORDS_INPUT
    f_path = file_path(model_input,plot_input,tod_input,vcords_input)
    
    # LOAD DATA   
    # reset saved variables
    hover_var = [] 

    with xr.open_dataset(f_path,decode_times=False) as f:

       # REPLACE TIME COORD WITH AREO
       areo_coord = np.array(f.areo[:,0]%360)
       f.coords['time'] = areo_coord

       # FIND DIMENSION NAME
       dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
       dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

       # MAKE LIST OF ADDITIONAL DIMENSIONS THAT MUST BE PROCESSED
       rlist = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx, dimy]] 
       # remove tod dimension option if not in diurn file, and lev3 if plotting "2D"
       rlist = [o for o in rlist if o != 'time_of_day_12' and tod_input == "ALL"]

       # FOR LEV MAKE SOME ADDITIONAL CHECKS
       if 'lev' in str(dimy):
          dimy=vcords_input
       else:
          dimy=dimy

       # GET VARIABLE NAME & EXTRACT
       hover_var_name = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'hover1'].values[0]
       hover_var_name = hover_var_name[1]
       hover_var = f[hover_var_name]       
      
       # rename lev to vcords in rlist
       rlist = [o.replace('lev', vcords_input) for o in rlist]

       for i in rlist:  # i dimension name, dim_input = "all, int, or range"
 
          # grab the user input
          user_input = lon_input if i=='lon' \
            else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

          if user_input == 'ALL':
             if i != 'lat':
                hover_var = hover_var.mean(i)
             else:
                weights= np.cos(np.deg2rad(f.lat))
                hover_var = hover_var.weighted(weights).mean(i)

          elif "," in user_input:   # range of values selected
             if i != "lat":
                dim_split = str(user_input).split(",")
                hover_var = hover_var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).mean(i)
             else:  # if dimension is latitude need to do a weighted mean
                dim_split = str(user_input).split(",")
                weights = np.cos(np.deg2rad(f.lat))
                hover_var = hover_var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).weighted(weights).mean(i)
          else: # single value selected
             hover_var = hover_var.sel(**{i:user_input},method='nearest')
 
       # IDENTIFY MIN MAX
       hv_min,hv_max = hover_var.min(),hover_var.max()

       # SELECT VARIABLE BASED ON HOVER DATA  (DON'T REMOVE DIMX IF == TIME)
       if dimx == 'time':
          hover_var = hover_var.sel(**{dimy:dimy_hover},method='nearest')
       else:
          hover_var = hover_var.sel(**{dimx:dimx_hover,dimy:dimy_hover},method='nearest')

       return hv_min,hv_max,hover_var

def select_vertical_profile_var(dv,plot_input,var1_input,model_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover):
    
    # FIRST LOAD DATA
    # SPECIFY FILE PATH BASED ON MODEL_INPUT, PLOT_INPUT, TOD_INPUT, VCORDS_INPUT
    f_path = file_path(model_input,plot_input, tod_input,vcords_input)

    # reset saved variables
    hover_var = []

    with xr.open_dataset(f_path,decode_times=False) as f:

       # REPLACE TIME COORD WITH AREO
       areo_coord = np.array(f.areo[:,0]%360)
       f.coords['time'] = areo_coord

       # FIND DIMENSION NAME
       dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
       dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

       # MAKE LIST OF ADDITIONAL DIMENSIONS THAT MUST BE PROCESSED
       # lev is not included becasue it is your y-axis
       rlist = [o for o in ['lon', 'lat', 'time', 'time_of_day_12'] if o not in [dimx, dimy]]
       # remove tod dimension option if not in diurn file, and lev3 if plotting "2D"
       rlist = [o for o in rlist if o != 'time_of_day_12' and tod_input == "ALL"]

       # GET VARIABLE NAME & EXTRACT
       hover_var_name = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'hover2'].values[0]
       hover_var_name = hover_var_name[1]
       hover_var = f[hover_var_name]

       for i in rlist:  # i dimension name, dim_input = "all, int, or range"
          
          # grab the user input
          user_input = lon_input if i=='lon' \
            else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

          # change vertical coordinate name based on user input
          if i == 'lev':
             i = vcords_input

          if user_input == 'ALL':
             if i != 'lat':
                hover_var = hover_var.mean(i)
             else:
                weights= np.cos(np.deg2rad(f.lat))
                hover_var = hover_var.weighted(weights).mean(i)

          elif "," in user_input:   # range of values selected
             if i != "lat":
                dim_split = str(user_input).split(",")
                hover_var = hover_var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).mean(i)
             else:  # if dimension is latitude need to do a weighted mean
                dim_split = str(user_input).split(",")
                weights = np.cos(np.deg2rad(f.lat))
                hover_var = hover_var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).weighted(weights).mean(i)

                #int(dim_split[0]),int(dim_split[1]))}).weighted(weights).mean(i)
          else: # single value selected
             hover_var = hover_var.sel(**{i:user_input},method='nearest')

       # IDENTIFY MIN MAX
       hv_min,hv_max = hover_var.min(),hover_var.max()
 
       # SELECT VARIABLE BASED ON HOVER DATA  (DON'T REMOVE DIMY IF == LEV)
       if dimy == 'lev':
          hover_var = hover_var.sel(**{dimx:dimx_hover},method='nearest')
       else:
          hover_var = hover_var.sel(**{dimx:dimx_hover,dimy:dimy_hover},method='nearest')

    return hv_min,hv_max,hover_var

def define_2D(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input):

    # FIND DIMENSION NAME
    dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
    dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

    # MAKE LIST OF ADDITIONAL DIMENSIONS THAT MUST BE PROCESSED
    rlist_var = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx, dimy] and not ('Surface' in var_input and o == 'lev')]
    # remove tod dimension option if not in diurn file, and lev3 if plotting "2D"
    rlist_var = [o for o in rlist_var if o != 'time_of_day_12' and tod_input == "ALL"]
 

    # CHECK DIMENSION USER INPUTS
    dim1_input = lon_input if dimx=='lon' \
         else (lat_input if dimx=='lat' else (areo_input if dimx=='time' else (lev_input if dimx=='lev' else tod_input)))
    dim2_input = lon_input if dimy=='lon' \
         else (lat_input if dimy=='lat' else (areo_input if dimy=='time' else (lev_input if dimy=='lev' else tod_input)))

  
    # CHANGE LEV TO PSTD, ZAGL OR ZSTD
    if dimx=='lev':
       dimx=vcords_input
    if dimy=='lev': 
       dimy=vcords_input

    # NOW FIND VARIABLE
    var = dv.loc[(dv['label']==str(var_input)),'variable'].values[0]  
    var = f[var]

    if dim1_input !="ALL":
       dim_split = str(dim1_input).split(",")
       var = var.sel(**{dimx:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})

    if dim2_input !="ALL":
       dim_split = str(dim2_input).split(",")
       var = var.sel(**{dimy:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})

    for i in rlist_var:    # i dimension name, dim_input = "all, int, or range"

       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if 'lev' in str(i):  # replace lev with pstd, zstd, zagl
          i = vcords_input

       if user_input == 'ALL':
          if i != 'lat':
             var = var.mean(i)
          else:
             weights= np.cos(np.deg2rad(f.lat))
             var = var.weighted(weights).mean(i)

       elif "," in user_input:   # range of values selected
          if i != "lat":
             dim_split = str(user_input).split(",")
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).mean(i)
          else:  # if dimension is latitude need to do a weighted mean
             dim_split = str(user_input).split(",")
             weights = np.cos(np.deg2rad(f.lat))
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).weighted(weights).mean(i)
       else: # single value selected
          var = var.sel(**{i:user_input},method='nearest')

    return var


def define_dims(f,dv,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input):

    # FIND DIMENSION NAME 
    dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
    dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

    # FOR 1D PLOTS SET DIMX = DIMY
    if dimy == "NaN":
       dimy = dimx

    # CHANGE LEV TO PSTD, ZAGL OR ZSTD
    #if dimx=='lev':
    #   dimx=vcords_input
    #if dimy=='lev': 
    #   dimy=vcords_input
       
    # LOOK AT RELEVANT USER RANGE INPUT & DEFINE DIMENSIONS
    #dim1,dim2 = f[dimx],f[dimy]
    #time_dim,vert_dim = f.time,f[vcords_input]
    
    # CHECK DIMENSION USER INPUTS
    dim1_input = lon_input if dimx=='lon' \
         else (lat_input if dimx=='lat' else (areo_input if dimx=='time' else (lev_input if dimx=='lev' else tod_input)))
    dim2_input = lon_input if dimy=='lon' \
         else (lat_input if dimy=='lat' else (areo_input if dimy=='time' else (lev_input if dimy=='lev' else tod_input)))
    
    # CHANGE LEV TO PSTD, ZAGL OR ZSTD
    if dimx=='lev':
       dimx=vcords_input
    if dimy=='lev':
       dimy=vcords_input

    # LOOK AT RELEVANT USER RANGE INPUT & DEFINE DIMENSIONS
    dim1,dim2 = f[dimx],f[dimy]
    time_dim,vert_dim = f.time,f[vcords_input]
   
    if dim1_input !="ALL":
       dim_split = str(dim1_input).split(",")
       dim1 = dim1.sel(**{dimx:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})
    
    if dim2_input !="ALL":
       dim_split = str(dim2_input).split(",")
       dim2 = dim2.sel(**{dimy:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})

    return dim1, dim2, time_dim, vert_dim

def define_1D(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input):

    # FIND DIMENSION NAME
    dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]

    # MAKE LIST OF ADDITIONAL DIMENSIONS THAT MUST BE PROCESSED
    rlist_var = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o !=dimx and not ('Surface' in var_input and o == 'lev')]
    # remove tod dimension option if not in diurn file
    rlist_var = [o for o in rlist_var if o != 'time_of_day_12' and tod_input == "ALL"]

    # CHANGE LEV TO PSTD, ZAGL OR ZSTD
    if dimx=='lev':
       dimx=vcords_input
       
    # NOW FIND VARIABLE
    var = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var_input)),'variable'].values[0]  
    var = f[var]

    # SELECT VARIABLE BASED ON DIMENSION INPUTS
    dim1_input = lon_input if dimx=='lon' \
         else (lat_input if dimx=='lat' else (areo_input if dimx=='time' else (lev_input if dimx=='lev' else tod_input)))
    
    if dim1_input !="ALL":
       dim_split = str(dim1_input).split(",")
       var = var.sel(**{dimx:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})

    for i in rlist_var:    # i dimension name, dim_input = "all, int, or range"
      
       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if i == 'lev':  # replace lev with pstd, zstd, zagl
          i = vcords_input

       if user_input == 'ALL':
          if i != 'lat':
             var = var.mean(i)
          else:
             weights= np.cos(np.deg2rad(f.lat))
             var = var.weighted(weights).mean(i)

       elif "," in user_input:   # range of values selected
          if i != "lat":
             dim_split = str(user_input).split(",")
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).mean(i)
          else:  # if dimension is latitude need to do a weighted mean
             dim_split = str(user_input).split(",")
             weights = np.cos(np.deg2rad(f.lat))
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).weighted(weights).mean(i)
       else: # single value selected
          var = var.sel(**{i:user_input},method='nearest')
   
    return var

def load_column_data(plot_input,var_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

  # SPECIFY FILE PATH BASED ON MODEL_INPUT, PLOT_INPUT,TOD_INPUT, VCORDS_INPUT
  f_path = file_path(model_input,plot_input, tod_input,vcords_input)

  # LOAD DATA
  # order : plot_input, array dimensions, specified lat,lon,lev,areo

  # reset saved variables
  var = []

  with xr.open_dataset(f_path,decode_times=False) as f:
     # REPLACE TIME COORD WITH AREO
     areo_coord = np.array(f.areo[:,0]%360)
     f.coords['time'] = areo_coord

     # DEFINE VARIBLES
     if "1D" in str(plot_input):
        var = define_1D_col(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input)
     else:
        var = define_2D_col(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input)

     # return the loaded variables in the specified format
     return json.dumps(var.to_dict())

def define_1D_col(f,dv,var_input,plot_input,lon_input,lat_input,areo_input,vcords_input,lev_input,tod_input):

    # FIND DIMENSION NAME
    dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0] 
    dimy = 'lev'

    # MAKE LIST OF ADDITIONAL DIMENSIONS THAT MUST BE PROCESSED
    rlist_var = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx,dimy] and not ('Surface' in var_input and o == 'lev')]
    # remove tod dimension option if not in diurn file
    rlist_var = [o for o in rlist_var if o != 'time_of_day_12' and tod_input == "ALL"]
    
    # CHANGE LEV TO PSTD, ZAGL OR ZSTD
    if dimx=='lev':
       dimx=vcords_input
       
    # NOW FIND VARIABLE
    var = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var_input)),'variable'].values[0]  
    var = f[var]

    # SELECT VARIABLE BASED ON DIMENSION INPUTS
    dim1_input = lon_input if dimx=='lon' \
         else (lat_input if dimx=='lat' else (areo_input if dimx=='time' else (lev_input if dimx=='lev' else tod_input)))
    
    if dim1_input !="ALL":
       dim_split = str(dim1_input).split(",")
       var = var.sel(**{dimx:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))})

    for i in rlist_var:    # i dimension name, dim_input = "all, int, or range"

       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if i == 'lev':  # replace lev with pstd, zstd, zagl
          i = vcords_input

       if user_input == 'ALL':
          if i != 'lat':
             var = var.mean(i)
          else:
             weights= np.cos(np.deg2rad(f.lat))
             var = var.weighted(weights).mean(i)

       elif "," in user_input:   # range of values selected
          if i != "lat":
             dim_split = str(user_input).split(",")
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).mean(i)
          else:  # if dimension is latitude need to do a weighted mean
             dim_split = str(user_input).split(",")
             weights = np.cos(np.deg2rad(f.lat))
             var = var.sel(**{i:slice(min(int(dim_split[0]),int(dim_split[1])),max(int(dim_split[0]),int(dim_split[1])))}).weighted(weights).mean(i)
       else: # single value selected
          var = var.sel(**{i:user_input},method='nearest')
   
    return var

def find_nearest_value(f_path,i,user_input):

   nearest_value1, nearest_value2 = None, None 
  
   # range of values selected
   if "," in user_input:   # range of values selected
      dim_split = str(user_input).split(",")
      with xr.open_dataset(f_path,decode_times=False) as f:
         # REPLACE TIME COORD WITH AREO
         areo_coord = np.array(f.areo[:,0]%360)
         f.coords['time'] = areo_coord    
         nearest_value1 = f[i].sel(**{i:dim_split[0]}, method='nearest').values
         nearest_value2 = f[i].sel(**{i:dim_split[1]}, method='nearest').values
   # single value selected
   else:
      with xr.open_dataset(f_path,decode_times=False) as f:
         # REPLACE TIME COORD WITH AREO
         areo_coord = np.array(f.areo[:,0]%360)
         f.coords['time'] = areo_coord
         nearest_value1=f[i].sel(**{i:user_input},method='nearest').values

   return nearest_value1, nearest_value2
