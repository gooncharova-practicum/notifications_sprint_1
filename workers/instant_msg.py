from sender import sender

from config import settings

sender.queue_bind(settings.instant_queue, settings.exchange, settings.instant_key)
