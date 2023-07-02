#================================================================================
# Callback to Generate Second Variable Dropdown List based on Plot Type
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df
from utils import common_functions as cf

# Load Variable Data
dv = df.var_data()

@app.callback(
    Output("variable2-dropdown", "options"),
    Input("variable1-dropdown", "value"),
    State("plot-type-dropdown", "value"),
    prevent_initial_call = True,
)

def update_variable2_options(var1_input, plot_input):
    options = sorted(set(dv.loc[dv['plot-type'] == plot_input, 'label']))
    return [o for o in options if o != var1_input]


