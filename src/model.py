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
import os
from os import path

import torch
from pytorch_lightning import LightningModule
from pytorch_lightning.demos.boring_classes import Net
from torch.nn import functional as F
from aim import Distribution


class ImageClassifier(LightningModule):
    def __init__(self, lr=1.0, gamma=0.7, batch_size=32):
        super().__init__()
        self.save_hyperparameters(ignore="model")
        self.model = Net()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self.forward(x)
        loss = F.nll_loss(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self.forward(x)
        loss = F.nll_loss(logits, y)
        self.log("test_loss", loss)

    def configure_optimizers(self):
        optimizer = torch.optim.Adadelta(self.model.parameters(), lr=self.hparams.lr)
        return [optimizer], [
            torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=1, gamma=self.hparams.gamma
            )
        ]
