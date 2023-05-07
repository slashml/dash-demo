import dash_mantine_components as dmc


def generateCard(id, text, btn_text, citation=None, image_url=None):
    dmc_image = None
    if image_url is not None:
        dmc_image = dmc.Image(
            src=image_url,
            height=350,
        )

    return dmc.Card(
        children=[
            dmc.CardSection(dmc_image),
            dmc.Blockquote(
                text,
                cite=citation,
            ),
            dmc.Button(
                btn_text,
                id=id,
                variant="light",
                color="blue",
                fullWidth=True,
                mt="md",
                radius="md",
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"width": 350},
    )


def summarizeCards():
    return dmc.Grid(
        children=[
            dmc.Col(
                generateCard(
                    id="card-summarize-king",
                    text="I have a dream",
                    btn_text="Summarize Text",
                    citation="Martin Luther King, Jr",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Martin_Luther_King%2C_Jr..jpg/160px-Martin_Luther_King%2C_Jr..jpg",
                ),
                span=4,
            ),
            dmc.Col(
                generateCard(
                    id="card-summarize-shakespeare",
                    text="To be, or not to be, that is the question",
                    btn_text="Summarize Text",
                    citation="William Shakespeare",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/1280px-Shakespeare.jpg",
                ),
                span=4,
            ),
            dmc.Col(
                generateCard(
                    id="card-summarize-sagan",
                    text="Pale Blue Dot",
                    btn_text="Summarize Text",
                    citation="Carl Edward Sagan",
                    image_url="https://upload.wikimedia.org/wikipedia/commons/8/8d/Carl_Sagan_Planetary_Society_cropped.png",
                ),
                span=4,
            ),
        ],
        gutter="xl",
    )
