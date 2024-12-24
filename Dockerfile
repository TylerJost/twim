FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-runtime
RUN apt-get update
RUN apt-get install -y git
RUN pip install -U --no-cache-dir \
pandas \
tqdm \
matplotlib \
spotipy \
datasets \
numpy \
beautifulsoup4 \
transformers \
ipykernel
