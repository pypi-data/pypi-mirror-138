from typing import NamedTuple

from tensorflow.keras import Model
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Concatenate

class Concatenation(NamedTuple):
    layer_one: str
    layer_two: str
    axis: int
    name: str

# SequentialWithConcatenations([
#   Input((32, 32, 1)),
#   Conv2D(..., name="layer1"),
#   Conv2D(..., name="layer2"),
#   Conv2D(..., name="layer3"),
#   Concatenation("layer2", "layer3", 3, "layer4")
#   Conv2D(..., name="layer5"),
#   Concatenation("layer1", "layer5", 3, "layer6")
#   Conv2D(..., name="layer7"),
#   Conv2D(..., name="layer8"),
#   Dense(4, name="layer9")
# ], name="MyModel")
class SequentialWithConcatenations(Model):
    def __init__(layers, input=None, name=None):
        if input is None:
            input = layers.pop(0)
        output, lookup = input, dict()
        for index, layer in enumerate(layers):
            if isinstance(layer, Layer):
                output = layer(output)
                lookup[layer.name] = output
            else:
                assert isinstance(layer, Concatenation)
                layer_one, layer_two, axis, name = layer
                output = Concatenate(axis=axis, name=name)(
                    [lookup[layer_one], lookup[layer_two]]
                )
        super().__init__(input=input, output=output, name=name)