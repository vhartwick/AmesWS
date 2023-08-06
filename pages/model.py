# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc


import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from components import model_description

# define the components
card = model_description.Model()

layout = html.Div(card, style={'background_color':'#252930'})
