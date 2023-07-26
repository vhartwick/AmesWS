
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.callbacks.do_it import blank_fig

BUTTON_STYLE = {
   "background-color":"#7B1112",
   "color":"white",
   "display":"none",
}

# Define the navbar structure
def Footer():
    layout = html.Div([
               dbc.Button("Additional Plot Information", id="btn-modal",
                  n_clicks=0,style=BUTTON_STYLE,className="d-grid gap-2"),
               dbc.Modal([
                  dbc.ModalHeader(dbc.ModalTitle("Information about Model Configuration and User Inputs used to generate this plot")),
                  dbc.ModalBody([
                     html.Div(id="modal-txt")
                  ]),
               ], id="modal", is_open=False)

    ], className='footer')
    
    return layout


