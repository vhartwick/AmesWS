#================================================================================
# Callback to Generate Descriptive Plot Title
#================================================================================
from index import app
from dash.dependencies import Input, Output, State
from utils import data_function as df
import xarray as xr
import numpy as np
from utils import common_functions as cf

from utils import common_functions as cf
from utils import data_function as df
import xarray as xr
from pathlib import Path


# Load Variable Data
dv = df.var_data() 

# Load Plotting Options
dp = df.plotting_options()

@app.callback(
    [Output("modal-txt","children"),
    Output("fig-title","children")],
    Input("btn-doit-txt","n_clicks"),
    [State("plot-type-dropdown", "value"),
    State("model-dropdown", "value"),
    State("variable1-dropdown", "value"),
    State("variable2-dropdown", "value"),
    State("variable3-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),
    State("tod-input", "value")],
    prevent_initial_call=True,
)

def user_input_text(doit_clicks,plot_input,model_input,var1_input,var2_input,var3_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

    # SPECIFY FILE PATH BASED ON TOD_INPUT, VCORDS_INPUT
    f_path = cf.file_path(model_input,plot_input,tod_input,vcords_input)
    
    # DESCRIPTION OF FILE 
    # text for each model scenario, including citation, dust configuration, RT aerosols,
    # water cycle, model topo, etc etc
    # based on f_path : temporal averaging (5 sol diurnal, 5 sol 1 hour, instantaneous)
    # based on vcords_input : description of vertical interpolation & link to CAP
    
    #file_options = {"sim1":"This plot was generated using data from the NASA Ames FV3 Mars Global Climate Model, Data Release 1 (c) Kahre+2023 (link). The full data is archived on the NASA Planetary Science (?) Data Portal and can be accessed and downloaded at the following link. The model scenario has 2x2 degree lat/lon resoltion with 56 vertical layers on a sigma hybrid pressure grid (Pa range) and includes a prescribed background dust climatology (citation). The model is dry. Extra relevant descriptions. A full description of the model configuration and details of the physics can be found in Kahre+2023 and the NASA Ames FV3 User Manual (link)."
     #    "atmos_ave": "Model results are averaged over 5 sols."
     #    "atmos_diurn": " Model results are averaged over 5 sols in 1 hour increments."
     #    "atmos_daily": "No temporal averaging is performed on model output."
     #    "pstd": "Vertical interpolation to a X level pressure grid was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."
     #    "zagl": "Vertical interpolation to a X level altitude grid [m] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."
     #    "zstd": "Vertical interpolation to a X level altitude grid [m] was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."}

    simulation = "Data Release 1, (c) Kahre+2023 (link)"
    spatial_resolution = "2x2"
    vertical_resolution = "56"
    vertical_grid = "sigma hybrid pressure grid (#-# Pa)"
    dust_scenario = "a prescribed background dust climatology (citation)"
    water_scenario = "The model is dry"
    aerosol_scenario = "Description of tracers"
    rt_scenario = "Description of RT"
    time_averaging = "Model results are averaged over 5 sols"
    vertical_interpolation = "Vertical interpolation to a X level pressure grid was performed using the Community Analysis Pipeline. See the CAP github for a complete description of vertical processing."

    file_description_text = f"This plot was generated using data from the NASA Ames FV3 Mars Global Climate Model, {simulation}. The full data is archived on the NASA Planetary Science (?) Data Portal and can be accessed and downloaded at the following link. The model scenario has {spatial_resolution} degree lat/lon resolution with {vertical_resolution} vertical layers on a {vertical_grid}, and includes {dust_scenario}. {water_scenario}. {aerosol_scenario}. {rt_scenario}. A full description of the model configuration and details of the physics can be found in Kahre+2023 and the NASA Ames FV3 User Manual (link). {time_averaging}. {vertical_interpolation}."

    # DESCRIPTION OF PLOT
    # list user inputs for lat, lon, lev, areo, time of day in words (as in title) & list
    
    # intro text describing nearest value selection (varies with resolution)
    with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value1=f.lat.sel(lat=-30,method='nearest').values
                nearest_value2=f.lat.sel(lat=30,method='nearest').values

    # find the nearest values to user inputs and generate the plot title
    
    # variable list
    var_value = var1_input #+ ', ' + var2_input + ', ' + var3_input
    # remove "None"(s)
    if "None" in var_value:
       var_value = var_value.replace(', None ','')

    # plot_title
    text_options = [['Zonal Average', ''],
                   ['Meridional Average', ''],
                   ['Column Integrated', ''], 
                   ['Annual Average', ''],
                   ['Diurnal Average', '']]

    unit_options = ['E','N','','Ls','LT']

    
    # select options based on user input
    rlist = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'rdims'].values[0]

    # Then remove levels as necessary
    rlist = [o for o in rlist]
       
    # go through rdmis assuming order lon,lat, lev, time, time_of_day_12
    text = []
 
    # first add variable names
    text += [var_value]
    for i in rlist:    # i dimension name, dim_input = "all, int, or range"

       # check dimension and go to appropriate option in text_options (e.g. lon == index[0])   
       dim_index = 0 if i=='lon' \
          else (1 if i=='lat' else (3 if i=='time' else (2 if i=='lev' else 4)))

       # grab user input for each extra dimension
       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if user_input == 'ALL':
          text += [text_options[dim_index][0]]

       elif "," in user_input:   # range of values selected
          dim_split = str(user_input).split(",")
          # check for unit
          if i == 'lev':
             unit = 'Pa' if vcords_input == 'pstd' else 'm'
             dim = vcords_input
             with xr.open_dataset(f_path,decode_times=False) as f:
                text += ['@ ' + text_options[dim_index][1]+f[dim].sel(**{dim:dim_split[0]},method='nearest').values+'-'+ f[dim].sel(**{dim:dim_split[1]},method='nearest').values + unit]
          elif i == 'time':
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value1=f[i].sel(**{i:dim_split[0]},method='nearest').values
                nearest_value2=f[i].sel(**{i:dim_split[1]},method='nearest').values
             text += ['@ ' + text_options[dim_index][1]+str(nearest_value1%360)+'-'+str(nearest_value2%360) + unit_options[dim_index]]

          else:
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value1=f[i].sel(**{i:dim_split[0]},method='nearest').values
                nearest_value2=f[i].sel(**{i:dim_split[1]},method='nearest').values
             text += ['@ ' + text_options[dim_index][1]+str(nearest_value1)+'-'+str(nearest_value2) + unit_options[dim_index]]
       else: # single value selected
          # check for unit
          if i == 'lev':
             unit = 'Pa' if vcords_input == 'pstd' else 'm'
             dim = vcords_input
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value=f[dim].sel(**{dim:user_input},method='nearest').values
                text += ['@ ' + text_options[dim_index][1]+str(nearest_value) + unit] 
          elif i == 'time':
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value=f[i].sel(**{i:user_input},method='nearest').values
             text += ['@ ' + text_options[dim_index][1]+str(nearest_value%360) + unit_options[dim_index]]


          else:
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value=f[i].sel(**{i:user_input},method='nearest').values
             text += ['@ ' + text_options[dim_index][1]+str(nearest_value) + unit_options[dim_index]]

    # order options (average first, if more than one average combine)
    #e.g. Global Diurnal Average @ X Pa
    text = sorted(text, key=lambda x: 'Average' in x, reverse=True)
    
    # Join the strings into a single text string
    text = ' '.join(text)

    # If both "Meridional Average" and "Zonal Average" appear, replace with "Global"
    if "Meridional Average" and "Zonal Average" in text:
       text = text.replace('Meridional Average ','')
       text = text.replace('Zonal Average','Global') 
    
    # If the word "Average" appears more than once, remove the first instance
    num_averages = text.count("Average")  # Count the number of occurrences of "Average"
    if num_averages > 1:
       last_average_index = text.rindex("Average")  # Find the index of the last occurrence of "Average"
       text = text.replace("Average", "", num_averages - 1)  # Replace all but the last occurrence of "Average"
    
    # If "@" appears more than once, remove the all but the first insttance
    if text.count('@') > 1:
       parts = text.split('@', 1)  # split the string at the first "@" character
       text = parts[0]+'@' + parts[1].replace('@', '')  # join the parts back together, keeping only the first "@"

    plot_title = text

    # Defaults
    lat_value = "ALL"
    lon_value = "ALL"
    lev_value = "100 Pa"
    areo_value = "ALL"
    tod_value = "ALL"     
    user_input_text = f"The plot/dataset shows the {plot_title} based on the following user inputs. Values listed represent the closest value in the model output. For example, if the user specified the latitude range 30S,30N, the plot will use model data between {nearest_value1}S and {nearest_value2}N. \n \n \033[1mVariable(s):\033[0m {var_value} \n \033[1mLatitude:\033[0m {lat_value} \n \033[1mLongitude:\033[0m {lon_value} \n \033[1mAtmospheric Level:\033[0m {lev_input} \n \033[1mSolar Longitude (Ls):\033[0m {areo_value} \n \033[1mLocal Time:\033[0m {tod_input}"
    
    
     # Join the strings into a single text string
    final_text = file_description_text + user_input_text

    return plot_title, final_text

