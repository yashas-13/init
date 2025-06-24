from dash import html
from backend.version import VERSION  # display API version


def layout():
    """Manufacturer dashboard layout."""
    return html.Div([
        html.H2("Manufacturer Dashboard"),
        html.P("Manage products, users, batches and approvals here."),
        html.P("Use /api/batches to register production batches."),
        html.Small(f"Backend version: {VERSION}"),
    ])
