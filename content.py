# contains callbacks imports so they can be registered with Dash app instance
# content.py

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from index import app
from components.callbacks import update_variable1_options
from components.callbacks import update_variable2_options
from components.callbacks import update_variable3_options
from components.callbacks import do_it
from components.callbacks import update_tooltips
from components.callbacks import second_hover
from components.callbacks import update_level_input
from components.callbacks import download_data
from components.callbacks import update_plotting_options
from components.callbacks import update_modal_text
from components.callbacks import update_plot_title
from components.callbacks import user_warning
from components.callbacks import update_mainfig_size
#from components.callbacks import reset_page
from components import header, footer, sidebar, graph_window, abar

# define the components
header = header.Header()
sidebar = sidebar.Sidebar()
graph_window = graph_window.Graph_Window()
abar = abar.Abar()

app.layout = html.Div([dcc.Location(id="url"),
                header,sidebar,graph_window,abar], style={'background_color':'#252930'})


