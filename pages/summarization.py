from dash import Dash, DiskcacheManager, html, ctx, register_page, callback
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
from slashml import TextSummarization, services
import diskcache
import json
from utils.cards import summarizeCards
from utils.artifacts import sampleTextKing, sampleTextShakespeare, sampleTextSagan
from utils.upload import filePicker
import base64


register_page(
    __name__,
    path="/summarization",
    title="Summarization API",
    name="SlashML Summarization API",
)


cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

provider_choices = TextSummarization.ServiceProvider.choices()

layout = html.Div(
    style={"padding": "10px"},
    children=[
        dmc.Anchor(
            dmc.Button("Home", id="return-to-home", variant="outline"), href="/"
        ),
        html.Br(),
        html.Br(),
        dmc.Alert(
            """Following is a demo of our summarization API. Click on an example or summarize your own text.
            """,
            title="Welcome!",
            color="violet",
        ),
        html.Div(
            [
                dmc.Title(f"Examples", order=3, style={"margin-top": "10px"}),
                summarizeCards(),
                filePicker(id="upload-data", accept=".txt"),
                dmc.Textarea(
                    id="summarization-input",
                    label="Input Text",
                    placeholder="Enter text that you want to summarize",
                    style={"width": "100%"},
                    minRows=15,
                    required=True,
                ),
                dmc.TextInput(
                    id="api-token",
                    label="API token",
                    placeholder="Enter token here",
                    style={"width": 350},
                ),
                dmc.Select(
                    label="Service Provider",
                    placeholder="Select one",
                    id="provider-dropdown",
                    value=provider_choices[0],
                    data=provider_choices,
                    style={"width": 200, "marginBottom": 10},
                ),
                dmc.Text(id="selected-value"),
            ]
        ),
        html.Br(),
        dmc.Button("Submit", id="btn-submit-summarization-request", variant="gradient"),
        html.Br(),
        html.Br(),
        html.Div(id="output-container", children=""),
    ],
)


@callback(
    Output("summarization-input", "value", allow_duplicate=True),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
    prevent_initial_call=True,
)
def update_output(contents, *_):
    if contents.startswith("data:text/plain;base64,"):
        contents = contents[len("data:text/plain;base64,") :]
    return base64.b64decode(contents).decode("utf-8")


@callback(
    Output("summarization-input", "value", allow_duplicate=True),
    Input("card-summarize-king", "n_clicks"),
    Input("card-summarize-shakespeare", "n_clicks"),
    Input("card-summarize-sagan", "n_clicks"),
    prevent_initial_call=True,
)
def prompt_pressed(*_):
    if "card-summarize-king" == ctx.triggered_id:
        return sampleTextKing()
    if "card-summarize-shakespeare" == ctx.triggered_id:
        return sampleTextShakespeare()
    if "card-summarize-sagan" == ctx.triggered_id:
        return sampleTextSagan()


@callback(
    Output("output-container", "children"),
    Input("btn-submit-summarization-request", "n_clicks"),
    State("summarization-input", "value"),
    State("provider-dropdown", "value"),
    State("api-token", "value"),
    background=True,
    prevent_initial_call=True,
    manager=background_callback_manager,
    running=[
        (Output("btn-submit-summarization-request", "disabled"), True, False),
        (
            Output("btn-submit-summarization-request", "children"),
            "Running ...",
            "Submit",
        ),
    ],
)
def submit_request(_, input_text, provider_str, api_token):
    response = None
    div_children = []

    if input_text == "":
        response = {"error": "Input text cannot be empty"}

    else:
        api_key = None if api_token == "" else api_token
        response = services.summarize_text(
            input_text, TextSummarization.ServiceProvider(provider_str), api_key
        )

        if (
            response.status
            and response.summarization_data
            and response.status == "COMPLETED"
        ):
            div_children.extend(
                [
                    dmc.Text("Summary", color="blue", size="xl", weight=700),
                    dmc.Text(response.summarization_data, color="blue", size="xl"),
                ]
            )

    div_children.extend(
        [
            html.Br(),
            dmc.Textarea(
                id="summarization-output",
                value=json.dumps(response, indent=2),
                label="JSON Response",
                style={"width": "100%"},
                minRows=10,
                disabled=True,
            ),
        ]
    )

    return html.Div(div_children)
