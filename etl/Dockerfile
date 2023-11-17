FROM python:3.11

ARG APPHOMEDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APPHOMEDIR

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -d $APPHOMEDIR

COPY requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir --requirement requirements.txt

COPY ./src .

USER $USERNAME

ENTRYPOINT ["python", "main.py"]
