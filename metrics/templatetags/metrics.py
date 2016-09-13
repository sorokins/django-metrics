from __future__ import absolute_import

import json

from django import template
from django.conf import settings

from metrics.evals import ValueEval


register = template.Library()


def _conv_set_params(request, set_params=None):
    if not set_params:
        set_params = getattr(settings, 'METRICS_SET_PARAMS', None)

    assert set_params is None or \
           isinstance(set_params, dict)

    if not set_params:
        return

    result = {
        key: value.render(request)
        for key, value in set_params.items()
        if not value.is_should_skip(request)
    }

    return result


@register.inclusion_tag('metrics/metrics.html')
def metrics_js():
    return {
        'DEBUG': settings.DEBUG,
        'metrika_id': settings.METRICS['metrika']['id'],
        'METRICS_EXCLUDE_USER_DOMAIN': settings.METRICS_EXCLUDE_USER_DOMAIN,
        'adwords_conversions': json.dumps(settings.METRICS['adwords_conversion']),
    }


@register.inclusion_tag('metrics/metrika_counter.html')
def metrika_counter():
    return {
        'id': settings.METRICS['metrika']['id'],
    }


@register.inclusion_tag('metrics/mixpanel_counter.html')
def mixpanel_counter():
    return {
        'id': settings.METRICS['mixpanel']['id'],
    }


@register.inclusion_tag('metrics/ga_counter.html', takes_context=True)
def ga_counter(context, ga_id=None, **set_params):
    request = context.get('request')
    return {
        'id': ga_id or settings.METRICS['ga']['id'],
        'set_params': _conv_set_params(request, set_params),
    }
