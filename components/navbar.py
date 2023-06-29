# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

logo = "/assets/MCMC_Square.png"

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                html.A(
                   # Use row and col to control vertical alignment of logo / brand
                   dbc.Row(
                       [
                           dbc.Col(html.Img(src=logo, height="30px")),
                           dbc.Col(dbc.NavbarBrand("MCMC", className="ms-2")),
                       ],
                       align="center",
                       className="g-0",
                   ),
                   href="https://plotly.com",
                   style={"textDecoration": "none"},
               ),
            ] ,
            color="dark",
            dark=True,
        ),
    ])

    return layout

## Define the navbar structure
#def Navbar():
#
#    layout = html.Div([
#        dbc.NavbarSimple(
#            children=[
#                dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
#                dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
#            ] ,
#            brand="Multipage Dash App",
#            brand_href="/page1",
#            color="dark",
#            dark=True,
#        ), 
#    ])
#
    return layout
