#================================================================================
# Callback to Execute Request
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import common_functions as cf
from utils import data_function as df
from utils import variables as vb
import pandas as pd
import xarray as xr
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import json
from pathlib import Path

# Load Variable Data
dv = df.var_data() 

# Load Plotting Options
dp = df.plotting_options()

@app.callback(
    [Output("figure_out","figure"),
    Output("dim1-sav", "data"),
    Output("dim2-sav", "data"),
    Output("time-dim-sav","data"),
    Output("vert-dim-sav","data"),
    Output("var1-sav", "data"),
    Output("var2-sav", "data"),
    Output("var3-sav", "data")],
    Input("btn-doit-txt","n_clicks"),
    [State("model-dropdown", "value"),
    State("plot-type-dropdown", "value"),
    State("variable1-dropdown", "value"),
    State("variable2-dropdown", "value"),
    State("variable3-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),
    State("tod-input", "value"),
    State("cmap-dropdown", "value"),
    State("clev-input", "value"),
    State("fig-title","children")],
    prevent_initial_call=True,
)

def do_it(btn_clicks,model_input,plot_input,var1_input,var2_input,var3_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input,cmap_input,clev_input,plot_title_input):
    
    # initialize variables
    var1, var2, var3 = None, None, None

    # Load data conditionally (based on 1D or 2D plot_input)
    dim1, dim2, time_dim, vert_dim = cf.load_dims(model_input,plot_input,var1_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input)

    var1 = cf.load_data(model_input,plot_input,var1_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input)

    if str(var2_input) != "None":
       var2 = cf.load_data(model_input,plot_input,var2_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input)

    if str(var3_input) != "None":
       var3 = cf.load_data(model_input,plot_input,var3_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input)
    
    fig = plot_it(plot_input,cmap_input,clev_input,var1_input,vcords_input,var1,var2,var3,dim1,dim2,areo_input,lat_input,lon_input,lev_input,tod_input,plot_title_input)  
    return fig, dim1, dim2, time_dim, vert_dim, var1, var2, var3


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
        paper_bgcolor="#252930",
        plot_bgcolor="#252930")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def plot_it(plot_input,cmap_input,clev_input,var1_input,vcords_input,var1,var2,var3,dim1,dim2,areo_input,lat_input,lon_input,lev_input,tod_input,plot_title_input):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=[0, 1, 2, 3, 4, 5, 6, 7, 8, 10],
    y=[0, 4, 5, 1, 2, 3, 2, 4, 2, 1],
    mode="lines+markers+text",
    text=["","","","", "SIN DATOS", "","","", "", ''],
    textfont_size=40,
    ))
    fig.update_layout(
        paper_bgcolor="#252930",
        plot_bgcolor="#252930",      
    )
    fig.update_layout(
        xaxis = dict(
            showgrid=False,
            gridcolor="#252930",
            zerolinecolor="#252930"),
        yaxis = dict(
            showgrid=False,
            gridcolor="#252930",
            zerolinecolor="#252930"))  

    if "2D" in str(plot_input):

       # reformat for plotting
       dim1,dim2,var1 = json.loads(dim1),json.loads(dim2),json.loads(var1)
       dim1,dim2,var1 = xr.DataArray.from_dict(dim1),xr.DataArray.from_dict(dim2),xr.DataArray.from_dict(var1)


       cbar_title = dv.loc[(dv['plot-type'] == plot_input) & (dv['variable'] == var1.name), 'label'].values[0]
       # Check for User Specifications for Contour Levels and Cmap
       if cmap_input != "None":
          cmap = cmap_input
       else:
          cmap = dv.loc[(dv['plot-type'] == plot_input) & (dv['variable'] == var1.name), 'cmap'].values[0]

       if clev_input != "DEFAULT":
          dim_split = str(clev_input).split(",")
          zmin,zmax= min(float(dim_split[0]),float(dim_split[1])),max(float(dim_split[0]),float(dim_split[1]))
       else:
          zmin,zmax = None,None
       
       #hover text
       #hovertext = list()
       #for yi, yy in enumerate(dim2):
       #   hovertext.append(list())
       #for xi, xx in enumerate(dim1):
       #   hovertext[-1].append('dim1.name: {}<br />dim2.name: {}<br />var1.name: {}'.format(xx, yy, var1[yi][xi]))
     
       fig = go.Figure(data=go.Heatmap(z=var1.transpose(dim2.name,dim1.name),x=dim1, y=dim2, zsmooth='best',colorscale=cmap, zmin = zmin, zmax=zmax,name=var1.name,
             colorbar=dict(title=cbar_title,
                           titleside='right')))
       if var2:
          var2 = json.loads(var2)
          var2 = xr.DataArray.from_dict(var2)
          fig.add_trace(go.Contour(z=var2.transpose(dim2.name,dim1.name), x=dim1, y=dim2,name=var2.name,showscale=False,
                         contours=dict(coloring='none',showlabels=True,start=zmin,end=zmax),
                         line_width=2))       
       else:
          fig.add_trace(go.Contour(z=var1.transpose(dim2.name,dim1.name), x=dim1, y=dim2,showscale=False,
                         contours=dict(coloring='none',showlabels=True),
                         line_width=2))
       # Make negative contours dashed
       #min_z = np.min(z)
       #contour_levels = fig['data'][0]['contours']['start']
       #fig.update_traces(contours_coloring='lines', line_width=2,
       #           line_dash=[(10 if level < min_z else 1) for level in contour_levels])
       
       fig.update_layout(
          #title=plot_title_input,
          #title_x=0.5,
          autosize=False,
          margin={'l':1,'r':300,'t':1,'b':1},
          font_color="white",
          font_size=11,
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
        )

       xaxis_column_name = dv.loc[(dv['plot-type']==plot_input),'xaxis_name'].values[0]
       yaxis_column_name = dv.loc[(dv['plot-type']==plot_input),'yaxis_name'].values[0]

       
       xrange,xtick = dp.loc[(dp['dim']==dim1.name),'range'].values[0],dp.loc[(dp['dim']==dim1.name),'tick'].values[0]
       
       yrange,ytick = dp.loc[(dp['dim']==dim2.name),'range'].values[0],dp.loc[(dp['dim']==dim2.name),'tick'].values[0]
       fig.update_xaxes(title=xaxis_column_name,range=[xrange[0],xrange[1]],dtick=xtick)

       if dim2.name == 'pstd': 
          fig.update_yaxes(title=yaxis_column_name, tickvals=[1000,500,50,10,5,1,0.5,0.1,0.05,0.01],autorange='reversed',type='log')
       else:
          fig.update_yaxes(title=yaxis_column_name, range=[yrange[0],yrange[1]],dtick=ytick)
 
    # 1D_LEV PLOT 
    elif plot_input == "1D_lev":   # 1D vertical profile

       dim1,var1 = json.loads(dim1),json.loads(var1)
       dim1,var1 = xr.DataArray.from_dict(dim1),xr.DataArray.from_dict(var1)
       
       # plot figure
       fig = go.Figure(data=go.Scatter(x=np.array(var1),y=np.array(dim1), xaxis='x1', name=var1.name,line=dict(color="#808ef2")))
       
       if var2:
          var2 = json.loads(var2)
          var2 = xr.DataArray.from_dict(var2)
          fig.add_trace(go.Scatter(x=np.array(var2),y=np.array(dim1),xaxis='x2',name=var2.name))
          fig.update_layout(
             xaxis2=dict(
               title=dv.loc[(dv['variable']==var2.name),'unit'].values[0],
               side='top',
               overlaying='x1',
               zeroline=False,
               showgrid=False,
               tickcolor='#d85d44',tickwidth=2, ticklen=10,ticks='inside',
               range=[var2.min(),var2.max()],
               color='#d85d44'))
       if var3:
          var3 = json.loads(var3)
          var3 = xr.DataArray.from_dict(var3)
          fig.add_trace(go.Scatter(x=np.array(var3),y=np.array(dim1),xaxis='x3',name=var3.name))
          fig.update_layout(
             yaxis=dict(domain=[0,0.80]),
             xaxis2=dict(position=0.80),
             xaxis3=dict(position=1.0,
               title=dv.loc[(dv['variable']==var2.name),'unit'].values[0],
               side='top',
               overlaying='x1',
               zeroline=False,
               showgrid=False,
               tickcolor='#1ac483',tickwidth=2, ticklen=10,ticks='inside',
               range=[var3.min(),var3.max()],
               color='#1ac483'))
      
       fig.update_layout(
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
          font_color="white",
          font_size=11,
          margin={'l':1,'r':1,'t':1,'b':1},
          xaxis=dict(
               zeroline=False,
               showgrid=False,
               range=[var1.min(),var1.max()],
               title=dv.loc[(dv['variable']==var1.name),'unit'].values[0],
               color='#808ef2',
               tickcolor='#808ef2',tickwidth=2, ticklen=10,ticks='inside'),
          legend=dict(
            x=0.01,
            y=0.9,
            orientation='v',
            bgcolor='#252930',
            font=dict(
              size=11,
              color='white')),      
          yaxis=dict(
             title=dp.loc[(dp['dim']==vcords_input),'unit'].values[0],
             type='log',
             tickcolor='white',tickwidth=2, ticklen=10,ticks='inside',
             autorange='reversed'))

    else:  # 1D PLOT

       dim1,var1 = json.loads(dim1),json.loads(var1)
       dim1,var1 = xr.DataArray.from_dict(dim1),xr.DataArray.from_dict(var1)

       # plot figure
       fig = go.Figure(data=go.Scatter(x=np.array(dim1),y=np.array(var1),yaxis='y1',name=var1.name,line=dict(color="#808ef2")))

       if var2:
          var2 = json.loads(var2)
          var2 = xr.DataArray.from_dict(var2)
          fig.add_trace(go.Scatter(x=np.array(dim1),y=np.array(var2),yaxis='y2',name=var2.name))
          fig.update_layout(
             yaxis2=dict(
               title=dv.loc[(dv['variable']==var2.name),'unit'].values[0],
               side='right',
               overlaying='y1',
               zeroline=False,
               showgrid=False,
               tickcolor='#d85d44',tickwidth=2, ticklen=10,ticks='inside',
               range=[var2.min(),var2.max()],
               color='#d85d44'))
       if var3:
          var3 = json.loads(var3)
          var3 = xr.DataArray.from_dict(var3)
          fig.add_trace(go.Scatter(x=np.array(dim1),y=np.array(var3),yaxis='y3',name=var3.name))
          fig.update_layout(
             xaxis=dict(domain=[0.0,0.86]),
             yaxis2=dict(position=0.86),
             yaxis3=dict(position=1.0,
                title=dv.loc[(dv['variable']==var3.name),'unit'].values[0],
                side='right',
                overlaying='y1',
                zeroline=False,
                showgrid=False,
                tickcolor='#1ac483',tickwidth=2, ticklen=10,ticks='inside',
                range=[var3.min(),var3.max()],
                color='#1ac483'))

       # load x-axis information
       xaxis_title = dv.loc[(dv['plot-type']==plot_input),'xaxis_name'].values[0]
       xrange,xtick = dp.loc[(dp['dim']==dim1.name),'range'].values[0],dp.loc[(dp['dim']==dim1.name),'tick'].values[0]
      
       # load y-axis information
       fig.update_layout(
          yaxis=dict(
              title=dv.loc[(dv['variable']==var1.name),'unit'].values[0],
              zeroline=False,
              showgrid=False,
              tickcolor='#808ef2',tickwidth=2, ticklen=10,ticks='inside',
              range=[var1.min(),var1.max()],
              color='#808ef2'),
          font_color="white",
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
          margin={'l':1,'r':1,'t':1,'b':1},
          xaxis=dict(
             title= xaxis_title,
             range = [xrange[0],xrange[1]],
             dtick = xtick),
          legend=dict(
            x=0.01,
            y=1.03,
            orientation='v',
            bgcolor='#252930',
            font=dict(
              size=11,
              color='white')))
      
    return fig
 

def create_vertical_profile(plot_input,vertical_profile_var,vert_dim,hv_min,hv_max):

    if "2D" in str(plot_input):
      
       # plot figure
       fig = go.Figure(data=go.Scatter(y=np.array(vert_dim),x=vertical_profile_var))
       fig.update_layout(
          autosize=False,
          margin={'l':1,'r':1,'t':1,'b':1},
          font_color="white",
          font_size=11,
          paper_bgcolor="#252930",
          plot_bgcolor="#252930",
        )


       yaxis_column_name=dp.loc[(dp['dim']==vert_dim.name),'unit'].values[0]
       xaxis_column_name=dv.loc[(dv['variable']==vertical_profile_var.name),'unit'].values[0]
       fig.update_xaxes(title=xaxis_column_name,range=[hv_min,hv_max])
       fig.update_yaxes(title=yaxis_column_name,type='log', autorange='reversed')

       return fig

