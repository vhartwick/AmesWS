#================================================================================
# Callback to Generate Descriptive Plot Title
#================================================================================
from index import app
from dash.dependencies import Input, Output, State
from utils import data_function as df
import xarray as xr
import numpy as np
from utils import common_functions as cf

# Load Variable Data
dv = df.var_data() 

# Load Plotting Options
dp = df.plotting_options()

@app.callback(
    Output("fig-title","children"),
    Input("figure_out","figure"),
    [State("plot-type-dropdown", "value"),
    State("model-dropdown", "value"),
    State("variable1-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),
    State("tod-input", "value")],
    prevent_initial_call=True,
)

def fig_title(fig,plot_input,model_input,var1_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

    # SPECIFY FILE PATH BASED ON TOD_INPUT, VCORDS_INPUT
    f_path = cf.file_path(model_input,tod_input,vcords_input)
    
    text_options = [['Zonal Average', ''],
                   ['Meridional Average', ''],
                   ['Column Integrated', ''], 
                   ['Annual Average', ''],
                   ['Diurnal Average', '']]

    unit_options = ['E','N','','Ls','LT']

    # select options based on user input
    rlist = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'rdims'].values[0]

    # Then remove levels as necessary
    rlist = [o for o in rlist if o not in ('lev2','lev3')]
       

    # go through rdmis assuming order lon,lat, lev, time, time_of_day_12
    text = []
 
    # first add variable names
    text += [var1_input]
    for i in rlist:    # i dimension name, dim_input = "all, int, or range"

       # check dimension and go to appropriate option in text_options (e.g. lon == index[0])   
       dim_index = 0 if i=='lon' \
          else (1 if i=='lat' else (3 if i=='time' else (2 if i=='lev' else 4)))

       # grab user input for each extra dimension
       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       # select text based on  both
       if "ALL" not in user_input:  # single value or range selected
          # check for unit
          if i == 'lev':
             unit = 'Pa' if vcords_input == 'pstd' else 'm'
             dim = vcords_input
             with xr.open_dataset(f_path,decode_times=False) as f:
                text += ['@ ' + text_options[dim_index][1]+f[dim].sel(**{dim:user_input},method='nearest').values + unit] 
          else:
             with xr.open_dataset(f_path,decode_times=False) as f:
                nearest_value=f[i].sel(**{i:user_input},method='nearest').values
                print(nearest_value)
             text += ['@ ' + text_options[dim_index][1]+str(nearest_value) + unit_options[dim_index]]
       elif user_input == 'ALL':
          text += [text_options[dim_index][0]]

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

   
    return text

