from django import template

from metrics.deferred.api import get_events_storage


register = template.Library()


@register.inclusion_tag('deferred/events.html', takes_context=True)
def deferred_events(context):
    events = []
    request = context.get('request', None)
    if request:
        storage = get_events_storage(request)
        events = list(storage)
        storage.clear()
    return {
        'events': events,
    }
