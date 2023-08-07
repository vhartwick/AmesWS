#================================================================================
# Callback to Change Visibility of Level Input Based on Variable Choice
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df

# Load Database
dv = df.var_data()


@app.callback(
    [Output("lat-input", "value"),
    Output("lon-input", "value")],
    Input("plot-type-dropdown", "value"),
)

def change_latlon_default(plot_input):

    default_lat_value, default_lon_value = 'ALL', 'ALL'
   
    if plot_input == "1D_daily":
       default_lat_value = '22'
       default_lon_value = '48'

    return default_lat_value, default_lon_value
