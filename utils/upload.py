from dash import dcc, html


def filePicker(id, accept):
    return dcc.Upload(
        id=id,
        accept=accept,
        children=html.Div(["Drag and Drop or Select File"]),
        style={
            "width": "100%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
            "cursor": "pointer",
        },
        # Allow multiple files to be uploaded
        multiple=False,
    )
