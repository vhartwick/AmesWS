
#================================================================================
# Callback to Generate First Variable Dropdown List based on Plot Type
#================================================================================
from index import app
from components.sidebar import Sidebar 
from dash.dependencies import Input, Output
from utils import data_function as df
from utils import common_functions as cf

# Load Variable Data
dv = df.var_data()


@app.callback(
    Output("variable1-dropdown", "options"),
    Input("plot-type-dropdown", "value")
)

def update_variable1_options(input_value):
    return sorted({o for o in dv.loc[dv['plot-type']==input_value, 'label']})   # optimized using set comprehension


