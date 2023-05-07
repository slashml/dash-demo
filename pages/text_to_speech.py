import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/text-to-speech",
    title="Text-to-Speech API",
    name="SlashML Text-to-Speech API",
)

layout = html.Div(
    children=[
        html.H1(children="Text to Speech Demo"),
    ]
)
