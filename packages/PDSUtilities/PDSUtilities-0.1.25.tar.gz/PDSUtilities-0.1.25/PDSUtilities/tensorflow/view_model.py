import os
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import load_model

import plotly.graph_objects as go
import plotly.io as pio

from ipywidgets import widgets
from ipywidgets import interactive, HBox, VBox, Button

from PDSUtilities.ipywidgets import prev_dropdown_next
from PDSUtilities.plotly import create_image_subplots

from utilities import load_image

def scale_image(image):
# 	image = image.numpy()
# 	image = image[..., 0]
    numerator = np.max(image) - np.min(image)
    numerator = 1.0 if numerator < 0.001 else numerator
    image = 255*(image - np.min(image))/numerator
    image = image.astype(int)
    return np.stack([image, image, image], axis = -1)

def cast_image(image):
    image = tf.expand_dims(image, axis=-1)
    image = tf.cast(image, tf.float32)
    image = 2.0*image/255.0 - 1.0
    return image

def view_model(model, filenames, rows, cols, template):
    if isinstance(model, str):
        model = load_model(model)
    if template is None:
        template = pio.templates.default
    if template is None:
        template = go.layout.Template()

    def get_options(layer):
        layer = model.layers[layer]
        # assert len(layer.output.shape) == 4
        filters, rc = layer.output.shape[-1], rows*cols
        return [
            (f"Filters {f} to {min(f + rc, filters) - 1}", f//rc)
            for f in range(0, filters, rc)
        ]
    # For now just get first four...
    def get_filters(image, layer, filter):
        #image = os.path.join("./training/x", image)
        image = cast_image(load_image(image, True))
        layer = model.layers[layer]
        filters = tf.keras.Model(
            inputs = model.inputs,
            outputs = layer.output
        ).predict(np.asarray([image]))
        lo = filter*rows*cols
        hi = min(lo + rows*cols, layer.output.shape[-1])
        return [
            filters[0][..., f] for f in range(lo, hi)
        ] + [
            np.zeros_like(filters[0][..., 0]) for f in range(hi, lo + rows*cols)
        ]

    def on_figure(image, layer, filter):
        filters = get_filters(image, layer, filter)
        _, height, width = np.shape(filters)
        with fig.batch_update():
            for f, filter in enumerate(filters):
                fig.data[f].z = scale_image(filter)
        for row in range(rows):
            for col in range(cols):
                fig.update_xaxes(
                    row = row + 1, col = col + 1,
                    range = [0, width - 1],
                )
                fig.update_yaxes(
                    row = row + 1, col = col + 1,
                    range = [0, height - 1],
                )

    def on_image(change):
        image, _ = images.options[change['new']]
        layer, filter = layers.value, filters.value
        on_figure(image, layer, filter)
    prev_image, images, next_image = prev_dropdown_next(
        "Images", [
            (filename, f) for f, filename in enumerate(filenames)
        ], on_image
    )
    #
    def on_layer(change):
        filters.value = 0
        filters.options = get_options(change['new'])
        image, _ = images.options[images.value]
        on_figure(image, change['new'], 0)
    prev_layer, layers, next_layer = prev_dropdown_next(
        "Layers",
        [
            (f"{layer.name} {layer.output.shape}", l)
            for l, layer in enumerate(model.layers)
        ],
        on_layer
    )
    #
    def on_filter(change):
        image, _ = images.options[images.value]
        on_figure(image, layers.value, change['new'])
    prev_filter, filters, next_filter = prev_dropdown_next(
        "Filters", get_options(layers.value), on_filter
    )
    #
    def create_figure(image, layer, filter, rows, cols, template):
        filters = get_filters(image, layer, filter)
        filters = [scale_image(filter) for filter in filters]
        return create_image_subplots(filters, rows, cols, template = template)
    fig = go.FigureWidget(
        create_figure(
            images.options[images.value][0],
            layers.value, filters.value, rows, cols, template
        ),
        layout=go.Layout(title = "Title"),
    )

    return widgets.VBox([
        widgets.HBox([images, prev_image, next_image]),
        widgets.HBox([layers, prev_layer, next_layer]),
        widgets.HBox([filters, prev_filter, next_filter]),
        fig
    ])