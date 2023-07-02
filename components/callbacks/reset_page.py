#================================================================================
# Callback to Reset Page After User Interacts with First Dropdown
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from dash import html,no_update
from dash.exceptions import PreventUpdate

@app.callback(Output('url', 'pathname'),
              Input('plot-type-dropdown', 'value'),
              State('url', 'pathname'))

def reset_page(value, current_pathname):
    if value is not None:
        return '/'
    else:
        return current_pathname



