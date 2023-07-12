#Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Define the Citation Page Description Card structure
def Citation():

   first_card = dbc.Card([
      dbc.CardBody([
         html.H4("How to Cite the MCMC Data Portal", className="card-title"),
         html.P(
            "Citation List for FV3 model data for each scenario, "
            "for dust scenarios?, "
            "for web server data or CAP use?",
            className="card-text"),
         dbc.Accordion([
            dbc.AccordionItem([
               html.P(html.Span("Placeholder Text")),
            ], title="Placeholder Accordian Item 1"),
            dbc.AccordionItem([
               html.P(html.Span("Placeholder Text")),
            ], title="Placeholder Accordian Item 2"),
         ],start_collapsed=True, className="my-accordion"),
      ]),
   ])

   layout = html.Div([
      dbc.Row(first_card),
      ],className='card_links')

   return layout

