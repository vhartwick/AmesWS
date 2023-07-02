#================================================================================
# Callback to Generate Third Variable Dropdown List based on Plot Type
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df
from dash.exceptions import PreventUpdate
from utils import common_functions as cf

# Load Variable Data
dv = df.var_data()

@app.callback(
    [Output("variable3-dropdown", "options"),
    Output("variable3-dropdown","style"),
    Output("variable3-text","style")],
    Input("variable2-dropdown", "value"),
    [State("variable1-dropdown", "value"),
    State("plot-type-dropdown", "value")],
    prevent_initial_call = True,
)

def update_variable_options(var1_input,var2_input,plot_input):
    options = sorted(set(dv.loc[dv['plot-type'] == plot_input, 'label']))
    display = "none" if "1D" not in str(plot_input) else "block"  
    return [ o for o in options if  o != var1_input and o!=var2_input],{"display":display,"backgroundColor":"#252930"}, {"display":display}

