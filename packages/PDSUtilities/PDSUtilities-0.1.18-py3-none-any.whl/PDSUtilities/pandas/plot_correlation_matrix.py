# Copyright 2022 by Contributors

import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PDSUtilities.pandas import get_numerical_columns
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import get_marker
from PDSUtilities.plotly import update_layout
from PDSUtilities.plotly import apply_default
from PDSUtilities.plotly import get_font
from PDSUtilities.plotly import get_marker
from PDSUtilities.plotly import update_layout
from PDSUtilities.plotly import hex_to_rgb
from PDSUtilities.plotly import rgb_to_hex
from PDSUtilities.plotly import get_colors
from PDSUtilities.plotly import update_title
from PDSUtilities.plotly import update_width_and_height

def get_labels(columns, labels):
    if isinstance(labels, list):
        message = "Length of labels list must match length of columns list..."
        assert len(columns) == len(labels), message
        labels = { f"{columns[c]}": labels[c] for c in range(len(columns))}
    return labels

def get_correlation_label(correlations, columns, labels, row, col, precision, align = "middle"):
    BR = "<br />"
    col_label = labels.get(columns[col], columns[col])
    row_label = labels.get(columns[row], columns[row])
    cor_label = f"<b>{np.round(correlations.iloc[row, col], precision)}</b>"
    if align == "top":
        return "<span>" + cor_label + BR + col_label + BR + row_label + "</span>"
    if align == "bottom":
        return "<span>" + col_label + BR + row_label + BR + cor_label + "</span>"
    return "<span>" + col_label + BR + cor_label + BR + row_label + "</span>"

def get_color(value, colors):
    rlo, glo, blo = colors[1]
    rhi, ghi, bhi = colors[0]
    fraction = (value + 1.0)/2.001
    r = rlo + int(np.round(fraction*(rhi - rlo)))
    g = glo + int(np.round(fraction*(ghi - glo)))
    b = blo + int(np.round(fraction*(bhi - blo)))
    return rgb_to_hex((r, g, b))

def get_scatter_text(x, y, text, font = {}):
    # TODO: Need to test for more than just list...
    x = x if isinstance(x, list) else [x]
    y = y if isinstance(y, list) else [y]
    return go.Scatter(x = x, y = y, text = text, textfont = font,
        mode = 'text', showlegend = False, hoverinfo = "skip",
    )

# font
# axis_font
# hover_font
# label_font
# title_font
#
# tick_font
# legend_font
# subtitle_font
def plot_correlation_matrix(df, columns = None, labels = {},
    width = None, height = None, title = None, precision = 4,
    template = None, colors = 0, xangle = 45, yangle = 45,
    font = {}, axis_font = {}, hover_font = {}, label_font = {},
    title_font = {}):
    #
    #
    font = apply_default(get_font(), font)
    axis_font = apply_default(font, axis_font)
    label_font = apply_default(font, label_font)
    #
    colors = get_colors(colors)
    colors = [hex_to_rgb(color) for color in colors]
    columns = get_numerical_columns(df, columns)
    labels = get_labels(columns, labels)
    rows = [columns[c] for c in range(len(columns))]
    cols = [columns[c] for c in range(len(columns))]
    correlations = df[columns].corr()
    #
    fig = make_subplots(rows = len(rows), cols = len(cols),
        horizontal_spacing = 0.1/len(cols),
        vertical_spacing = 0.1/len(rows),
        shared_xaxes = True,
        shared_yaxes = True,
        # print_grid = True,
    )
    for r in range(len(rows)):
        for c in range(r):
            value = correlations[cols[c]][rows[r]]
            text = get_correlation_label(
                correlations, columns, labels, r, c, precision, "middle"
            )
            fig.append_trace(
                go.Scatter(
                    x = [0], y = [0],
                    mode = 'markers',
                    marker = dict(
                        symbol = "square",
                        size = 1000,
                        color = get_color(value, colors),
                    ),
                    hoverlabel = dict(font = hover_font),
                    hovertemplate = f"{rows[r]}<br>{cols[c]}",
                    name = str(np.round(value, precision)), #columns[row] + "/" + columns[col],
                    showlegend = False,
                ),
                r + 1, c + 1
            )
            # Used to center correlation text in
            # the plot as plotly annotations...
            fig.append_trace(
                get_scatter_text(0.0, 0.0, text, label_font),
                c + 1, r + 1
            )
    # Point axes in upper plots to the axes
    # in the corresponding lower plots...
    fig.update_xaxes(range = [-1.0, 1.0])
    fig.update_yaxes(range = [-1.0, 1.0])
    fig.update_xaxes(showgrid = False, ticks = "",  mirror = True)
    fig.update_yaxes(showgrid = False, ticks = "",  mirror = True)
    fig.update_xaxes(linecolor = "black", linewidth = 0.5, zeroline = False)
    fig.update_yaxes(linecolor = "black", linewidth = 0.5, zeroline = False)
    fig.update_xaxes(tickfont_size = 1, tickfont_color = "#FFFFFF")
    fig.update_yaxes(tickfont_size = 1, tickfont_color = "#FFFFFF")
    # We use a single tick label as the axis label...
    for c in range(len(cols)):
        fig.update_xaxes(
            tickmode = "array",
            tickvals = [0.0],
            tickfont = axis_font,
            ticktext = [labels.get(cols[c], cols[c])],
            tickangle = -xangle,
            row = len(rows), col = c + 1,
        )
    for r in range(len(rows)):
        fig.update_yaxes(
            tickmode = "array",
            tickvals = [0.2 if yangle == 45 else 0.0],
            tickfont = axis_font,
            ticktext = [
                labels.get(rows[r], rows[r]) + "  " if yangle == 45 else " "
            ],
            tickangle = -yangle,
            row = r + 1, col = 1,
        )
    #
    fig = update_width_and_height(fig, width, height)
    fig = update_title(fig, title, title_font, font)
    fig = update_layout(fig, font = font, template = template)
    return fig