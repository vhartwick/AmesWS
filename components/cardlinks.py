
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Define the navbar structure
def Cardlinks():

   first_card = dbc.Card([
      dbc.CardBody([
         html.H4("Welcome to the Mars Climate Modeling Center Data Portal!", className="card-title"),
         html.P(
            "Some quick example text to build on the card title and "
            "make up the bulk of the card's content.",
            className="card-text"),         
         ]),
      ])


   second_card = dbc.Card([
      dbc.CardImg(src="/assets/images/Current_Mars_Diagram_Final_Apr12.png",top=True),
      dbc.CardBody([
         html.H4("Model Configurations", className="card-title"),
         html.P(
            "Some quick example text to build on the card title and "
            "make up the bulk of the card's content.",
            className="card-text"),
         dbc.Button("Go somewhere", color="primary", href="/model"),
         ]),
      ])

   third_card = dbc.Card([
      dbc.CardImg(src="/assets/images/Current_Mars_Diagram_Final_Apr12.png",top=True),
      dbc.CardBody([
         html.H4("NAS Data Portal", className="card-title"),
         html.P(
            "To access the raw data set from each simulation ... "
            "additional lines of text.",
             className="card-text"),
         dbc.Button("MCMC Data Portal", color="primary",
            href="https://data.nas.nasa.gov/mcmc/"),
         ]),
      ])

   fourth_card = dbc.Card([
      dbc.CardImg(src="/assets/images/Current_Mars_Diagram_Final_Apr12.png",top=True),
      dbc.CardBody([
         html.H4("CAP Github & Tutorial", className="card-title"),
         html.P(
            "Description of the Community Analysis Pipeline "
            "additional lines of text.",     
            className="card-text"),
         dbc.Button("AmesCAP", color="primary",
            href="https://github.com/NASA-Planetary-Science/AmesCAP"),
         ]),
      ])
   layout = html.Div([
      dbc.Row(first_card),
      html.Hr(),
      dbc.Row([
         dbc.Col(second_card, width=4),
         dbc.Col(third_card,width=4),
         dbc.Col(fourth_card,width=4),
      ]),
   ], className='card_links')
                      
   return layout






