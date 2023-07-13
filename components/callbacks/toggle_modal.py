#================================================================================
# Callback to Open and Close Modal Plot Info
#================================================================================
from index import app
from dash.dependencies import Input, Output, State


@app.callback(
    Output("modal", "is_open"),
    [Input("btn-modal", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


