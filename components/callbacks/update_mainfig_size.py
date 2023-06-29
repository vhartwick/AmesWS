#================================================================================
# Callback to Change Main Figure Size
#================================================================================
from index import app
import dash
from dash.dependencies import Input, Output, State

@app.callback(
   Output('main_figure', 'style'),
   [Input('plot_input', 'value')]
)
def update_figure_style(plot_type):
   if '1D' in plot_type:
       return {'width': '70vw', 'height': '48vh'}
   else:
       return {'width': '48vw', 'height': '48vh'}
