from .base import *

DEBUG = True

ALLOWED_HOSTS = []

CHANNEL_LAYERS = {
    'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
}
