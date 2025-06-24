"""Dash application to provide a minimal UI."""

# This module is kept separate to allow future expansion
# of the UI without impacting Flask API routes.

import dash
from dash import Dash, html, dcc
from . import manufacturer, cfa, stockist


def create_dash(server):
    """Factory to create Dash app and attach to given Flask server."""
    dash_app = Dash(__name__, server=server, url_base_pathname="/dashboard/", suppress_callback_exceptions=True)

    dash_app.layout = html.Div([
        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ])

    @dash_app.callback(
        dash.dependencies.Output("page-content", "children"),
        [dash.dependencies.Input("url", "pathname")],
    )
    def display_page(pathname):
        if pathname == "/dashboard/manufacturer":
            return manufacturer.layout
        if pathname == "/dashboard/cfa":
            return cfa.layout
        if pathname == "/dashboard/stockist":
            return stockist.layout
        return html.Div([
            html.H1("Pharma SCM Dashboard"),
            html.P("Select role dashboard."),
        ])
    return dash_app
