import plotly.graph_objects as go
from ipywidgets import HBox


def plot_history(history, height=400, width=500):
    if history.history is not None:
        history = history.history
    epochs = list(range(len(history["accuracy"])))

    figL = go.FigureWidget(
        [
            go.Scatter(x=epochs, y=history["accuracy"], name="Training"),
            go.Scatter(x=epochs, y=history["val_accuracy"], name="Validation"),
        ]
    )
    figR = go.FigureWidget(
        [
            go.Scatter(x=epochs, y=history["loss"], name="Training"),
            go.Scatter(x=epochs, y=history["val_loss"], name="Validation"),
        ]
    )

    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    figL.update_layout(height=400, width=500, legend=legend)
    figL.update_xaxes(title_text="Epoch")
    figL.update_yaxes(title_text="Accuracy")
    figR.update_layout(height=height, width=width, legend=legend)
    figR.update_xaxes(title_text="Epoch")
    figR.update_yaxes(title_text="Loss")

    return HBox([figL, figR])
