from dash import html


def layout():
    """CFA dashboard layout."""
    return html.Div([
        html.H2("CFA Dashboard"),
        html.P("Track inventory and dispatch requests."),
    ])
