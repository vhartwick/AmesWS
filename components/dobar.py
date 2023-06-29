
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc


DO_BAR_STYLE = {
   "position": "fixed",
   "top": "200px",
   "right": 0,
   "width": "18rem",
   "padding": "1rem 2rem",
   "background-color":'#252930',
   "color":"white",
   "overflow-y":"scroll",
}

# Define the navbar structure
def Dobar():

    layout = html.Div([
          html.Div([
               dbc.Button("Generate Plot", id="btn-doit-txt",
                  style=BUTTON_STYLE,className="d-grid gap-2"),

               html.Hr(),
               #dbc.Button("Download Data", id="download-file",
               #    style=BUTTON_STYLE,className="d-grid gap-2"),
               #dcc.Checklist(id="export-data-checklist",
               #    options=[
               #       {'label': 'PNG image', 'value': 'png'},
               #       {'label': 'Netcdf File', 'value': 'ncdf'},
               #       {'label': '.csv text file', 'value': 'csv'},
               #    ],style={"padding":"10px"}),
               #html.Hr(),
               #dbc.Button("Want to Learn More?", color="primary"),
               #dbc.Card([
               #    dbc.CardImg(src="/static/images/placeholder286x180.png", top=True),
               #    dbc.Button("Want to Learn More?", color="primary"),
               #]),
               dcc.Store(id="dim1-sav"),
               dcc.Store(id="dim2-sav"),
               dcc.Store(id="time-dim-sav"),
               dcc.Store(id="vert-dim-sav"),
               dcc.Store(id="var1-sav"),
               dcc.Store(id="var2-sav"),
               dcc.Store(id="var3-sav"),
               dcc.Store(id="time-var-sav"),
               dcc.Store(id="vert-var-sav"),
         ]),
    ], style=DO_BAR_STYLE)

    return layout






