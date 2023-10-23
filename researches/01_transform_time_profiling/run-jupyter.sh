#!/bin/bash

python -m spacy download en_core_web_sm
python -m jupyter notebook --NotebookApp.token='aaa'