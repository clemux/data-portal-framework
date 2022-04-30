FROM python:3.9-slim-bullseye

RUN apt update && apt upgrade -y

# RUN useradd -ms /bin/bash elections
# USER elections
# this container should be run with rootless podman and SElinux enabled
WORKDIR /root

COPY dpf/ dpf/
COPY website/ website/
COPY pyproject.toml .
COPY pdm.lock .

RUN pip install --user pdm
RUN .local/bin/pdm install

ENTRYPOINT [".local/bin/pdm", "run"]

