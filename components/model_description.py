#Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Define the Model Description Card structure
def Model():

   first_card = dbc.Card([
      dbc.CardBody([
         html.H4("Description of Simulation Configurations", className="card-title"),
         html.P(
            "Basic description of FV3 and shared characteristics of model configurations "
            "for example, C48 resolution, L56 etc. "
            "Then add dropdown to give more detailed description of each option: "
            "including dust and cloud scenario, etc",
            className="card-text"),
         dbc.Accordion([
            dbc.AccordionItem([
               html.P(html.Span("dust climatology from (Montabone ?), radiatively active clouds, simple cloud scheme description, water cycle?")),
            ], title="Base Simulation"),
            dbc.AccordionItem([
               html.P(html.Span("Simulation Description")),
            ], title="Simulation 2"),
            dbc.AccordionItem([
               html.P(html.Span("Simulation Description")),
            ], title="Simulation 3"),
         ],start_collapsed=True, className="my-accordion"),
      ]),
   ])

   second_card = dbc.Card([
      dbc.CardBody([
         html.H4("Description of Averaging, Post-Processing", className="card-title"),
         html.P(
            "Description of vertical interpolation, daily, diurnal and average time structures, etc",
            className="card-text"),
         dbc.Accordion([
            dbc.AccordionItem([
               html.P(html.Span("pressure, altitude above surface, altitude wrt aeroid")),
            ], title="Vertical Interpolation"),
            dbc.AccordionItem([
               html.P(html.Span("5 sol average, 1 hour outputs if time of day specified, instantaneous description")),
            ], title="Time Averaging"),
         ],start_collapsed=True, className="my-accordion"),

      ]),
   ])


   layout = html.Div([
      dbc.Row(first_card),
      html.Hr(),
      dbc.Row(second_card),
      ],className='card_links')

   return layout

