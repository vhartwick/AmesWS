# Import necessary libraries 
from dash import html
import dash_bootstrap_components as dbc


import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from components.callbacks import update_variable1_options
from components.callbacks import update_variable2_options
from components.callbacks import update_variable3_options
from components.callbacks import do_it
from components.callbacks import update_tooltips
#from components.callbacks import first_hover
from components.callbacks import second_hover
from components.callbacks import update_level_input
from components.callbacks import download_data
#from components.callbacks import update_download_options
from components.callbacks import update_plotting_options
from components.callbacks import update_plot_title
from components.callbacks import user_warning
from components.callbacks import user_warning
from components.callbacks import update_mainfig_size
from components import footer, sidebar, graph_window, abar

# define the components
sidebar = sidebar.Sidebar()
graph_window = graph_window.Graph_Window()
abar = abar.Abar()
footer = footer.Footer()

layout = html.Div([sidebar,graph_window,footer,abar], style={'background_color':'#252930'})
#                sidebar,graph_window,abar], style={'background_color':'#252930'})
