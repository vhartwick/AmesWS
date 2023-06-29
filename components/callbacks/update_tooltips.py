#================================================================================
# Callback to Change Tooltip Text Based on Plot Type Choice
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import common_functions as cf
from utils import data_function as df

# Load Database
dv = df.var_data()

@app.callback(
    [Output("lat-tooltip", component_property="children"),
    Output("lon-tooltip", component_property="children"),
    Output("time-tooltip", component_property="children"),
    Output("tod-tooltip", component_property="children"),
    Output("lev-tooltip", component_property="children"),
    Output("lev2-tooltip", component_property="children"),
    Output("lev3-tooltip", component_property="children")],
    Input("plot-type-dropdown", "value"),
)
def update_tooltips(plot_input):

    # FIND DIMENSION NAME
    dimx = dv.loc[(dv['plot-type']==plot_input),'dimx'].values[0]
    dimy = dv.loc[(dv['plot-type']==plot_input),'dimy'].values[0]
    
    # Define a dictionary with dyanmic values 
    output_dict = {}
    options = ['lat','lon','time','time_of_day_12','lev']
    
    for i in options:
        if i in dimx:
           output_dict[i] = f'This is your X-axis. Choose a range of values "X,Y" or to see the entire range "ALL"'

        elif i in dimy:
           output_dict[i] = f'This is your Y-axis. Choose a range of values "X,Y" or to see the entire range "ALL"'
        else:
           output_dict[i] = 'Choose a single value "X", a range of values "X,Y" or to see average over the entire range "ALL"'
       
        # Now take care of lev2 and lev3 for optional variables 1 and 2
        if dimx == 'lev' or dimy == 'lev':
           output_dict['lev2'] = 'Choose a range of values "X,Y" or to see the entire range "ALL"'
           output_dict['lev3'] = 'Choose a range of values "X,Y" or to see the entire range "ALL"'
        else:
           output_dict['lev2'] = 'Choose a single value "X", a range of values "X,Y" or to see average over the entire range "ALL"'
           output_dict['lev3'] = 'Choose a single value "X", a range of values "X,Y" or to see average over the entire range "ALL"'

    # Return the dictionary values as strings
    return [str(output_dict.get(key, "")) for key in options + ['lev2', 'lev3']]
    


