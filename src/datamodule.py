# Copyright The PyTorch Lightning team.
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
from os import path

import torch
import torchvision.transforms as T
from pytorch_lightning import LightningDataModule
from pytorch_lightning.demos.mnist_datamodule import MNIST

DATASETS_PATH = path.join(path.dirname(__file__), "..", "data-versioning")


class MNISTDataModule(LightningDataModule):
    def __init__(self, batch_size=32):
        super().__init__()
        self.save_hyperparameters()

    @property
    def transform(self):
        return T.Compose([T.ToTensor(), T.Normalize((0.1307,), (0.3081,))])

    def prepare_data(self) -> None:
        MNIST(DATASETS_PATH, download=False)

    def train_dataloader(self):
        train_dataset = MNIST(
            DATASETS_PATH, train=True, download=False, transform=self.transform
        )
        return torch.utils.data.DataLoader(
            train_dataset, batch_size=self.hparams.batch_size
        )

    def val_dataloader(self):
        train_dataset = MNIST(
            DATASETS_PATH, train=False, download=False, transform=self.transform
        )
        return torch.utils.data.DataLoader(
            train_dataset, batch_size=self.hparams.batch_size
        )

    def test_dataloader(self):
        test_dataset = MNIST(
            DATASETS_PATH, train=False, download=False, transform=self.transform
        )
        return torch.utils.data.DataLoader(
            test_dataset, batch_size=self.hparams.batch_size
        )
