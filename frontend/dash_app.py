"""Dash application to provide a minimal UI."""

# This module is kept separate to allow future expansion
# of the UI without impacting Flask API routes.

from dash import Dash, html, dcc, Output, Input
from .manufacturer import layout as manufacturer_layout
from .cfa import layout as cfa_layout
from .stockist import layout as stockist_layout



def create_dash(server):
    """Factory to create Dash app and attach to given Flask server."""
    dash_app = Dash(__name__, server=server, url_base_pathname="/dashboard/")
    dash_app.layout = html.Div([

        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ])

    @dash_app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        if pathname.endswith("/manufacturer"):
            return manufacturer_layout()
        if pathname.endswith("/cfa"):
            return cfa_layout()
        if pathname.endswith("/stockist"):
            return stockist_layout()
        return html.Div([
            html.H1("Pharma SCM Dashboard"),
            html.P("Select a dashboard page."),
        ])


    return dash_app
