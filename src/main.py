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

from pytorch_lightning import Trainer, cli_lightning_logo
from pytorch_lightning.cli import LightningCLI

from datamodule import MNISTDataModule
from model import ImageClassifier


# The LightningCLI removes all the boilerplate associated with arguments parsing. This is purely optional.
cli = LightningCLI(
    ImageClassifier,
    MNISTDataModule,
    save_config_overwrite=True,
)
