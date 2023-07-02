#================================================================================
# Callback to Generate First Variable Dropdown List based on Plot Type
#================================================================================
import dash
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df
from utils import common_functions as cf
import json
import xarray as xr
from utils import common_functions as cf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Load Database
dv = df.var_data()

@app.callback(
    Output("time_series", "figure"),
    Input("figure_out", "hoverData"),
    [State("plot-type-dropdown", "value"),
    State("variable1-dropdown","value"),
    State("variable2-dropdown","value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),  
    State("tod-input", "value"),
    State("time-dim-sav","data")],
    prevent_initial_call = True)


def update_timeseries(hoverData,plot_input,var1_input,var2_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,time_dim_input):

    if "2D" in str(plot_input): 
       time_dim = json.loads(time_dim_input)
       time_dim = xr.DataArray.from_dict(time_dim)

       # Use hover data to select variable at x,y of hover
       dimx_hover = hoverData['points'][0]['x']
       dimy_hover = hoverData['points'][0]['y']

       hv_min,hv_max,time_series_var = cf.select_timeseries_hover_var(dv,plot_input,var1_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover)

       # LOAD SECOND VARRIABLE IF SELECTED
       if str(var2_input) != "None":
          hv2_min,hv2_max,time_series_var2 = cf.select_timeseries_hover_var(dv,plot_input,var2_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover)

       # NOW MAKE THE FIGURE
       yaxis_column_name=dv.loc[(dv['variable']==time_series_var.name),'unit'].values[0]
       xaxis_column_name="Ls"
       
       # plot figure
       fig = go.Figure(data=go.Scatter(x=np.array(time_dim),y=time_series_var,name=time_series_var.name,yaxis='y1'))
       if str(var2_input) != "None":
          yaxis_column_name2=dv.loc[(dv['variable']==time_series_var2.name),'unit'].values[0]
          fig.add_trace(go.Scatter(x=np.array(time_dim), y=time_series_var2, name=time_series_var2.name, yaxis='y2'))
          fig.update_layout(
             yaxis2=dict(
               title=yaxis_column_name2,
               range=[hv2_min, hv2_max],
               side='right',
               overlaying='y', 
               tickcolor='white',tickwidth=2, ticklen=10,ticks='inside',
               showgrid=False,
               color='#de5f46'))

       fig.update_layout(
          autosize=False,
          margin={'l':1,'r':1,'t':1,'b':1},
          font_color="white",
          font_size=10,
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
          yaxis=dict(
            title=yaxis_column_name,
            range=[hv_min, hv_max],
            tickcolor='white',tickwidth=2, ticklen=10,ticks='inside',
            showgrid=False,
            side='left',
            color='#6273f1'),
          xaxis=dict(
            title=xaxis_column_name,
            range=[0, 360],
            dtick=60),
          legend=dict(
             x=0.01,
             y=1.03,
             orientation='v',
             bgcolor='#252930',
             font=dict(
               size=10,
               color='white')))

       return fig
    else:
       return dash.no_update


