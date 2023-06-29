
# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

logo = "/assets/logos/MCMC_Square.png"

FOOTER_STYLE = {
  "position": "fixed",
  "bottom": 0,
  "width":"100%",
  "height":"40px",
  #"line-height":"20px", # vertically center text
  "background-color":'gray',
  "color":"white"
}

# Define the navbar structure
def Footer():

    layout = html.Div([
      
      html.A(
                   # Use row and col to control vertical alignment of logo / brand
                   dbc.Row([
                      dbc.Col(width=8),
                      dbc.Col([
                           html.P("More Information"),
                      ]),
                   ]),
      ),

    ],style=FOOTER_STYLE)
     
    return layout






