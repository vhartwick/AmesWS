
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.callbacks.do_it import blank_fig

#GW_STYLE = {
#   "position": "fixed",
##   "top": "200px",
#   "top":"20vh",
#   "left":"18vw"
#   "right":"18vw",
#   "height":"80vw",
##   "left": "18rem",
##   "right": "18rem",
##   "height":"700px",
#   "background-color":'#252930',
#   "color":"white",
#   "z-index":1,
#   "overflow-y":"scroll",
#}

TS_STYLE = {
   "position": "fixed",
   "top": "600px",
   "left":"18vw",
   "right":"25vw",
#   "left": "18rem",
#   "right": "18rem",
   "height":"200px",
   "background-color":'#252930',
   "color":"white",
}

MF_STYLE = {
   "position": "fixed",
   "top": "200px",
   "left": "18rem",
   "right": "18rem",
   "height":"400px",
   "background-color":'#252930',
   "color":"white",
}
# Define the navbar structure
def Graph_Window():
    layout = html.Div([
               dbc.Card("",id="fig-title", className='title_box'),
               dcc.Graph(figure=blank_fig(), id="figure_out",className='main_figure'),
               dcc.Graph(figure=blank_fig(), id="time_series",className='time_series'),
               dcc.Graph(figure=blank_fig(), id="vertical_profile",className='vertical_profile',style={"display":"none"}),
    ], className='graph_window')
    
    return layout






