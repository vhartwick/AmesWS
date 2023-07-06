# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc


import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from components import cardlinks

# define the components
card_links = cardlinks.Cardlinks()

layout = html.Div(card_links, style={'background_color':'#252930'})
#                sidebar,graph_window,abar], style={'background_color':'#252930'})
