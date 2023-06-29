#================================================================================
# Callback to Download Figure & Data (Save Dimensions of Dynamic Zoom
#================================================================================
from index import app
from components.abar import Abar
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
from dash import html, dcc

# Load Variable Data
variable_list = df.variable_list()

# Load Variable Data
dv = df.var_data()

@app.callback(
    Output("download-fig","data"),
    Input("btn-download", "n_clicks"),
    [State('figure_out', 'relayoutData'),
    State("figure_out", "figure"),
    State("plot-type-dropdown", "value"),
    State("vertical-coordinates-radio", "value"),
    State("solar-longitude-input", "value"),
    State("lat-input", "value"),
    State("lon-input", "value"),
    State("lev-input", "value"),
    State("tod-input", "value"),
    State("dim1-sav", "data"),
    State("dim2-sav", "data"),
    State("var1-sav", "data"),
    State("var2-sav", "data"),
    State("var3-sav", "data"),
    State("output-format-checklist", "value"),
    State("fig-title","children")],
    prevent_initial_call = True,
)

def download_data(btn_clicks,relayoutData,fig_input,plot_input,vcords_input,areo_input,lat_input,lon_input,lev_input,tod_input,dim1_input,dim2_input,var1_input,var2_input,var3_input,output_format_input,fig_title_input):
 
   # Execute on Button Click
   if btn_clicks != None:

      # initialize variables
      dim1,dim2,var1,var2,var3=[],[],[],[],[]
      var1_zoom, var2_zoom, var3_zoom = None, None, None
      var1_name, var2_name, var3_name = None, None, None
      uvars,uvars_surf,uvars_col = {},{},{}
      
      # Load data
      dim1,dim2,var1 = json.loads(dim1_input),json.loads(dim2_input),json.loads(var1_input)
      dim1,dim2,var1 = xr.DataArray.from_dict(dim1),xr.DataArray.from_dict(dim2),xr.DataArray.from_dict(var1)
      var1_name = var1.name

      if var2_input:
         var2 = json.loads(var2_input)
         var2 = xr.DataArray.from_dict(var2)
         var2_name =var2.name
      if var3_input:
         var3 = json.loads(var3_input)
         var3 = xr.DataArray.from_dict(var3)
         var3_name = var3.name

      dim1_name, dim2_name=dim1.name,dim2.name
    
      # Select Based on Zoom
      try:
         var1_zoom = var1.sel(**{dim1_name:slice(int(relayoutData['xaxis.range[0]']),int(relayoutData['xaxis.range[1]'])),dim2_name:slice(int(relayoutData['yaxis.range[0]']),int(relayoutData['yaxis.range[1]']))})

         # Check for Second & Third Variables
         # Two variables
         if var2_input:
            var2_zoom = var2.sel(**{dim1_name:slice(int(relayoutData['xaxis.range[0]']),int(relayoutData['xaxis.range[1]'])),dim2_name:slice(int(relayoutData['yaxis.range[0]']),int(relayoutData['yaxis.range[1]']))})

         # Three Variables
         if var3_input:
            var3_zoom = var3.sel(**{dim1_name:slice(int(relayoutData['xaxis.range[0]']),int(relayoutData['xaxis.range[1]'])), dim2_name:slice(int(relayoutData['yaxis.range[0]']),int(relayoutData['yaxis.range[1]']))})
     
      except (ValueError, KeyError, TypeError):
         print('temporary print statemnent until I figure out how to exit try statement')

      # Tell the file where to go
      t = Path.cwd().joinpath("downloads")
      if not t.is_dir(): t.mkdir()


      # CSV 
      if output_format_input[0] == "csv" or (len(output_format_input) > 1 and output_format_input[1] == "csv") or (len(output_format_input) > 2 and output_format_input[2] == "csv"):
       
         # Tell the file where to go
         t = Path.cwd().joinpath("downloads/data")
         if not t.is_dir(): t.mkdir()
 
         # Zoom
         if var1_zoom is not None:
            var1_zoom =var1_zoom.to_dataframe()

            # Two variables 
            if var2_zoom is not None:
               var2_zoom = var2_zoom.to_dataframe()

            # Three Variables
            if var3_zoom is not None:
               var3_zoom = var3_zoom.to_dataframe()

            # Return the CSV file for the variables that exist
            if var2_input and var3_input:
               tnc = (var1.name+ "_" + var2.name+"_"+ var3.name + "_"+plot_input+"_zoom.csv")
               ds = pd.concat([var1_zoom, var2_zoom, var3_zoom], axis=1, ignore_index=True)
               return dcc.send_data_frame(ds.to_csv, filename=tnc)
            elif var2_input:
               tnc = (var1.name+ "_" + var2.name+"_"+plot_input+"_zoom.csv")
               ds = pd.concat([var1_zoom, var2_zoom], axis=1)
               return dcc.send_data_frame(ds.to_csv, filename=tnc)             
            else:
               tnc = (var1.name+ "_"+plot_input+"_zoom.csv")
               return dcc.send_data_frame(var1_zoom.to_csv, filename=tnc)

         else:
            var1 =var1.to_dataframe()
            var1.name = var1_name

            # Check for Second & Third Variables
            if var2_input:
               var2 = var2.to_dataframe()
               var2.name = var2_name
            if var3_input:
               var3 = var3.to_dataframe()
               var3.name = var3_name

            # Send to CSV
            if var2_input and var3_input:
               tnc = (var1.name+ "_" + var2.name+"_"+ var3.name +  "_" + plot_input+".csv")
               tnc_surf= (plot_input+"_surf.csv")
               ds = pd.concat([var1, var2, var3], axis=1) #, keys=[var1.name,var2.name,var3.name])
               return dcc.send_data_frame(ds.to_csv, filename=tnc)
            
            elif var2_input:
               tnc = (var1.name+ "_" + var2.name+"_"+plot_input+".csv")
               ds = pd.concat([var1, var2], axis=1) #, keys=[var1.name,var2.name])
               return dcc.send_data_frame(ds.to_csv, filename=tnc)

            else:
               tnc =(var1.name+ "_" + plot_input+".csv")
               return dcc.send_data_frame(var1.to_csv, filename=tnc)


      # NETCDF
      if output_format_input[0] == "ncdf" or (len(output_format_input) > 1 and output_format_input[1] == "ncdf"):
 
         # Tell the file where to go
         t = Path.cwd().joinpath("downloads/data")
         if not t.is_dir(): t.mkdir()

         # Select Based on Zoom
         if var1_zoom is not None:

             # Three Variables Selected
             if var2_input and var3_input:
                tnc =  t.joinpath(var1.name+"_"+var2.name+"_"+var3.name+"_"+plot_input+"_zoom.nc")
                var1_zoom.to_netcdf(tnc,mode='a')
                var2_zoom.to_netcdf(tnc,mode='a')
                var3_zoom.to_netcdf(tnc,mode='a')

             # Two Variables
             elif var2_input:             
                 tnc = t.joinpath(var1.name+ "_" + var2.name+"_"+plot_input+"_zoom.nc")
                 var1_zoom.to_netcdf(tnc,mode='a')
                 var2_zoom.to_netcdf(tnc,mode='a')
       
             else:
                 tnc = t.joinpath(var1.name+"_"+plot_input+"_zoom.nc")
                 var1_zoom.to_netcdf(tnc)
  
         else:

             # Three Variables Selected
             if var2_input and var3_input:
                tnc = t.joinpath(var1.name+"_"+var2.name+"_"+var3.name+"_"+plot_input+".nc")
                var1.to_netcdf(tnc, mode='a')
                var2.to_netcdf(tnc, mode='a')        
                var3.to_netcdf(tnc, mode='a')
        
             # Two variables
             elif var2_input:
                tnc = t.joinpath(var1.name+"_"+var2.name+"_"+plot_input+".nc")
                var1.to_netcdf(tnc, mode='a')
                var2.to_netcdf(tnc, mode='a') 
           
             # One Variable Selected
             else:
                tnc = t.joinpath(var1.name+"_"+plot_input+".nc")
                var1.to_netcdf(tnc)

         return dcc.send_file(tnc)

      #PNG
      if output_format_input[0] == "png":
         fig = go.Figure(fig_input)
         # Set the title of the figure
         fig.update_layout(
            title=fig_title_input,
            title_x=0.5,
            margin={'l':1,'r':1,'t':50,'b':1},
            font_color="black",
            font_size=11,
            paper_bgcolor="white",
            plot_bgcolor="white",
            legend=dict( 
               x=0.01,
               y=1.03,
               orientation='v',
               bgcolor='white',
               font=dict(
                 size=11,
                 color='black'))   
         )

         filename="Saved_Figure.png"
          # Tell the file where to go
         t = Path.cwd().joinpath("downloads/images")
         if not t.is_dir(): t.mkdir()

         t = t.joinpath(filename)
         fig.write_image(t,format='png',engine='kaleido')
