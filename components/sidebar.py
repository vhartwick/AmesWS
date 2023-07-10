
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Define the navbar structure
def Sidebar():

   layout = html.Div([
    
        html.Div(["Model Scenario",
           dcc.Dropdown(id="model-dropdown",
              options = [
                 {'label': 'Background Dust Climatology', 'value':'sim1'},
               ],
               style={"backgroundColor":"#252930"}, value='sim1'),
        ]),
 
        html.Div([
           "Plot Selection",
           dcc.Dropdown(id="plot-type-dropdown",
             options=[
               {'label': '(2D) Lat/Lon Map', 'value': '2D_lon_lat'},
               {'label': '(2D) Lat/Altitude Cross Section', 'value': '2D_lat_lev'},
               {'label': '(2D) Lon/Altitude Cross Section', 'value': '2D_lon_lev'},
               {'label': '(2D) Latitude/Time Series', 'value': '2D_time_lat'},
               {'label': '(2D) Altitude/Time Series', 'value': '2D_time_lev'},
               {'label': '(2D) Longitude/Time Series', 'value': '2D_time_lon'},
               {'label': '(1D) Time Series', 'value': '1D_time'},
               {'label': '(1D) Latitude', 'value': '1D_lat'},
               {'label': '(1D) Longitude', 'value': '1D_lon'},
               {'label': '(1D) Altitude Profile', 'value': '1D_lev'},
               {'label': '(1D) Diurnal Cycle 5 Sol Average', 'value': '1D_diurn'},
               {'label': '(1D) Diurnal Cycle Instantaneous', 'value': '1D_daily'},
             ],
          style={"backgroundColor":"#252930"}, value='1D_time'),
        ]),

        html.Div([html.Hr()]),
   
        html.Div([
           "Variable Selection",
           dcc.Dropdown(id="variable1-dropdown",
              style={"backgroundColor":"#252930"}),
        ]),

        html.Div([
           "Second Variable Selection",
           dcc.Dropdown(id="variable2-dropdown",
              style={"backgroundColor":"#252930"}),
        ]),

        html.Div([
           "Third Variable Selection",
           dcc.Dropdown(id="variable3-dropdown", 
              style={"backgroundColor":"#252930","display":"none"}),
        ],id="variable3-text",style={"display":"none"}),

        html.Div([html.Hr()]),

        html.Div([
           "Vertical Coordinates",
           dcc.RadioItems(id="vertical-coordinates-radio",
               options=[
                  {'label': '   Pressure [Pa]', 'value': 'pstd'},
                  {'label': '   Altitude above ground level [m]', 'value': 'zagl'},
                  {'label': '   Altitude with respect to ref areoid [m]', 'value': 'zstd'},
               ],
           value='pstd'),
        ]),

        html.Div([html.Hr()]),
         
        html.Div([
           dbc.Accordion([ 
              dbc.AccordionItem([
                 dcc.Input(id="lat-input",value='ALL', type='text'),
                 html.P(html.Span("Latitude",id="lat-input-txt")),
                 dbc.Tooltip({},target="lat-input-txt",id="lat-tooltip"),
                 dbc.Alert(id='lat-alert', color='danger', dismissable=True, is_open=False),

                 dcc.Input(id="lon-input",value='ALL', type='text'),
                 html.P("Longitude",id="lon-input-txt"),
                 dbc.Tooltip(target="lon-input-txt",id="lon-tooltip"),
                 dbc.Alert(id='lon-alert', color='danger', dismissable=True, is_open=False),
                 
                 dcc.Input(id="solar-longitude-input",value='ALL', type='text'),
                 html.P("Solar Longitude (Ls)",id="time-input-txt"),
                 dbc.Tooltip(target="time-input-txt",id="time-tooltip"),
                 dbc.Alert(id='ls-alert', color='danger', dismissable=True, is_open=False),
                 
                 dcc.Input(id="tod-input",value='ALL', type='text'),
                 html.P("Local Time",id="tod-input-txt"),
                 dbc.Tooltip(target="tod-input-txt",id="tod-tooltip"),
                 dbc.Alert(id='tod-alert', color='danger', dismissable=True, is_open=False),

                 dcc.Input(id="lev-input",value='ALL', type='text',
                     style={"display":"none"}),
                 html.P("Atmospheric Level", id='lev-input-txt',
                     style={"display":"none"}),
                 dbc.Tooltip(target="lev-input-txt",id='lev-tooltip'),
                 dbc.Alert(id='lev-alert', color='danger', dismissable=True, is_open=False),
              
              ], title="Additional Options"),
           ],start_collapsed=True, className="my-accordion"),
       ]),

       html.Div([html.Hr()]),


       # Plotting Options for Contours
       html.Div([
           dbc.Accordion([
              dbc.AccordionItem([
                 dcc.Dropdown(id="cmap-dropdown",
                    options=[
                       {'label': 'Oryel', 'value': 'Oryel'},
                       {'label': 'Viridis', 'value': 'viridis'},
                       {'label': 'Plasma', 'value': 'plasma'},
                       {'label': 'Magma', 'value': 'magma'},
                       {'label': 'Red/Blue', 'value': 'RdBu_r'},
                    ],
                 style={"backgroundColor":"#252930"}, value='None'),
                 html.P("Contour Color Map",id="cmap-dropdown-txt"),

                 dcc.Input(id="clev-input",value='DEFAULT', type='text'),
                 html.P(html.Span("Contour Range",id="clev-input-txt")),
                 dbc.Tooltip('Specify the desired range of contours "#,#"',target="clev-input-txt",id="clev-tooltip"),

                 dbc.Alert(id='clev-alert', color='danger', dismissable=True, is_open=False),


              ], title="Plotting Style Options"),
           ],start_collapsed=True, id="plotting-accordian",className="my-accordion"),
       ]),

       dcc.Location(id='url',pathname='/',refresh=True),
   ],className="sidebar_vlh") # close html div

    
   return layout






