
# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Define the navbar structure
def Cardlinks():

   layout = html.Div([
               dbc.Card([ 
                  dbc.CardImg(src="/assets/images/Current_Mars_Diagram_Final_Apr12.png",top=True),
                  dbc.CardBody([
                     html.H4("Card title", className="card-title"),
                     html.P(
                       "Some quick example text to build on the card title and "
                       "make up the bulk of the card's content.",
                       className="card-text",
                     ),
                     dbc.Button("Go somewhere", color="primary"),
                  ]),
               ]), #,"style={"width": "18rem"}),     
            ], className = "card_links") 



           #html.P("To Download All Simulation Data:",style={"color":"white"}),
          # dbc.CardLink("CLICK HERE", href="https://github.com/NASA-Planetary-Science/AmesCAP",target="_blank",style={"color":"white"}),
           #html.P("Our Group:"),
           #dbc.CardLink("MCMC", href="https://www.nasa.gov/mars-climate-modeling-center-ames",target="_blank"),
           #html.P("Information about the Community Analysis Pipeline:"),
           #dbc.CardLink("CAP", href="https://github.com/NASA-Planetary-Science/AmesCAP",target="_blank"),

       #html.Div([
       #   html.P("Model Configuration"),
       #   html.P("How to Cite the Ames WS "),
       #]), 
   #],className="card_links") # close html div

    
   return layout






