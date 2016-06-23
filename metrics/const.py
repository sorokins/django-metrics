from metrics import __version__

USER_AGENT = 'django-metrics/{}'.\
    format('.'.join(map(str, __version__)))
