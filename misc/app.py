from dash import Dash, html, dcc
import dash_mantine_components as dmc
import dash


app = Dash(__name__, use_pages=True)

server = app.server  # need this line to deploy to cloud

app.layout = html.Div(
    [
        dmc.Header(
            height=60,
            children=[
                html.H1(children="SlashML + Dash", style={"textAlign": "center"}),
            ],
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
