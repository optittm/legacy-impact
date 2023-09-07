FROM tensorflow/tensorflow:2.14.0rc1-jupyter

WORKDIR /data

RUN apt-get update
RUN pip install --upgrade pip

EXPOSE 8888

ENTRYPOINT [ "jupyter", "lab", "--NotebookApp.allow_origin='*'", "--NotebookApp.ip='0.0.0.0'","--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token='tensorflow'","--NotebookApp.password=" ]