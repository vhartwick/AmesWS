# Dash app definition


import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
        __name__,
        external_stylesheets=[
           dbc.themes.LUX,
           "./assets/style.css"
        ], # fetch the proper css items we want
        meta_tags = [
            { # check if device is a mobile device. Required for mobile styling
              'name':'viewport',
              'content':'width=device-width, initial-scale=1'
             }
        ],
        suppress_callback_exceptions=True,
   )

 
