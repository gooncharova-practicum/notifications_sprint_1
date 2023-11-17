FROM rabbitmq:3

RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://github.com/rabbitmq/rabbitmq-delayed-message-exchange/releases/download/v3.12.0/rabbitmq_delayed_message_exchange-3.12.0.ez \
    -O /opt/rabbitmq/plugins/rabbitmq_delayed_message_exchange-3.12.0.ez

RUN rabbitmq-plugins enable --offline rabbitmq_management \
    rabbitmq_tracing rabbitmq_delayed_message_exchange \
    rabbitmq_web_dispatch rabbitmq_management_agent
