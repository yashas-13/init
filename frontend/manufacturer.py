from dash import html


def layout():
    """Manufacturer dashboard layout."""
    return html.Div([
        html.H2("Manufacturer Dashboard"),
        html.P("Manage products, users and approvals here."),
    ])
