import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from PDSUtilities.plotly import get_rows_and_cols


def create_image_subplots(
    images, labels=None, rows=None, cols=None, width=None, height=None, template=None
):
    rows, cols = get_rows_and_cols(len(images), rows, cols)
    vertical_spacing = 0.01 if labels is None else 0.05
    labels = labels if labels is not None else []
    fig = make_subplots(
        rows=rows,
        cols=cols,
        shared_xaxes=False,
        shared_yaxes=False,
        vertical_spacing=vertical_spacing,
        horizontal_spacing=0.01,
        subplot_titles=labels,
    )
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            fig.add_trace(go.Image(z=images[index]), row=1 + row, col=1 + col)
    _, max_y, max_x, _ = np.shape(images)
    height = height if height is not None else 100 + 200 * rows
    width = width if width is not None else 200 * cols
    for row in range(rows):
        for col in range(cols):
            fig.update_xaxes(
                row=row + 1,
                col=col + 1,
                range=[0, max_x - 1],
                showgrid=False,
                ticks="",
                tickfont_size=1,
                tickfont_color="#FFFFFF",
                linecolor="black",
                linewidth=0.5,
                zeroline=False,
            )
            fig.update_yaxes(
                row=row + 1,
                col=col + 1,
                range=[0, max_y - 1],
                showgrid=False,
                ticks="",
                tickfont_size=1,
                tickfont_color="#FFFFFF",
                linecolor="black",
                linewidth=0.5,
                zeroline=False,
            )
    fig.update_layout(height=height, width=width)
    if template is not None:
        fig.update_layout(template=template)
    return fig
