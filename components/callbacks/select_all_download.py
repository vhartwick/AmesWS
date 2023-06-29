#================================================================================
# Callback to Select All Options in Download Checklist
#================================================================================
from index import app
from dash.dependencies import Input, Output, State

@app.callback(
    [Output("output-column-data-checklist", "value"),
    Output("output-data-checklist","value")],
    Input("output-all-data", "value"),
    [State("output-column-data-checklist", "options"),
    State("output-data-checklist","options")],
    prevent_initial_call=True,
)

def select_all_none(all_selected, options1,options2):
    all_or_none1,all_or_none2 = [],[]
    print('all_selected',all_selected)
    print('options1',options1)
    all_or_none1 = [option["value"] for option in options1 if all_selected]
    all_or_none2 = [option["value"] for option in options2 if all_selected]
    return all_or_none1,all_or_none2


