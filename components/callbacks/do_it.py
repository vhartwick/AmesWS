#================================================================================
# Callback to Execute Request
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash import html
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
import re
from pathlib import Path

# Load Variable Data
dv = df.var_data() 

# Load Plotting Options
dp = df.plotting_options()

# Load File Options Dictionary
file_options = df.file_options()

@app.callback(
    [Output("figure_out","figure"),
    Output("dim1-sav", "data"),
    Output("dim2-sav", "data"),
    Output("time-dim-sav","data"),
    Output("vert-dim-sav","data"),
    Output("var1-sav", "data"),
    Output("var2-sav", "data"),
    Output("var3-sav", "data"),
    Output("fig-title","children"),
    Output("modal-txt","children"),
    Output("btn-download","disabled")],
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
    State("clev-input", "value")],
    prevent_initial_call=True,
)

def do_it(btn_clicks,model_input,plot_input,var1_input,var2_input,var3_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input,cmap_input,clev_input):
    
    # initialize variables
    var1, var2, var3 = None, None, None

    # Load data conditionally (based on 1D or 2D plot_input)
    dim1, dim2, time_dim, vert_dim = cf.load_dims(model_input,plot_input,var1_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input)

    var1 = cf.load_data(model_input,plot_input,var1_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input)

    if str(var2_input) != "None":
       var2 = cf.load_data(model_input,plot_input,var2_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input)

    if str(var3_input) != "None":
       var3 = cf.load_data(model_input,plot_input,var3_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input)
    
    # output figure information and title
    modal_text,plot_title = user_input_text(plot_input,model_input,var1_input,var2_input,var3_input,vcords_input,time_input,lat_input,lon_input,lev_input,tod_input)
    
    fig = plot_it(plot_input,cmap_input,clev_input,var1_input,vcords_input,var1,var2,var3,dim1,dim2,time_input,lat_input,lon_input,lev_input,tod_input)  
    return fig, dim1, dim2, time_dim, vert_dim, var1, var2, var3, plot_title, modal_text, False


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None,
        paper_bgcolor="#252930",
        plot_bgcolor="#252930")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig

