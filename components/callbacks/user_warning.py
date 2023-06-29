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

# Option to Link to Submit Button and Check all 
@app.callback(
    [Output('lat-alert', 'children'),
    Output('lat-alert', 'is_open')],
    Input("lat-input", "value"),
    State("plot-type-dropdown", "value"),
)
def user_warning(lat_input, plot_input):

   # FIND DIMENSION NAME
   dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
   dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]

   # check if latittude is a dimension
   if 'lat' in dimx or 'lat' in dimy:


      # define he regular expression to match the user input
      input_pattern = r'^(\d+,\d+|ALL)$'
                    
      # check format
      if re.match(input_pattern, lat_input):
         alert_message = ""
         alert_is_open = False
      else:
         alert_message = "User input is not in the expected format. Separate values for the latitude range by a single comma with no spaces or, to include the entire latitude range, type ALL"
         alert_is_open = True

   else:
      # define the regular expression to match the user input
      input_pattern = r'^(\d+,\d+|\d+|ALL)$'

      # check format
      if re.match(input_pattern, lat_input):
         alert_message = ""
         alert_is_open = False       
      else:
         alert_message = "User Input is not in the Expected Format. You can specify a single value (#), a range of values separated by a comma, or to include the entire range, type ALL"


   # Check if value is within expected range or in the correct format (-90,90)
   if "," and "ALL" not in lat_input:  # single value selected
      try:  
         if int(lat_input) < -90 or int(lat_input) > 90:
            raise ValueError("Latitude should be between -90 and 90")
         alert2_message = ""
         alert2_is_open = False
      except ValueError as e:
         alert2_message = str(e)
         alert2_is_open = True

   elif lat_input == 'ALL':   # average over ALL
      alert2_message = ""
      alert2_is_open = False

   else: # range
      dim_split = str(lat_input).split(",")
      try:
         if dim_split[0] < -90 or dim_split[0] > 90 or dim_split[1] < -90 or dim_split[1] > 90:
            raise ValueError("Latitude should be between -90 and 90")
         alert2_message = ""
         alert2_is_open = False
      except ValueError as e:
         alert2_message = str(e)
         alert2_is_open = True

   # Combine alerts & return any that are open
   alert_message = alert_message+alert2_message
   alert_is_open = alert_is_open or alert2_is_open
   return alert_message, alert_is_open

