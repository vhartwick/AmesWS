
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.callbacks.do_it import blank_fig

GW_STYLE = {
   "position": "fixed",
   "top": "200px",
   "left": "18rem",
   "right": "5rem",
   "bottom":"60px",
   #"height":"493px",
   "background-color":'#252930',
   "color":"white"
}



BUTTON_STYLE = {
   "background-color":"#7B1112",
   "color":"white"
}
# Define the navbar structure
def Graph_Window():

    layout = html.Div([
          html.Div([
             dcc.Graph(figure=blank_fig(), id="figure_out"),
          ]),
          html.Div([       # hover graphs
             dcc.Graph(figure=blank_fig(), id='first_hover'),
             dcc.Graph(figure=blank_fig(), id='second_hover'),  
          ]), 
   ], style=GW_STYLE)
     
    return layout






