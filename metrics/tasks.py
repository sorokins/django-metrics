import uuid
import logging
from datetime import datetime

from django.conf import settings
from celery.task import task
from mixpanel import Mixpanel
from django.utils import six
import requests

from .const import USER_AGENT


logger = logging.getLogger(__name__)


domain_exclude = getattr(settings, 'METRICS_EXCLUDE_USER_DOMAIN', None)
if domain_exclude:
    domain_exclude = u'@' + domain_exclude


# https://developers.google.com/analytics/devguides/collection/protocol/v1/parameters
GA_UTM_CONVERSION = {
    'dr': 'referrer',
    'cs': 'source',
    'cn': 'campaign',
    'cm': 'medium',
    'gclid': 'gclid',
    'dclid': 'dclid',
    'uip': 'user_ip',
    'ua': 'user_agent',
}


@task(name='metrics.mixpanel_alias')
def mixpanel_alias(new_id, old_id):
    if not settings.DEBUG and domain_exclude and new_id.endswith(domain_exclude):
        return

    id = settings.METRICS.get('mixpanel', {}).get('id')
    if not id:
        logger.info('Mixpanel id not defined, task ignored')
        return
    mp = Mixpanel(id)
    mp.alias(new_id, old_id)


@task(name='metrics.mixpanel_track')
def mixpanel_track(distinct_id, event_name, properties=None,
                   utm=None, user_ip=None, user_agent=None, **kwargs):
    if not distinct_id:
        return
    if not settings.DEBUG and domain_exclude and distinct_id.endswith(domain_exclude):
        return

    id = settings.METRICS.get('mixpanel', {}).get('id')
    if not id:
        logger.info('Mixpanel id not defined, task ignored')
        return

    # if utm:
    #     properties.update({
    #         "utm_referrer": utm.get("referrer"),
    #         "utm_source": utm.get("source"),
    #         "utm_campaign": utm.get("campaign"),
    #         "utm_medium": utm.get("medium"),
    #     })

    mp = Mixpanel(id)
    mp.track(distinct_id, event_name, properties or {})


@task(name='metrics.mixpanel_people_set')
def mixpanel_people_set(distinct_id, event_name, value=None, increment=False):
    """
    If value not set value = datetime`
    """
    if not distinct_id:
        return
    if not settings.DEBUG and domain_exclude and distinct_id.endswith(domain_exclude):
        return

    id = settings.METRICS.get('mixpanel', {}).get('id')
    if not id:
        logger.info('Mixpanel id not defined, task ignored')
        return

    mp = Mixpanel(id)
    if increment:
        mp.people_increment(distinct_id, {event_name: value})
    else:
        if value is None:
            value = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        mp.people_set(distinct_id, {event_name: value})


@task(name='metrics.mixpanel_track_charge')
def mixpanel_track_charge(distinct_id, amount):
    if not settings.DEBUG and domain_exclude and distinct_id.endswith(domain_exclude):
        return
    id = settings.METRICS.get('mixpanel', {}).get('id')
    if not id:
        logger.info('Mixpanel id not defined, task ignored')
        return

    mp = Mixpanel(id)
    mp.people_track_charge(distinct_id, amount, {
        '$time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })


@task(name="ga.track_event")
def ga_track(event_category, event_action, distinct_id=None,
             event_label='', event_value='',
             utm=None, **kwargs):

    id = settings.METRICS.get('ga', {}).get('id')
    if not id:
        logger.info('GA id not defined, task ignored')
        return

    data = {
        'v': 1,
        'tid': id,
        'cid': distinct_id or uuid.uuid4(),
        't': 'event',
        'ec': event_category,
        'ea': event_action,
    }

    data.update(kwargs)

    utm = utm or {}
    for ga_key, utm_key in six.iteritems(GA_UTM_CONVERSION):
        if utm_key not in utm:
            continue
        data[ga_key] = utm[utm_key]

    if event_label:
        data.update({
            'el': event_label
        })
    if event_value:
        data.update({
            'ev': event_value
        })

    logger.info(u'GA data: %s' % data)
    requests.post('http://www.google-analytics.com/collect', data,
                  headers={'user-agent': USER_AGENT})


@task(name='metrics.track_event')
def track_event(event_category, event_action, distinct_id=None, event_label='', event_value='', properties=None, utm=None):
    ga_track.delay(event_category, event_action, distinct_id, event_label, event_value,
                   utm=utm)
    mixpanel_track.delay(distinct_id, event_action, properties,
                         utm=utm)
