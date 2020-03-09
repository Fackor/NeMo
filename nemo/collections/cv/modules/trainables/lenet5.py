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

from nemo.backends.pytorch.nm import TrainableNM
from nemo.core.neural_types import AxisKind, AxisType, LogprobsType, NeuralType, NormalizedValueType
from nemo.utils.decorators import add_port_docs

__all__ = ['LeNet5']


class LeNet5(TrainableNM):
    """Classical LeNet-5 model for MNIST image classification.
    """

    @property
    @add_port_docs()
    def input_ports(self):
        """ Returns definitions of module input ports. """
        return {
            "images": NeuralType(
                axes=(
                    AxisType(kind=AxisKind.Batch),
                    AxisType(kind=AxisKind.Channel, size=1),
                    AxisType(kind=AxisKind.Height, size=32),
                    AxisType(kind=AxisKind.Width, size=32),
                ),
                elements_type=NormalizedValueType(),
            )
        }

    @property
    @add_port_docs()
    def output_ports(self):
        """ Returns definitions of module output ports. """
        return {"predictions": NeuralType(axes=('B', 'D'), elements_type=LogprobsType())}

    def __init__(self):
        """
        Creates the LeNet-5 model.
        """
        super().__init__()

        # Create the LeNet-5 model.
        self.model = torch.nn.Sequential(
            torch.nn.Conv2d(1, 6, kernel_size=(5, 5)),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=(2, 2), stride=2),
            torch.nn.Conv2d(6, 16, kernel_size=(5, 5)),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=(2, 2), stride=2),
            torch.nn.Conv2d(16, 120, kernel_size=(5, 5)),
            torch.nn.ReLU(),
            # reshape to [-1, 120]
            torch.nn.Flatten(),
            torch.nn.Linear(120, 84),
            torch.nn.ReLU(),
            torch.nn.Linear(84, 10),
            torch.nn.LogSoftmax(dim=1),
        )
        self.to(self._device)

    def forward(self, images):
        """
        Performs the forward step of the model.

        Args:
            images: Batch of images to be classified.
        """

        predictions = self.model(images)
        return predictions
