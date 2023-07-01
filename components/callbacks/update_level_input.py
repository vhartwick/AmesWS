#================================================================================
# Callback to Change Visibility of Level Input Based on Variable Choice
#================================================================================
from index import app
from components.sidebar import Sidebar
from dash.dependencies import Input, Output, State
from utils import data_function as df

# Load Database
dv = df.var_data()


@app.callback(
    [Output("lev-input", component_property="style"),
    Output("lev-input-txt", component_property="style")],
    Input("variable1-dropdown", "value"),
    State("plot-type-dropdown", "value"),
)

def change_lev_vis(var1_input,plot_input):

    # Set styles based on input values
    styles = {
        "lev-input": {"display": "none"},
        "lev-input-txt": {"display": "none"},
    }
    if "2D" in plot_input and "lev" not in plot_input:
        var1_display = "block" if str(var1_input) != "None" and "Surface" not in str(var1_input) else "none"
        styles["lev-input"] = {"display": var1_display}
        styles["lev-input-txt"] = {"display": var1_display}
    elif "1D" in plot_input and "lev" not in plot_input:
        var1_display = "block" if str(var1_input) != "None" and "Surface" not in str(var1_input) else "none"
        styles["lev-input"] = {"display": var1_display}
        styles["lev-input-txt"] = {"display": var1_display}

    return [styles[k] for k in ["lev-input","lev-input-txt"]]


