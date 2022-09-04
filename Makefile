PYTHON=3.8
BASENAME=$(shell basename $(CURDIR))
CONDA_CH=pytorch defaults conda-forge

env:
	conda create -n $(BASENAME)  python=$(PYTHON)

setup:
	conda install --file requirements.txt $(addprefix -c ,$(CONDA_CH))
	pip install -r requirements-pip.txt

train:
	echo "Run train with 10 epochs and 0.1 limit batches to check mlflow client quickly. "
	python src/main.py fit --config configs/small_train.yaml  --trainer.limit_train_batches 0.1 --trainer.limit_val_batches 0.1

aim:
	aim up
