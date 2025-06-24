"""Dash application to provide a minimal UI."""

# This module is kept separate to allow future expansion
# of the UI without impacting Flask API routes.

from dash import Dash, html


def create_dash(server):
    """Factory to create Dash app and attach to given Flask server."""
    dash_app = Dash(__name__, server=server, url_base_pathname="/dashboard/")
    dash_app.layout = html.Div([
        html.H1("Pharma SCM Dashboard"),
        html.P("Data visualization will appear here."),
    ])
    return dash_app
