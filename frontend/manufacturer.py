from dash import html
from backend.version import VERSION  # display API version


def layout():
    """Manufacturer dashboard layout."""
    return html.Div([
        html.H2("Manufacturer Dashboard"),
        html.P("Manage products, users and approvals here."),
        html.Small(f"Backend version: {VERSION}"),
    ])
