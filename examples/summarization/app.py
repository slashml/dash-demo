from dash import Dash, html, page_container, DiskcacheManager, ctx, callback
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
from slashml import TextSummarization
import diskcache
import json
import base64
import time

from utils.cards import summarizeCards
from utils.artifacts import sampleTextKing, sampleTextShakespeare, sampleTextSagan
from utils.upload import filePicker

# TODO: Move to slashml package
def summarize_text(text, service_provider, api_key):
    # Initialize model
    model = TextSummarization(api_key=api_key)

    # Submit request
    job = model.submit_job(text=text, service_provider=service_provider)

    assert job.status != "ERROR", f"{job}"
    print(f"Job ID: {job.id}")

    # Check job status
    response = model.status(job.id, service_provider=service_provider)

    # Keep checking job status until the task is complete
    while response.status == "PENDING":
        print(f"Response = {response}. Retrying in 30 seconds")
        time.sleep(30)
        response = model.status(job.id, service_provider=service_provider)

    return response


app = Dash(__name__)

server = app.server  # need this line to deploy to cloud


cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

provider_choices = TextSummarization.ServiceProvider.choices()

app.layout = html.Div(
    style={"padding": "10px"},
    children=[
        dmc.Header(
            height=60,
            children=[
                html.H1(children="SlashML + Dash", style={"textAlign": "center"}),
            ],
        ),
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


@app.callback(
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


@app.callback(
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


@app.callback(
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

        service_provider = TextSummarization.ServiceProvider(provider_str)
        response = summarize_text(input_text, service_provider, api_key)

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


if __name__ == "__main__":
    app.run_server(debug=True)