def plot_it(plot_input,cmap_input,clev_input,var1_input,vcords_input,var1,var2,var3,dim1,dim2,time_input,lat_input,lon_input,lev_input,tod_input):

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

       # if vertical coordinate is not pressure and dimy=lev, change from m to km
       if "lev" in plot_input and vcords_input != 'pstd':
          dim2 = dim2/1000
     
       # specifications for colorbars & contour range 
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
 
       # check that the user didn't specify dimx or dimy range (lat, lon, lev, areo, tod)
       # quickly rename pstd,zstd,zagl to lev
       tmp_dim1name = 'lev' if dim1.name in ['pstd', 'zstd', 'zagl'] else dim1.name
       tmp_dim2name = 'lev' if dim2.name in ['pstd', 'zstd', 'zagl'] else dim2.name

       if locals()[f'{dim1.name}_input'] != 'ALL':
           xsplit =locals()[f'{tmp_dim1name}_input'].split(",") 
           while np.abs(int(xsplit[0]) - int(xsplit[1])) / xtick < 3:  # make sure there are att least three ticks
              xtick = xtick / 2
           fig.update_xaxes(range=[xsplit[0],xsplit[1]],dtick=xtick)
       if locals()[f'{tmp_dim2name}_input'] != 'ALL':
           ysplit =locals()[f'{dim2.name}_input'].split(",")
           while np.abs(int(ysplit[0]) - int(ysplit[1])) / ytick < 3:  # make sure there are att least three ticks
              ytick = ytick / 2
           fig.update_yaxes(range=[ysplit[0],ysplit[1]],dtick=ytick)



    # 1D_LEV PLOT (separated out since dimension is on y axis) 
    elif plot_input == "1D_lev":   # 1D vertical profile

       dim1,var1 = json.loads(dim1),json.loads(var1)
       dim1,var1 = xr.DataArray.from_dict(dim1),xr.DataArray.from_dict(var1)
     
       # for zagl, zstd change vertical coordinate to km from m 
       if vcords_input != 'pstd':
          dim1 = dim1/1000

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

       if vcords_input != 'pstd':
          fig.update_layout(
             yaxis=dict(
                title=dp.loc[(dp['dim']==vcords_input),'unit'].values[0],
                type='linear',
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
     
       # check that the user didn't specify dimx or dimy range (lat, lon, lev, areo, tod)
       if locals()[f'{dim1.name}_input'] != 'ALL':
           xsplit =locals()[f'{dim1.name}_input'].split(",")
           while np.abs(int(xsplit[0]) - int(xsplit[1])) / xtick < 3:  # make sure there are att least three ticks
              xtick = xtick / 2
           fig.update_xaxes(range=[xsplit[0],xsplit[1]],dtick=xtick)
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

# GENERATE TEXT TO DESCRIBE FIGURE, DISPLAY TITLE & COPY FOR README
def user_input_text(plot_input,model_input,var1_input,var2_input,var3_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input):

    # SPECIFY FILE PATH BASED ON TOD_INPUT, VCORDS_INPUT
    f_path = cf.file_path(model_input,plot_input,tod_input,vcords_input)
    
    # DESCRIPTION OF FILE 
    # Select file description text from dictionary
    simulation = file_options[model_input]
    if "atmos_ave" in f_path:
       time_averaging = file_options["atmos_ave"]
    elif "atmos_diurn" in f_path:
       time_averaging = file_options["atmos_diurn"]
    else:
       time_averaging = file_options["atmos_daily"]
    vertical_interpolation = file_options[vcords_input]

    # DESCRIPTION OF PLOT
    
    # intro text describing nearest value selection (varies with resolution)
    nearest_value1_samp,nearest_value2_samp = cf.find_nearest_value(f_path,'lat',"-30,30")

    # variable list
    var_value = var1_input 
    if var2_input is not None:
       var_value += ', ' + var2_input
    if var3_input is not None:
       var_value += ', ' + var3_input

    # PLOT TITLE
    text_options = [['Zonal Average', ''],
                   ['Meridional Average', ''],
                   ['Column Integrated', ''], 
                   ['Annual Average', ''],
                   ['Diurnal Average', '']]

    unit_options = ['E','N','','Ls','LT']

      
    # select options based on user input
    dimx = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'dimx'].values[0]
    dimy = dv.loc[(dv['plot-type']==plot_input)&(dv['label']==str(var1_input)),'dimy'].values[0]
    rlist = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx, dimy] and not ('Surface' in var1_input and o == 'lev')]

    combined_list = rlist
    if var2_input is not None:
       rlist2 = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx, dimy] and not ('Surface' in var2_input and o == 'lev')] 
       combined_list = rlist + rlist2
    if var3_input is not None:
       rlist3 = [o for o in ['lon', 'lat', 'lev', 'time', 'time_of_day_12'] if o not in [dimx, dimy] and not ('Surface' in var3_input and o == 'lev')] 
       combined_list = rlist + rlist2 + rlist3
    rlist = list(set(combined_list))
    dlist = [dimx,dimy]
    
    # go through rdmis assuming order lon,lat, lev, time, time_of_day_12
    text = []
 
    # first add variable names
    if "," in var_value:
       # Find the index of the last comma
       last_comma_index = var_value.rfind(',')

       # Reconstruct the modified var_value with the last comma replaced by an ampersand
       var_value_title = var_value[:last_comma_index] + ' &' + var_value[last_comma_index+1:]
    else:
       var_value_title = var_value
    text += [var_value_title]
    
    nval_options = {
       "lat_value":"ALL",
       "lon_value":"ALL",
       "lev_value":"Surface",
       "time_value":"ALL",
       "time_of_day_12_value":"ALL"}

    for i in dlist:
       
       # quickly identify tthe unit based each coordinate (using unit_options)
       dim_index = 0 if i=='lon' \
          else (1 if i=='lat' else (3 if i=='time' else (2 if i=='lev' else 4)))
       unit = unit_options[dim_index] if i != 'lev' else ('Pa' if vcords_input == 'pstd' else 'm')

       # grab user input for each dimension
       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if user_input == 'ALL':
          nval_options[f"{i}_value"]="ALL"

       else:
          # set dimension name based on i or (for vertical level) vcords_input
          dim = vcords_input if i == "lev" else i
          nearest_value1,nearest_value2 = cf.find_nearest_value(f_path,dim,user_input)
          if "," in user_input:   # range of values selected
             nval_options[f"{i}_value"] = f"{nearest_value1:.2f}-{nearest_value2:.2f}{unit}"
          else: # single value selected
             nval_options[f"{i}_value"] = f"{text_options[dim_index][1]}{nearest_value1:.2f}{unit}"

    # now go through other user inputs (other than dimensions)
    for i in rlist:    # i dimension name, dim_input = "all, int, or range"

       # quickly identify tthe unit based each coordinate (using unit_options)
       dim_index = 0 if i=='lon' \
          else (1 if i=='lat' else (3 if i=='time' else (2 if i=='lev' else 4)))
       unit = unit_options[dim_index] if i != 'lev' else ('Pa' if vcords_input == 'pstd' else 'm')

       # grab user input for each extra dimension
       user_input = lon_input if i=='lon' \
          else (lat_input if i=='lat' else (areo_input if i=='time' else (lev_input if i=='lev' else tod_input)))

       if user_input == 'ALL':
          text += [text_options[dim_index][0]]
          nval_options[f"{i}_value"]=text_options[dim_index][0]

       else:
          dim = vcords_input if i == "lev" else i
          nearest_value1,nearest_value2 = cf.find_nearest_value(f_path,dim,user_input)
          if "," in user_input:   # range of values selected
             text += [f'@ {text_options[dim_index][1]} {nearest_value1:.2f}-{nearest_value2:.2f}{unit}']
             nval_options[f"{i}_value"] = f"{nearest_value1:.2f}-{nearest_value2:.2f}{unit}"
          else: # single value selected
             nval_options[f"{i}_value"] = f"{text_options[dim_index][1]}{nearest_value1:.2f}{unit}"
             text += [f"@{text_options[dim_index][1]}{nearest_value1:.2f}{unit}"]

    # FORMAT PLOT TITLE
    # order options (average first, if more than one average combine)
    #e.g. Global Diurnal Average @ X Pa
    text = sorted(text, key=lambda x: 'Average' in x, reverse=True)

    # Join the strings into a single text string
    text = ' '.join(text)

    # If both "Meridional Average" and "Zonal Average" appear, replace with "Global"
    # and move to start of string
    if "Meridional Average" in text and "Zonal Average" in text:
       text = text.replace('Meridional Average ','')
       text = text.replace('Zonal Average','Global')
       # Find the index of "Global" & move to start of string
       global_index = text.find("Global")
       text = "Global " + text[:global_index] + text[global_index + len("global"):]

    # If the word "Average" appears more than once, remove the first instance
    num_averages = text.count("Average")  # Count the number of occurrences of "Average"
    if num_averages > 1:
       last_average_index = text.rindex("Average")  # Find the index of the last occurrence of "Average"
       text = text.replace("Average", "", num_averages - 1)  # Replace all but the last occurrence of "Average"
    
    # If "@" appears more than once, remove the all but the first insttance
    if text.count('@') > 1:
       parts = text.split('@', 1)  # split the string at the first "@" character
       text = parts[0]+'@' + parts[1].replace('@', '')  # join the parts back together, keeping only the first "@"
    
    # format case of title & descripton
    plot_title = text.title()
    # Define a regular expression pattern to match the content inside square brackets
    pattern = r'\[.*?\]'
    # Find all occurrences of the pattern in the string
    matches = re.findall(pattern, text)
    # Replace the content inside the brackets with a placeholder (e.g., '###')
    lowercased_string = re.sub(pattern, '###', text.lower())
    # Restore the original content inside the brackets
    for match in matches:
       plot_description = lowercased_string.replace('###', match, 1)

    # GENERATE TEXT FOR POP-UP/README
    # save the file name and simulation directory
    last_slash_index = f_path.rfind('/')
    # Find the index of the second-to-last slash using the previously found index
    second_last_slash_index = f_path.rfind('/', 0, last_slash_index)
    # Get the file name from the second-to-last slash to the end of the string
    file_name = f_path[second_last_slash_index + 1:]
  
    final_txt = f'''This plot was generated using data from the NASA Ames FV3 Mars Global Climate Model, {simulation["name"]}. The full data is archived on the NASA Planetary Science (?) Data Portal and can be accessed and downloaded at the link below.

The model scenario has {simulation["spatial_resolution"]} degree spatial resolution with {simulation["vertical_resolution"]} vertical layers on a {simulation["vertical_grid"]}, and includes {simulation["dust_scenario"]}. {simulation["water_scenario"]}. {simulation["aerosol_scenario"]}. {simulation["rt_scenario"]}.

{time_averaging}. {vertical_interpolation}. A full description of the model configuration and details of the physics can be found in Kahre+2023 and the NASA Ames FV3 User Manual.

The plot/dataset shows the {plot_description} based on the following user inputs. Values listed represent the closest value in the model output. For example, if the user specifies the latitude range 30S,30N, the plot will show model data between {nearest_value1_samp}S and {nearest_value2_samp}N. 

Simulation Name: NASA Ames FV3 Mars Global Climate Model, {simulation["name"]}
Variable(s): {var_value}
Latitude: {nval_options["lat_value"]}
Longitude: {nval_options["lon_value"]}
Atmospheric Level: {nval_options["lev_value"]}
Solar Longitude (Ls): {nval_options["time_value"]}
Local Time: {nval_options["time_of_day_12_value"]}
File Name: {file_name}'''
    
    return html.Pre(final_txt, className='pre-style'), plot_title


