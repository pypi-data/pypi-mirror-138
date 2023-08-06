###############################################################################
# Copyright (C) 2021-2022 Habana Labs, Ltd. an Intel Company
###############################################################################

import tensorflow as tf
from tensorflow.python.framework import ops

from habana_frameworks.tensorflow import habana_ops


def habana_gelu(features, approximate=False, name=None):
    """
    Has the same behaviour as
    https://www.tensorflow.org/api_docs/python/tf/nn/gelu

    HabanaGelu op is used, so it works only on Habana Gaudi.
    """
    with ops.name_scope(name, "Gelu", [features]):
        features = ops.convert_to_tensor(features, name="features")
        output, _ = habana_ops.habana_gelu(data_input=features, approximate=approximate)
        return output
