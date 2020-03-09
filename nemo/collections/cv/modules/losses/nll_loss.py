# =============================================================================
# Copyright (c) 2020 NVIDIA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import torch

from nemo.backends.pytorch.nm import DataLayerNM, LossNM, NonTrainableNM, TrainableNM
from nemo.core.neural_types import AxisKind, AxisType, LabelsType, LogprobsType, LossType, NeuralType
from nemo.utils.decorators import add_port_docs

__all__ = ['NLLLoss']


class NLLLoss(LossNM):
    """ Class representing a simple NLL loss. """

    def __init__(self, **kwargs):
        # Neural Module API specific
        LossNM.__init__(self, **kwargs)
        # End of Neural Module API specific
        self._criterion = torch.nn.NLLLoss()

    @property
    @add_port_docs()
    def input_ports(self):
        """ Returns definitions of module input ports. """
        return {
            "predictions": NeuralType(axes=('B', 'D'), elements_type=LogprobsType()),
            # "targets": NeuralType(axes=tuple(AxisType(AxisKind.Batch)), elements_type=LabelsType()),
            "targets": NeuralType(axes=tuple('B'), elements_type=LabelsType()),
        }

    @property
    @add_port_docs()
    def output_ports(self):
        """ Returns definitions of module output ports. """
        return {"loss": NeuralType(elements_type=LossType())}

    # You need to implement this function
    def _loss_function(self, **kwargs):
        return self._criterion(*(kwargs.values()))
