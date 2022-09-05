# ML Versioning with DVC

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


## Versioning with DVC

Initialize dvc.

```
$ dvc init


Initialized DVC repository.

You can now commit the changes to git.

+---------------------------------------------------------------------+
|                                                                     |
|        DVC has enabled anonymous aggregate usage analytics.         |
|     Read the analytics documentation (and how to opt-out) here:     |
|             <https://dvc.org/doc/user-guide/analytics>              |
|                                                                     |
+---------------------------------------------------------------------+

What's next?
------------
- Check out the documentation: <https://dvc.org/doc>
- Get help and share ideas: <https://dvc.org/chat>
- Star us on GitHub: <https://github.com/iterative/dvc>

```

A few files are created.
```
$ tree .dvc

.dvc
├── config
└── tmp
    ├── hashes
    │   └── local
    │       └── cache.db
    └── links
        └── cache.db
```

Add remote(e.g. localstorage)

```
$ dvc remote add localstorage -d ~/remote/localstorage

Setting 'localstroage' as a default remote.
```

Check remote list

```
$ dvc remote list

localstorage   ~/remote/localstorage
```

Add `.dvc/config` on git

```
$ git add .dvc/config
```


## Download data and train model

Run train with 10 epochs and 0.1 limit batches.

```
$ make train

python src/main.py fit --config configs/small_train.yaml  --trainer.limit_train_batches 0.1 --trainer.limit_val_batches 0.1
```

Check data and checkpoint.

```
$ tree Datasets

Datasets
└── MNIST
    └── raw
        ├── t10k-images-idx3-ubyte
        ├── t10k-images-idx3-ubyte.gz
        ├── t10k-labels-idx1-ubyte
        ├── t10k-labels-idx1-ubyte.gz
        ├── train-images-idx3-ubyte
        ├── train-images-idx3-ubyte.gz
        ├── train-labels-idx1-ubyte
        └── train-labels-idx1-ubyte.gz
```

```
$ tree lightning_logs

version_2
    ├── checkpoints
    │   └── epoch=9-test_loss=0.0653.ckpt
    ├── config.yaml
    ├── events.out.tfevents.1662336863.wontakui-MacBookPro.local.95538.0
    └── hparams.yamlsss
```

## Add dataset on DVC


Add datasets

```
$ dvc add Datasets/

100% Adding...|██████████████████████████████████████████████████████████████████████████████|1/1 [00:00,  5.46file/s]

$ dvc data status

DVC committed changes:
  (git commit the corresponding dvc files to update the repo)
        added: Datasets/
(there are other changes not tracked by dvc, use "git status" to see)

```

Commit

```
$ git add Datasets.dvc
$ git commit -m "Add v1 mnist  data"

$ dvc data status

No changes.
(there are changes not tracked by dvc, use "git status" to see)
```


`dvc add` moves the data to the project's cache, and links it to the workspace.

```
$ tree .dvc/cache

.dvc/cache
├── 26
│   └── 46ac647ad5339dbf082846283269ea
├── 27
│   └── ae3e4e09519cfbb04c329615203637
├── 6b
│   └── bc9ace898e44ae57da46a324031adb
├── 9f
│   └── b629c4189551a2d022fa330f9573f3
├── a2
│   └── 5bea736e30d166cdddb491f175f624
├── ab
│   └── 3353d41bd7a24a20a31f29b64e3b3c.dir
├── d5
│   └── 3e105ee54ea40749a09fcbcd1e9432
├── ec
│   └── 29112dd5afa0611ce80d1b7f02629c
└── f6
    └── 8b3c2dcbeaaa9fbdd348bbdeb94873

9 directories, 9 files
```

`Datasets.dvc` indicates the cache file path.

```
$ cat Datasets.dvc

outs:
- md5: ab3353d41bd7a24a20a31f29b64e3b3c.dir # .dvc/ab/3353d41bd7a24a20a31f29b64e3b3c.dir
  size: 66544770
  nfiles: 8
  path: Datasets
```

Push data to data remote

```
$ dvc push -r localstorage

$ tree ~/remote/localstorage

/Users/wontakryu/remote/data
├── 26
│   └── 46ac647ad5339dbf082846283269ea
├── 27
│   └── ae3e4e09519cfbb04c329615203637
├── 6b
│   └── bc9ace898e44ae57da46a324031adb
├── 9f
│   └── b629c4189551a2d022fa330f9573f3
├── a2
│   └── 5bea736e30d166cdddb491f175f624
├── ab
│   └── 3353d41bd7a24a20a31f29b64e3b3c.dir
├── d5
│   └── 3e105ee54ea40749a09fcbcd1e9432
├── ec
│   └── 29112dd5afa0611ce80d1b7f02629c
└── f6
    └── 8b3c2dcbeaaa9fbdd348bbdeb94873
```

Remove data and Retrive data

```
$ rm -r .dvc/cache Datasets/

```

Check files are removed.

```
$ tree Datasets
$ tree .dvc/cache
```

Pull data from `localstorage` remote
```
$ dvc pull -r localstorage
```

Check files are restored.

```
$ tree Datasets
$ tree .dvc/cache
```

## Model versioning with DVC


Add model to dvc and git

Move model to model directory `checkpoints`

```
$ mkdir -p checkpoints
$ mv lightning_logs/version_2/checkpoints/epoch=9-test_loss=0.0653.ckpt checkpoints/model.ckpt

```

```
$ dvc add checkpoints
```

```
$ git add checkpoints.dvc
$ git commit -m "Save model"
```

Push

```
$ dvc push -r localstorage
```


## Make a new model and commit on git

Run new train and generage new checkpoints.

```
$ make train
```

Move model to `checkpoints/model.ckpt`

```
$ mv lightning_logs/version_3/checkpoints/epoch=9-test_loss=0.0626.ckpt checkpoints/model.ckpt
```

Add to dvc and commit

```
$ dvc add checkpoints
$ git add checkpoints.dvc
$ git commit -m "save model v2"
```


## Reference

[1] [lightning mnist example](https://github.com/Lightning-AI/lightning/blob/master/examples/convert_from_pt_to_pl/image_classifier_5_lightning_datamodule.py)

[2] [Get Started: Data Versioning](https://dvc.org/doc/start/data-management)

[3] [AimLogger](https://aimstack.readthedocs.io/en/v3.0.4/guides/integrations/basic_aim_pytorch_lightning.html)
