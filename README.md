# Aim 

## Prerequisite

- Anaconda3


## Setup

Create conda env

```
$ make env
```

Activate conda env

```
$ source init.sh
```

Install `requirements.txt` and `requirementx-pip.txt`

```
$ make setup
```

## Aim UI

Run aim server

```
$ make aim 

┌------------------------------------------------------------------------┐
                Aim UI collects anonymous usage analytics.
                        Read how to opt-out here:
    https://aimstack.readthedocs.io/en/latest/community/telemetry.html
└------------------------------------------------------------------------┘
Running Aim UI on repo `<Repo#5787586767819238508 path=/Users/wontakryu/annotation-ai/toy-code/aim/.aim read_only=None>`
Open http://127.0.0.1:43800

```

click `http://localhost:43800'

## Train MNIST model

Run train with 10 epochs and 0.1 limit batches.

```
$ make semi-train

python src/main.py fit --config configs/small_train.yaml  --trainer.limit_train_batches 0.1 --trainer.limit_val_batches 0.1
```

## Reference

[1] [lightning mnist example](https://github.com/Lightning-AI/lightning/blob/master/examples/convert_from_pt_to_pl/image_classifier_5_lightning_datamodule.py)

[2] [lightning AimLogger](https://github.com/aimhubio/aim/blob/main/examples/pytorch_lightning_track.p://github.com/aimhubio/aim/blob/main/examples/pytorch_lightning_track.py)
