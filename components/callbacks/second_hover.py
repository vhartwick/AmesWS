#================================================================================
# Callback to Generate First Variable Dropdown List based on Plot Type
#================================================================================
from index import app
import dash
from dash.dependencies import Input, Output, State
from utils import data_function as df
import json
import xarray as xr
from utils import common_functions as cf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Load Database
dv = df.var_data()

# Load Plotting Options
dp = df.plotting_options()

@app.callback(
    [Output("vertical_profile", "figure"),
    Output("vertical_profile", "style")],
    Input("figure_out", "hoverData"),
    [State("plot-type-dropdown", "value"),
    State("variable1-dropdown","value"),
    State("variable2-dropdown","value"),
    State("model-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),
    State("tod-input", "value"),
    State("vert-dim-sav","data")],
    #State("time-var-sav","data")],
    prevent_initial_call = True)


def update_vertical_profile(hoverData,plot_input,var1_input,var2_input,model_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,vert_dim_input):

    fig_visibility = {"display":"none"}

    if "2D" in str(plot_input):
       vert_dim = json.loads(vert_dim_input)
       vert_dim = xr.DataArray.from_dict(vert_dim)

       # change units of vert_dim to km if necesary
       if vcords_input != 'pstd':
          vert_dim = vert_dim/1000

       # Use hover data to select variable at x,y of hover
       dimx_hover = hoverData['points'][0]['x']
       dimy_hover = hoverData['points'][0]['y']

       hvv_min,hvv_max,vertical_profile_var = cf.select_vertical_profile_var(dv,plot_input,var1_input,model_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover)
    
       # LOAD SECOND VARRIABLE IF SELECTED
       if str(var2_input) != "None":
          hv2_min,hv2_max,vertical_profile_var2 = cf.select_vertical_profile_var(dv,plot_input,var2_input,model_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,dimx_hover,dimy_hover)

       # NOW CREATE THE FIGURE
       yaxis_column_name=dp.loc[(dp['dim']==vert_dim.name),'unit'].values[0]
       xaxis_column_name=dv.loc[(dv['variable']==vertical_profile_var.name),'unit'].values[0]  
       
       # plot it
       fig = go.Figure(data=go.Scatter(y=np.array(vert_dim),x=vertical_profile_var, name=vertical_profile_var.name,xaxis='x1',line=dict(color="#808ef2")))
     
       if str(var2_input) != "None":
          xaxis_column_name2=dv.loc[(dv['variable']==vertical_profile_var2.name),'unit'].values[0]
          fig.add_trace(go.Scatter(y=np.array(vert_dim), x=vertical_profile_var2, name=vertical_profile_var2.name, xaxis='x2'))
          fig.update_layout(
             xaxis2=dict(
               title=xaxis_column_name2,
               range=[hv2_min, hv2_max],
               overlaying='x',
               tickcolor='white',tickwidth=2, ticklen=10,ticks='inside',
               showgrid=False,
               color='#d85d44',
               side='top'))

       # Update Vertical Profile Title
       if plot_input == '2D_lat_lev':
          title = 'Vertical Profile <br>('+str("%.1f" % dimx_hover)+'N)'
       elif plot_input == '2D_lon_lev':
          title = 'Vertical Profile <br>('+str("%.1f" % dimx_hover)+'E)'
       elif plot_input == '2D_time_lat':
          title = 'Vertical Profile <br>('+str("%.1f" % dimy_hover)+'N, '+str("%.1f" % dimx_hover)+'°Ls)'
       elif plot_input == '2D_time_lon':
          title = 'Vertical Profile <br>('+str("%.1f" % dimy_hover)+'E, '+str("%.1f" % dimx_hover)+'°Ls)'       
       elif plot_input == '2D_time_lev':
          title = 'Vertical Profile <br>('+str("%.1f" % dimx_hover)+'°Ls)'
       else:
          title = 'Vertical Profile <br>('+str("%.1f" % dimy_hover)+'N, '+str("%.1f" % dimx_hover)+'E)'
      
       fig.update_layout(
          title=title,
          title_x=0.5,
          showlegend=False,
          autosize=False,
          margin={'l':1,'r':1,'t':100,'b':1},
          font_color="white",
          font_size=10,
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
          xaxis=dict(
            title=xaxis_column_name,
            tickcolor='white',tickwidth=2, ticklen=10,ticks='inside',
            showgrid=False,
            side='bottom',
            color='#808ef2'),
          yaxis=dict(
            title=yaxis_column_name,
            type='log',
            range=[1000,0.01],
            autorange='reversed'),
          legend=dict(
            x=0.5,
            y=1.2,
            orientation='h',
            bgcolor='#252930',
            font=dict(
              size=6,
              color='white')))

       # change to linear axis if vertical coordinate is not Pa
       if vcords_input != 'pstd':
          fig.update_layout(
             yaxis = dict(
                type='linear',
                range=[0,110],
                autorange=True))
       
       fig_visibility = {"display":"block"} 
       return fig, fig_visibility

    else:
       return dash.no_update
