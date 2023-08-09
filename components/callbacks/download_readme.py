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
dv = df.var_data()

@app.callback(
    Output("download-readme","data"),
    Input("btn-download", "n_clicks"),
    [State("plot-type-dropdown", "value"),
    State("var1-sav", "data"),
    State("var2-sav", "data"),
    State("var3-sav", "data"),
    State("modal-txt", "children")],
    prevent_initial_call = True,
)

def download_readme(btn_clicks,plot_input,var1_input,var2_input,var3_input,modal_txt):

   # Execute on Button Click
   if btn_clicks != None:

      # Load data
      var1 = json.loads(var1_input)
      var1 = xr.DataArray.from_dict(var1)
      var1_name = var1.name

      if var2_input:
         var2 = json.loads(var2_input)
         var2 = xr.DataArray.from_dict(var2)
         var2_name =var2.name
      if var3_input:
         var3 = json.loads(var3_input)
         var3 = xr.DataArray.from_dict(var3)
         var3_name = var3.name

      # Create a temporary text file with the README content
      if var2_input and var3_input:
         readme_filename = f"{var1.name}_{var2.name}_{var3.name}_{plot_input}_README.txt"
      elif var2_input:
         readme_filename = f"{var1.name}_{var2.name}_{plot_input}_README.txt" 
      else:
         readme_filename = f"{var1.name}_{plot_input}_README.txt"

      # Extract the text content from the dictionary
      readme_content = modal_txt['props']['children']
      links =  "Link to Full Dataset: https://data.nas.nasa.gov/mcmc/, NASA Ames FV3 User Manual: https://data.nas.nasa.gov/mcmc,Community Analysis Pipeline (CAP) User Manual: https://data.nas.nasa.gov/mcmc, Kahre et al., 2023: https://data.nas.nasa.gov/mcmc/"
      with open(readme_filename, "w") as f:
         f.write(readme_content)

      return dcc.send_file(readme_filename)
