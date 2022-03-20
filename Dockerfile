from nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu20.04 as base

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-dev && \
    apt clean && \
    rm -rf /var/lib/apt && \
    rm -rf /var/lib/dpkg/info/*

RUN mkdir /app
COPY requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt
RUN python3 -c 'import nltk;nltk.download("punkt")'

CMD ["./run_ner.py", "--help"]
