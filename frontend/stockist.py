from dash import html


def layout():
    """Stockist dashboard layout."""
    return html.Div([
        html.H2("Stockist Dashboard"),
        html.P("Submit orders and view approvals."),
    ])
