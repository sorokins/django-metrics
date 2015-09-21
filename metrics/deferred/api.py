KEY = '_metrics_storage'


def _has_storage(request):
    return hasattr(request, KEY)


def _get_storage_class():
    # TODO: should depend on settings
    from .storage import SessionStorage
    return SessionStorage


def get_events_storage(request):
    if not _has_storage(request):
        setattr(request, KEY, _get_storage_class()(request))
    return getattr(request, KEY)


def add_deferred_event(request, **kwargs):
    get_events_storage(request).add(**kwargs)
