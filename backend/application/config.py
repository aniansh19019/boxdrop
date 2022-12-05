import os

class Config(object):
    # * API_KEYS and all can be accessed from here, don't hardcode though
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'