
# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

logo = "/assets/logos/MCMC_Square.png"
nasa_logo = "/assets/logos/NASA_logo.svg.png"

# Define the navbar structure
def Header():

    layout = html.Div([
      
      html.A(
                   # Use row and col to control vertical alignment of logo / brand
                   dbc.Row([
                           dbc.Col(html.Img(src=logo,height="170vh"),width=2),
                           dbc.Col([
                               #html.H2("Mars Climate Modeling Center <br/> Data Portal Web Interface",className="mcmc",
                               html.H2(["Mars Climate Modeling Center", html.Br(), "Data Portal Web Interface"],className="mcmc",
                                  style={"color": "#FCD7BC","font-family":"Helvetica Neue","letter-spacing":"10px"},
                               ), 
                           dbc.NavbarSimple([

                              dbc.NavItem(dbc.NavLink("Home", href="/home", style={"color":"white"})),
                              dbc.NavItem(dbc.NavLink("Analytics", href="/analytics", style={"color":"white"})),
                              dbc.NavItem(dbc.NavLink("Model Description", href="/model", style={"color":"white"})),
                              dbc.NavItem(dbc.NavLink("How to Cite", href="/citation", style={"color":"white"})),
                           ], color="#25293"),

#                               html.P(
#                                  "Some quick example text to build on the card title and make "
#                                  "up the bulk of the card's content.",
#                                  style={"color":"#BE8760","font-family":"Helvetica Neue"}),
                           ],
                           align='center',
                           className="align-items-center text-center b-0"),
                           dbc.Col(html.Img(src=nasa_logo, height="130vh",style={"margin-top": "15px"}),width=2,),
                   ]),

      ),

    ],className="header")
     
    return layout






