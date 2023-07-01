#================================================================================
# Callback to Pop Up Alert if User Input is out of range, in wrong format, ettc
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import common_functions as cf
from utils import data_function as df
import re

# Load Database
dv = df.var_data()
dp = df.plotting_options()


# Option to Link to Submit Button and Check all 
@app.callback(
    [Output('lat-alert', 'children'),
    Output('lat-alert', 'is_open'),
    Output('lon-alert', 'children'),
    Output('lon-alert', 'is_open'),
    Output('ls-alert', 'children'),
    Output('ls-alert', 'is_open'),
    Output('tod-alert', 'children'),
    Output('tod-alert', 'is_open'),  
    Output('clev-alert', 'children'),
    Output('clev-alert', 'is_open'),
    Output('btn-doit-txt', 'disabled')],
    [Input("lat-input", "value"),
    Input("lon-input", "value"),
    Input("solar-longitude-input", "value"),
    Input("tod-input", "value"),
    Input("clev-input", "value")],
    State("plot-type-dropdown", "value"),
)

def user_warning(lat_input,lon_input,ls_input, tod_input,clev_input,plot_input):

   alert_message = ["None","None","None","None","None"]
   alert_is_open = [False, False, False, False, False]
   var_list = ['lat','lon','time','time_of_day']
   input_list = [lat_input, lon_input, ls_input, tod_input]
   button_status = False   # the plot button is enabled by default

   for i in range(len(var_list)):
      
      # First check formattting
      alert_message[i],alert_is_open[i], button_status = format_check(plot_input,var_list[i],input_list[i])
  
   if any(alert_is_open): # checks if any formatting alerts are triggered
      return alert_message[0], alert_is_open[0], alert_message[1], alert_is_open[1], alert_message[2], alert_is_open[2], alert_message[3], alert_is_open[3], alert_message[4], alert_is_open[4], button_status

   for i in range(len(var_list)):
      # Next Check Values
      alert_message[i], alert_is_open[i], button_status = range_check(i,var_list[i],input_list[i])
      
   return alert_message[0], alert_is_open[0], alert_message[1], alert_is_open[1], alert_message[2], alert_is_open[2], alert_message[3], alert_is_open[3], alert_message[4], alert_is_open[4], button_status

def format_check(plot_input,var_name,var_input):
   aio, am, btns = False, "", True     

   # FIND DIMENSION NAME
   dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
   dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

   # Define the regular expression to match the user input
   if var_name in dimx or var_name in dimy:   # if user variable is one of the plot dimensions
      input_pattern = r'^(-?\d+,-?\d+|ALL)$'
      format_error_message = "User Input is not in the expected format. Separate values for the latitude range by a single comma with no spaces or, to include the entire latitude range, type ALL"
   else:
      input_pattern = r'^(-?\d+,-?\d+|-?\d+|ALL)$'
      format_error_message = "User Input is not in the expected format. You can specify a single numeric value (#), a range of values separated by a single comma with no spaces, or to include the entire latitude range, type ALL"
    
   # check format & return if not matching expected format
   if not re.match(input_pattern, var_input):
      aio = True
      am = format_error_message
      btns = aio
   return am, aio, btns
   
def range_check(i, var_name, var_input):

   ### BIG WARNING CHANGE RANGE MAX FOR TOD BASED ON SIZE OF DIURN FILE! ###
   range_max = [90,360,360,24]
   range_min = [-90,0,0,0]
   rem_list = ["Latitude should be between -90 and 90", "Longitude should be between 0 and 360",
              "Aerocentric longitude (Ls) should be between 0 and 360","Local Times should be between 0 and 24"]
   aio, am = False, ""    
   
   # Check that values are within expected range
   range_error_message = rem_list[i]          
         
   if "," not in var_input and "ALL" not in var_input:  # single value selected
      try:  
         if int(var_input) < range_min[i] or int(var_input) > range_max[i]:
            raise ValueError(range_error_message)
      except ValueError as e:
         am = str(e)
         aio = True

   elif var_input == 'ALL':   # average over ALL
      aio = False

   else: # range
      dim_split = str(var_input).split(",")
      try:
         if int(dim_split[0]) < range_min[i] or int(dim_split[0]) > range_max[i] or int(dim_split[1]) < range_min[i] or int(dim_split[1]) > range_max[i]:
            raise ValueError(range_error_message)
      except ValueError as e:
         am = str(e)
         aio = True

   btns= aio

   # return any that are open 
   return am, aio, btns

