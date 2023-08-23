#!/bin/bash

source  ~/legacy-impact/jupyterenv/bin/activate
python -m pip install -r ~/legacy-impact/requirements.txt
python -m spacy download en_core_web_sm
python -m jupyter notebook --NotebookApp.token='aaa'