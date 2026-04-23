FROM debian:stretch

# As of 2023, Debian stretch updates have been moved to archive.debian.org
# The Docker registry doesn't have an up-to-date version so we monkeypatch our own.
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

# Libffi-dev is the bridge between compiled and interpreted languages. Here it's C and Python.
RUN apt-get -qq update && apt-get install -y python3 python3-pip python3-venv libffi-dev
RUN python3 -m venv /ctf/venv
RUN /ctf/venv/bin/pip install wheel
RUN /ctf/venv/bin/pip install cryptography flask
COPY main.py /ctf/main.py
COPY ctf.key /ctf/ctf.key
ENV CSAW_FLAG=NowyourereadytocrackthePS3YeahSonydidthiswithECDSA


WORKDIR /ctf
CMD ["/ctf/venv/bin/python", "main.py"]
