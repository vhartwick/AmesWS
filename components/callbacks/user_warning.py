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
    Output('lev-alert', 'children'),
    Output('lev-alert', 'is_open'),
    Output('clev-alert', 'children'),
    Output('clev-alert', 'is_open'),
    Output('btn-doit-txt', 'disabled')],
    [Input("lat-input", "value"),
    Input("lon-input", "value"),
    Input("solar-longitude-input", "value"),
    Input("tod-input", "value"),
    Input("vertical-coordinates-radio", "value"),
    Input("lev-input", "value"),
    Input("clev-input", "value")],
    State("plot-type-dropdown", "value"),
)

def user_warning(lat_input,lon_input,ls_input,tod_input,vcords_input,lev_input,clev_input,plot_input):

   alert_message = ["None","None","None","None","None","None"]
   alert_is_open = [False, False, False, False, False,False]
   var_list = ['lat','lon','time','time_of_day','lev']
   var_longname = ['latitude', 'longitude', 'aerocentric longitude (Ls)', 'local time', 'pressure']
   input_list = [lat_input, lon_input, ls_input, tod_input,lev_input]
   button_status = False   # the plot button is enabled by default

   if "zstd" in str(vcords_input) or "zagl" in str(vcords_input):
      var_longname = "Altitude"
   
   for i in range(len(var_list)):
      # First check formattting
      alert_message[i],alert_is_open[i], button_status = format_check(plot_input,var_list[i],var_longname[i],input_list[i])
   if any(alert_is_open): # checks if any formatting alerts are triggered
      return alert_message[0], alert_is_open[0], alert_message[1], alert_is_open[1], alert_message[2], alert_is_open[2], alert_message[3], alert_is_open[3], alert_message[4], alert_is_open[4], alert_message[5], alert_is_open[5], button_status

   for i in range(len(var_list)):
      # Next Check Values
      alert_message[i], alert_is_open[i], button_status = range_check(i,var_list[i],input_list[i],vcords_input)
  
   ## Now check contour ranges (acceptable characters are - , . and DEFAULT)
   input_pattern = r'^(-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?|DEFAULT)$'
   format_error_message = "User Input is not in the expected format. Separate values for the contour range by a single comma with no spaces or, to use the default contour range, type DEFAULT"   
   if not re.match(input_pattern, clev_input):
      alert_message[5] = format_error_message
      alert_is_open[5] = True
      button_status = True
 
   if any(alert_is_open):  # checks if any alerts are open
      button_status= True
   
   return alert_message[0], alert_is_open[0], alert_message[1], alert_is_open[1], alert_message[2], alert_is_open[2], alert_message[3], alert_is_open[3], alert_message[4], alert_is_open[4], alert_message[5], alert_is_open[5], button_status

def format_check(plot_input,var_name,var_longname,var_input):
   aio, am, btns = False, "", True     

   # FIND DIMENSION NAME
   dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
   dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

   # Define the regular expression to match the user input
   if var_name in dimx or var_name in dimy:   # if user variable is one of the plot dimensions
      if var_name == "lat" or var_name == "lon": # allow negative numbers
         input_pattern = r'^(-?\d+,-?\d+|ALL)$'
         format_error_message = f"User Input is not in the expected format. You can specify a range of values separated by a single comma with no spaces or, to include the entire range, type ALL"
      else:
         input_pattern = r'^(\d+,\d+|ALL)$'
         format_error_message = f"User Input is not in the expected format. You can specify a range of values separated by a single comma with no spaces or, to include the entire range, type ALL. Values must be positive"
   else:
      if var_name == "lat" or var_name == "lon": # allow negative numbers
         input_pattern = r'^(-?\d+,-?\d+|-?\d+|ALL)$'
         format_error_message = f"User Input is not in the expected format. You can specify a single numeric value (#), a range of values separated by a single comma with no spaces, or to include the entire {var_longname} range, type ALL"
      elif var_name != "lev":  # allow range
         input_pattern = r'^(\d+,\d+|\d+|ALL)$'
         format_error_message = f"User Input is not in the expected format. You can specify a single positive numeric value (#), a range of values separated by a single comma with no spaces, or to include the entire {var_longname} range, type ALL"
      else:
         input_pattern = r'^(\d+)$'
         format_error_message = f"User Input is not in the expected format. You can specify a single positive numeric value (#)"
    
   # check format & return if not matching expected format
   if not re.match(input_pattern, var_input):
      aio = True
      am = format_error_message
      btns = aio
   return am, aio, btns
   
def range_check(i, var_name, var_input, vcords_input):

   range_max = [90,360,360,24,700]
   range_min = [-90,0,0,0, 0.01]
   rem_list = ["Latitude should be between -90 and 90", "Longitude should be between 0 and 360",
              "Aerocentric longitude (Ls) should be between 0 and 360","Local Times should be between 0 and 24",
              "Pressure should be between 700 and 0.01 Pa"]
   aio, am = False, ""    
   
   # replace elements of range_max, range_min and rem_list based on vcords_input (pstd is default)
   if "zstd" in str(vcords_input):
      range_max[i] = 110000.
      range_min[i] = 0
      rem_list[i] = "Altitude above the Reference Aeroid should be between 0 and 110 km"
   elif "zagl" in str(vcords_input):
      range_max[i] = 110000.
      range_min[i] = 0
      rem_list[i] = "Altitude above the surface should be between 0 and 110 km"
   
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

