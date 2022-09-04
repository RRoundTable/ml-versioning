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
    def __init__(self, model, lr=1.0, gamma=0.7, batch_size=32):
        super().__init__()
        self.save_hyperparameters(ignore="model")
        self.model = model or Net()

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
    def validation_epoch_end(self, outputs) -> None:
        weight_hist = {}
        for name, param in self.model.named_parameters():
            weight_hist[name] = Distribution(param)
        self.logger.log_metrics(weight_hist)

    def on_train_end(self) -> None:
        from mlem.api import save
        import glob
        checkpoint_dir = os.path.join(self.logger.save_dir, self.logger.name or "None", self.logger.version, "*.ckpt")
        checkpoints = glob.glob(checkpoint_dir)
        save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".mlem/model")
        for checkpoint in checkpoints:
            _, filename = os.path.split(checkpoint)
            savepath = os.path.join(save_dir, filename)
            model = self.load_from_checkpoint(checkpoint)
            save(model, savepath)
