KEY = 'js_events'


def _has_events(request):
    return hasattr(request, KEY)


def _get_events(request):
    if not _has_events(request):
        setattr(request, KEY, [])
    events = getattr(request, KEY, None)
    return events


def track_js_event(request, *args, **kwargs):
    _get_events(request).append([
        args,
        kwargs,
    ])
