FROM nginx:1.23.3

ARG USERNAME
ARG USER_UID
ARG USER_GID
ARG STATICROOT_NGINX

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --no-create-home $USERNAME \
    && chown -R $USER_UID:$USER_GID $STATICROOT_NGINX
