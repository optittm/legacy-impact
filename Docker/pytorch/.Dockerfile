FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

WORKDIR /data
COPY requirement.txt requirement.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip


RUN pip install -r requirement.txt


EXPOSE 8888

ENTRYPOINT [ "jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token='pytorch'","--NotebookApp.password=''" ]
