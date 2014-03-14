import logging
import uuid
from celery.task import task
from datetime import datetime
from django.conf import settings
from mixpanel import Mixpanel
import requests


logger = logging.getLogger(__name__)


domain_exclude = u'@' + settings.METRICS_EXCLUDE_USER_DOMAIN

@task(name='metrics.mixpanel_alias')
def mixpanel_alias(new_id, old_id):
    if not settings.DEBUG and new_id.endswith(domain_exclude):
        return
    else:
        mp = Mixpanel(settings.METRICS['mixpanel']['id'])
        mp.alias(new_id, old_id)


@task(name='metrics.mixpanel_track')
def mixpanel_track(distinct_id, event_name, properties={}):
    if not distinct_id:
        return
    if not settings.DEBUG and distinct_id.endswith(domain_exclude):
        return

    mp = Mixpanel(settings.METRICS['mixpanel']['id'])
    mp.track(distinct_id, event_name, properties)


@task(name='metrics.mixpanel_people_set')
def mixpanel_people_set(distinct_id, event_name, value=None, increment=False):
    """
    If value not set value = datetime
    """
    if not distinct_id:
        return
    if not settings.DEBUG and distinct_id.endswith(domain_exclude):
        return

    mp = Mixpanel(settings.METRICS['mixpanel']['id'])
    if increment:
        mp.people_increment(distinct_id, {event_name: value})
    else:
        if value is None:
            value = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        mp.people_set(distinct_id, {event_name: value})


@task(name='metrics.mixpanel_track_charge')
def mixpanel_track_charge(distinct_id, amount):
    if not settings.DEBUG and distinct_id.endswith(domain_exclude):
        return

    mp = Mixpanel(settings.METRICS['mixpanel']['id'])
    mp.people_track_charge(distinct_id, amount, {
        '$time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    })


@task(name="ga.track_event")
def ga_track(event_category, event_action, distinct_id=None, event_label='', event_value='', utm=None):
    if not distinct_id:
        distinct_id = uuid.uuid4()

    data = {
        'v': 1,
        'tid': settings.METRICS['ga']['id'],
        'cid': distinct_id,
        't': 'event',
        'ec': event_category,
        'ea': event_action,
    }
    if utm:
        data.update({
            "dr": utm.get("referrer"),
            "cs": utm.get("source"),
            "cn": utm.get("campaign"),
            "cm": utm.get("medium"),
            "gclid": utm.get("gclid"),
            "dclid": utm.get("dclid"),
        })


    if event_label:
        data.update({
            'el': event_label
        })
    if event_value:
        data.update({
            'ev': event_value
        })

    logger.info(u'GA data: %s' % data)
    requests.post('http://www.google-analytics.com/collect', data)


@task(name='metrics.track_event')
def track_event(event_category, event_action, distinct_id=None, event_label='', event_value='', properties={}, utm=None):
    ga_track.delay(event_category, event_action, distinct_id, event_label, event_value, utm=utm)
    mixpanel_track.delay(distinct_id, event_action, properties)