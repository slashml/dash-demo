import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/speech-to-text",
    title="Speech-to-Text API",
    name="SlashML Speech-to-Text API",
)

layout = html.Div(
    children=[
        html.H1(children="Speech to Text Demo"),
    ]
)
