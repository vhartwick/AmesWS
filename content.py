# contains callbacks imports so they can be registered with Dash app instance
# content.py

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from index import app

# Connect to your app pages
from pages import home,model,citation,analytics

# Connect the header & navbar (which appear on all pages) to the index
from components import header

# Load all callbacks
from components.callbacks import update_variable1_options
from components.callbacks import update_variable2_options
from components.callbacks import update_variable3_options
from components.callbacks import do_it
from components.callbacks import update_tooltips
from components.callbacks import second_hover
from components.callbacks import update_level_input
from components.callbacks import download_data
from components.callbacks import update_plotting_options
from components.callbacks import update_plot_title
from components.callbacks import user_warning
from components.callbacks import update_mainfig_size
from components.callbacks import update_modal_text
from components.callbacks import toggle_modal
#from components.callbacks import reset_page
from components import footer, sidebar, graph_window, abar

# define the components
header = header.Header()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    header,
    html.A("Test Text", style={"color":"white"}),
    html.Div(id='page-content', children=[]),
])

app.config.suppress_callback_exceptions = True

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
       return home.layout
    if pathname == '/analytics':
        return analytics.layout
    if pathname == '/model':
        return model.layout
    if pathname == '/citation':
        return citation.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"



