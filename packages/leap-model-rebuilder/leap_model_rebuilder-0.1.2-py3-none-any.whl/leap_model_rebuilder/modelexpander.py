import logging
from typing import List, Dict

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Layer, InputLayer, Input
from tensorflow.python.keras.engine.node import Node, KerasHistory

from leap_model_rebuilder.utils import is_custom_layer

_logger = logging.getLogger(__name__)

"""The ModelExpander class expands custom layers inside keras models.
    The Expand process is using the call method of custom layers to expand to the logic inside them.
"""


def expand_model(model: Model, layer_replacement_dict: Dict[str, Layer]) -> Model:
    """
    Expanding model's custom layers

    :return: Expanded model
    :rtype: tensorflow.keras.Model
    """

    layer_cache: Dict[str, Layer] = {}
    tensor_cache: Dict[int, tf.Tensor] = {}
    model_input_tensors: List[tf.Tensor] = []
    output_tensors: List[tf.Tensor] = []
    for out_tensor in model.outputs:
        expanded_tensor = _expand_tensor(
            out_tensor, tensor_cache, layer_cache, model_input_tensors, layer_replacement_dict)
        output_tensors.append(expanded_tensor)
    converted_model = tf.keras.Model(inputs=model_input_tensors, outputs=output_tensors)
    return converted_model


def _expand_tensor(tensor: tf.Tensor, tensor_cache: Dict[int, tf.Tensor], layer_cache: Dict[str, Layer],
                   model_input_tensors: List[tf.Tensor], layer_replacement_dict: Dict[str, Layer]) -> tf.Tensor:
    tensor_id = id(tensor)
    expanded_tensor = tensor_cache.get(tensor_id)
    if expanded_tensor is not None:
        return expanded_tensor

    current_node = _get_node_from_tensor(tensor)
    current_layer = _get_layer_from_tensor(tensor)

    # Creating first model input layer
    if isinstance(current_layer, InputLayer):
        input_tensor = _create_input_tensor(tensor)
        tensor_cache[tensor_id] = input_tensor
        model_input_tensors.append(input_tensor)
        return input_tensor

    # get all input tensors
    node_input_tensors = []
    parent_nodes = current_node.parent_nodes
    for parent_node in parent_nodes:
        output_tensor = parent_node.outputs
        node_input_tensor = _expand_tensor(
            output_tensor, tensor_cache, layer_cache, model_input_tensors, layer_replacement_dict)
        node_input_tensors.append(node_input_tensor)

    # squeeze node_input_tensors
    if len(node_input_tensors) == 1:
        node_input_tensors = node_input_tensors[0]

    if is_custom_layer(current_layer):
        expanded_tensor = current_layer.call(node_input_tensors)
    elif current_layer.name in layer_replacement_dict:
        expanded_tensor = layer_replacement_dict[current_layer.name](node_input_tensors)
    else:
        expanded_tensor = current_layer(node_input_tensors)

    tensor_cache[tensor_id] = expanded_tensor
    return expanded_tensor


def _get_layer_from_tensor(tensor: tf.Tensor) -> Layer:
    history = _get_keras_history(tensor)
    layer = history.layer
    return layer


def _get_keras_history(tensor: tf.Tensor) -> KerasHistory:
    # pylint: disable=protected-access
    return tensor._keras_history


def _get_node_from_tensor(tensor: tf.Tensor) -> Node:
    history = _get_keras_history(tensor)
    layer = history.layer
    node_index = history.node_index
    node = layer.inbound_nodes[node_index]
    return node


def _create_input_tensor(input_tensor: tf.Tensor) -> tf.Tensor:
    history = _get_keras_history(input_tensor)
    input_layer = history.layer
    inp_config = input_layer.get_config()
    new_input_tensor = Input(**inp_config)
    _logger.debug(f"Input created, name: {new_input_tensor.name}, shape: {new_input_tensor.shape}")
    return new_input_tensor
