import json

from django import template
from django.conf import settings


register = template.Library()


@register.inclusion_tag('metrics/metrics.html')
def metrics_js():
    return {
        'DEBUG': settings.DEBUG,
        'metrika_id': settings.METRICS['metrika']['id'],
        'METRICS_EXCLUDE_USER_DOMAIN': settings.METRICS_EXCLUDE_USER_DOMAIN,
        'adwords_conversions': json.dumps(settings.METRICS['adwords_conversion'])
    }


@register.inclusion_tag('metrics/metrika_counter.html')
def metrika_counter():
    return {
        'id': settings.METRICS['metrika']['id']
    }


@register.inclusion_tag('metrics/mixpanel_counter.html')
def mixpanel_counter():
    return {
        'id': settings.METRICS['mixpanel']['id']
    }


@register.inclusion_tag('metrics/ga_counter.html')
def ga_counter():
    return {
        'id': settings.METRICS['ga']['id']
    }
