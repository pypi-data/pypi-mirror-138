import plotly.graph_objects as go
import plotly.io as pio

# Template settings for plotly...
# https://plotly.com/python/templates/

layout_axis = dict(
    mirror=True,
    ticks="outside",
    showline=True,
    title_standoff=5,
    showgrid=True,
    zeroline=False,
)

pio.templates["DrJohnWagner"] = go.layout.Template(
    layout_xaxis=layout_axis,
    layout_yaxis=layout_axis,
    layout_title_font_size=18,
    layout_font_family="Verdana, Helvetica, Verdana, Calibri, Garamond, Cambria, Arial",
    layout_font_size=16,
)

pio.templates.default = "DrJohnWagner"

pio.templates["draft"] = go.layout.Template(
    layout_annotations=[
        dict(
            name="draft watermark",
            text="DRAFT",
            textangle=-30,
            opacity=0.1,
            font=dict(color="black", size=100),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
    ]
)
