#================================================================================
# Callback to Open and Close Modal Plot Info
#================================================================================
from index import app
from dash.dependencies import Input, Output, State

@app.callback(
    Output("modal-txt", "children"),
    Input("btn-modal", "n_clicks"),
    [State("model-dropdown", "value"),
    State("plot-type-dropdown", "value"),
    State("variable1-dropdown", "value"),
    State("variable2-dropdown", "value"),
    State("variable3-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("solar-longitude-input","value"),
    State("tod-input","value"),
    State("lev-input","value")],
)

def plot_information(n1, model_input,plot_input,var1_input,var2_input,var3_input,vcords_input,lat_input,
   lon_input,time_input,tod_input,lev_input):

    # Generate the dynamic content based on the selected model input
    
    # Find name of Simulation
    txt_model = "Selected Model Configuration: {}".format(next((option['label'] for option in [
        {'label': 'Background Dust Climatology', 'value': 'sim1'},
    ] if option['value'] == model_input), 'Unknown'))

    # Find Name of Plot   
    txt_plot = "Selected Plot: {}".format(next((option['label'] for option in [
        {'label': '(2D) Lat/Lon Map', 'value': '2D_lon_lat'},
        {'label': '(2D) Lat/Altitude Cross Section', 'value': '2D_lat_lev'},
        {'label': '(2D) Lon/Altitude Cross Section', 'value': '2D_lon_lev'},
        {'label': '(2D) Latitude/Time Series', 'value': '2D_time_lat'},
        {'label': '(2D) Altitude/Time Series', 'value': '2D_time_lev'},
        {'label': '(2D) Longitude/Time Series', 'value': '2D_time_lon'},
        {'label': '(1D) Time Series', 'value': '1D_time'},
        {'label': '(1D) Latitude', 'value': '1D_lat'},
        {'label': '(1D) Longitude', 'value': '1D_lon'},
        {'label': '(1D) Altitude Profile', 'value': '1D_lev'},
        {'label': '(1D) Diurnal Cycle', 'value': '1D_diurn'},
    ] if option['value'] == plot_input), 'Unknown'))

    # Find Names of Variables
    txt_var1 = "Selected Variables: {}".format(var1_input)
    txt_var2 = "                {}".format(var2_input)
    txt_var3 = "                {}".format(var3_input)

    # Find Nearest Latitude Values
    txt_lat = "Selected Latitudes"
    txt = txt_model + "\n"+ txt_plot + "\n" + txt_var1 +  "\n" + txt_var2 +  "\n" + txt_var3

    #txt_var1 + "\n" + txt_var2 + "\n" + txt_var3 
 #txt = "Selected Model Label: {}".format(next((option['label'] for option in dropdown_options if option['value'] == model_input), 'Unknown'))
    
    
    # Return the generated content
    return txt

