#================================================================================
# Callback to Change Visibility of Plotting Options Accordion Based on Plot Type
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df

# Load Database
dv = df.var_data()


@app.callback(
    Output("plotting-accordian", component_property="style"),
    Input("plot-type-dropdown", "value"),
)

def change_po_vis(plot_input):
   
    # Set styles based on input values
    if "2D" in plot_input:
       style={"display":"block"} 
    else:
       style={"display":"none"} 
    return style 


