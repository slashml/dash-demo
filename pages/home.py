import dash
from dash import html
import dash_mantine_components as dmc

dash.register_page(
    __name__,
    path="/",
    title="SlashML Dash Demos",
    name="SlashML Dash Demos",
)

layout = html.Div(
    children=[
        # html.P("Following is the list of Dash demos."),
        dmc.Text("Following is the list of our Dash demos", size="xl"),
        html.Br(),
        dmc.Anchor(
            dmc.Button("Summarization API", variant="outline"), href="/summarization"
        ),
        html.Br(),
        html.Br(),
        dmc.Anchor(
            dmc.Button("Text-to-Speech API", variant="outline"), href="/text-to-speech"
        ),
        html.Br(),
        html.Br(),
        dmc.Anchor(
            dmc.Button("Speech-to-Text API", variant="outline"), href="/speech-to-text"
        ),
        html.Br(),
        html.Br(),
    ]
)
