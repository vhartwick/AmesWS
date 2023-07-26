
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc


ABAR_STYLE = {
   "position": "fixed",
   "top": "200px",
   "right": 0,
   "bottom": "60px",
   "width": "18rem",
   "padding": "1rem 2rem",
   "background-color":'#252930',
   "color":"white",
   "overflow-y":"scroll",
}

BUTTON_STYLE = {
   "background-color":"#7B1112",
   "color":"white",
}

# Define the navbar structure
def Abar():

   layout = html.Div([
     
        html.Div([
             dbc.Button("Generate Plot", id="btn-doit-txt",
                style=BUTTON_STYLE,className="d-grid gap-2"),

             html.Hr(),
             
             html.Div([
                 dbc.Button("Download Data", id="btn-download",
                    disabled=True,style=BUTTON_STYLE,className="d-grid gap-2"),
                 dcc.Download(id="download-fig"),
             ]),

             dcc.Checklist(id="output-format-checklist",
                 options=[
                    {'label': '   PNG Image', 'value': 'png'},
                    {'label': '   NetCDF File', 'value': 'ncdf'},
                    {'label': '   CSV Text File', 'value': 'csv'},
                 ],style={"padding":"10px"}),
            
             html.P("To Download All Simulation Data:",style={"color":"white"}),
             dbc.CardLink("CLICK HERE", href="https://github.com/NASA-Planetary-Science/AmesCAP",target="_blank",style={"color":"white"}), 
             html.Hr(),


#             dbc.Popover([
#                dbc.PopoverHeader("Would you like to download any additional variables?"),
#                dbc.PopoverBody([
#                   dbc.Checklist(id="output-all-data",
#                     options = [
#                       {'label':'ALL VARIABLES','value':'ALL'},
#                     ],style={"backgroundColor":"#252930","color":"white"}),
#                   html.Hr(),
#                   dbc.Accordion([
#                      dbc.AccordionItem(                  
#                         dbc.Checklist(id="output-column-data-checklist",value=[],
#                            style={"backgroundColor":"#252930","color":"white"}),
#                      title="Column Variables"),             
#                   ],id="column-accordion",start_collapsed=True, className="my-accordion"),
#                   html.Hr(),
#                   dbc.Accordion([
#                      dbc.AccordionItem(                  
#                         dbc.Checklist(id="output-data-checklist",value=[],
#                            style={"backgroundColor":"#252930","color":"white"}),
#                      title="Sliced Variables"),                         
#                   ],start_collapsed=True, className="my-accordion"),
#                   html.Hr(),
#                   html.P("To Download All Simulation Data",style={"color":"white"}),
#                   dbc.CardLink("CLICK HERE", href="https://github.com/NASA-Planetary-Science/AmesCAP",target="_blank",style={"color":"white"}),
#                ]),
#             ],
#             id = "output-data-popover",
#             target="output-format-checklist",
#             trigger="click",
#             placement = "left",
#             style={"border": "1px solid white","backgroundColor":"#252930","color":"white","display":"block"},
#             ),           
#             
             dbc.Accordion([ 
                dbc.AccordionItem([
                   html.P("Our Group:"),
                   dbc.CardLink("MCMC", href="https://www.nasa.gov/mars-climate-modeling-center-ames",target="_blank"),
                   html.Hr(),
                   html.P("Information about the Community Analysis Pipeline:"),
                   dbc.CardLink("CAP", href="https://github.com/NASA-Planetary-Science/AmesCAP",target="_blank"),
                   html.Hr(),
                   html.P("Model Configuration"),
                   html.Hr(),
                   html.P("How to Cite the Ames WS Name"),
                   #dbc.Collapse(
                   #   dbc.Card("How to Cite the Ames OFFICIAL NAME OF WS",
                   #      dbc.CardBody(
                   #         """
                   #            To cite the Ames NAME, use the following citation:
                   #            - Google. (n.d.). Retrieved Month Day, Year, from https://www.google.com
                   #         """
                   #      ),
                   #   ),id="amesws-citation-collapse",is_open=False,
                   #),
                ], title="Want to Learn More?"),
             ],start_collapsed=True),
             
             dcc.Store(id="dim1-sav"),
             dcc.Store(id="dim2-sav"),
             dcc.Store(id="time-dim-sav"),
             dcc.Store(id="vert-dim-sav"),
             dcc.Store(id="var1-sav"),
             dcc.Store(id="var2-sav"),
             dcc.Store(id="var3-sav"),
             #dcc.Store(id="time-var-sav"),
             #dcc.Store(id="vert-var-sav"),
        ]),
   #],style=ABAR_STYLE) # close html div
   ],className="action_bar") # close html div

    
   return layout






