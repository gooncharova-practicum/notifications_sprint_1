from sender import sender

from config import settings

sender.queue_bind(settings.scheduled_queue, settings.exchange, settings.scheduled_key)
