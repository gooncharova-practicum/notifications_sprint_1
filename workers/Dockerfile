FROM python:3.11

ARG APPHOMEDIR
ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG STATICROOT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APPHOMEDIR

RUN apt-get update && apt-get install -y \
    gettext \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -d $APPHOMEDIR

RUN mkdir -p $STATICROOT \
    && chown -R $USER_UID:$USER_GID $STATICROOT

COPY requirements.txt .

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir --requirement requirements.txt

COPY ./ .

EXPOSE 8000

USER $USERNAME
