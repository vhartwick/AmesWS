#================================================================================
# Callback to Generate List of Additional Variables for User to Dowload
#================================================================================
from index import app
from dash.dependencies import Input, Output, State
from utils import data_function as df
import json 
import xarray as xr
import numpy as np

# Load Variable Data
dv = df.var_data()

@app.callback(
    [Output("output-data-checklist", "options"),
     Output("output-column-data-checklist", "options"),
     Output("output-data-popover", "style"),
     Output("output-data-popover", "is_open"),
    Output("column-accordion","style")],
    [Input("output-format-checklist", "value"),
     Input("output-data-popover", "is_open")],
    [State("plot-type-dropdown","value"),
     State("var1-sav", "data"),
     State("var2-sav", "data"),
     State("var3-sav", "data")],
    prevent_initial_call=True,
)
def update_download_variables(output_format, is_open, plot_input,var1_input, var2_input, var3_input):

    result = []

    if "lev" in plot_input:
       col_style = {"display":"none"}
    else:
       col_style = {"display":"block"}

    if "ncdf" in output_format or "csv" in output_format:
        var1 = json.loads(var1_input)['name']
        
        # initialize var2, var3
        var2,var3 = None,None
        # check for second and third variables
        if var2_input:
           var2 = json.loads(var2_input)['name']
        if var3_input:
           var3 = json.loads(var3_input)['name']

        filtered_dv = dv[(dv['variable'] != var1) & (dv['variable'] != var2) & (dv['variable'] != var3)]
        result_label = filtered_dv['label'].unique()
        result_values = filtered_dv['variable'].unique()
        result = [{'label': label, 'value': value} for label, value in zip(result_label, result_values)]
 
        # return only 4D variables for column options
        mask = filtered_dv['label'].str.contains('Surface', case=False) 
        filtered_dv = filtered_dv[~mask]    
        col_result_label = filtered_dv['label'].unique().tolist()
        col_result_values = filtered_dv['variable'].unique().tolist()
        col_result = [{'label': label, 'value': value} for label, value in zip(col_result_label, col_result_values)]
        style = {"border": "1px solid white", "backgroundColor": "#252930", "color": "white", "display": "block"}
        is_open = True  # Open the popover if it was closed before and ncdf/csv are selected
    
    elif is_open:
        style = {"display": "none"}  # Close the popover if it was open before and no ncdf/csv are selected
    
    else:
        style = {"display": "none"}
    
    return result, col_result, style, is_open, col_style



