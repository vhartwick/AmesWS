
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
                     html.Div(id="modal-txt"),
                     dbc.CardLink("Link to Full Dataset", href="https://data.nas.nasa.gov/mcmc/",target="_blank",style={"color":"#7B1112"}),
                     html.Br(),
                     dbc.CardLink("Description of Vertical Interpolation Routines in CAP",href="https://github.com/NASA-Planetary-Science/AmesCAP/blob/master-dev/tutorial/CAP_lecture.md#4-marsinterppy---interpolating-the-vertical-grid", target="_blank",style={"color":"#7B1112"}), 
                     html.Br(),
                     dbc.CardLink("NASA Ames FV3 User Manual",href="https://data.nas.nasa.gov/mcmc/",target="_blank",style={"color":"#7B1112"}),
                     html.Br(),
                     dbc.CardLink("Community Analysis Pipeline (CAP) User Manual",href="https://data.nas.nasa.gov/mcmc/",target="_blank",style={"color":"#7B1112"}),
                     html.Br(),
                     dbc.CardLink("Kahre et al., 2023", href="https://data.nas.nasa.gov/mcmc/",target="_blank",style={"color":"#7B1112"}),
                  ]),
               ], id="modal", is_open=False)

    ], className='footer')
    
    return layout


