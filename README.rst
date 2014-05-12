=====
Django-metrics
=====

Application helps to track everything with Google Analytics, Google Adwords, Yandex.Metrika, Mixpanel

Installation
----
1. Install package from github::

    pip install -e git+https://github.com/sorokins/django-metrics.git#egg=django-metrics==0.1.5


2. Add 'metrics' to INSTALLED_APPS in settings.py

3. Add counter settings to settings.py::

    METRICS = {
        'ga': {
            'id': 'UA-1234567-1'
        },
        'adwords_conversion': {
            'id': 1234567,
            'demo': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'OKfPCKnOkggQ_5Pr2wM',
                'google_conversion_value': 25,
                'google_remarketing_only': False
            },
            'application': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'EzGBCOn-mggQ_5Pr2wM',
                'google_conversion_value': 25,
                'google_remarketing_only': False
            },
            'email_confirmation': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'n3-9CPHUkggQ_5Pr2wM',
                'google_conversion_value': 75,
                'google_remarketing_only': False
            },
            'docs_uploaded': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'LzRICPnTkggQ_5Pr2wM',
                'google_conversion_value': 150,
                'google_remarketing_only': False
            },
            'application_approved': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'Ig8fCInSkggQ_5Pr2wM',
                'google_conversion_value': 750,
                'google_remarketing_only': False
            },
            'deposit': {
                'google_conversion_language': 'en',
                'google_conversion_color': 'ffffff',
                'google_conversion_label': 'hu49COnVkggQ_5Pr2wM',
                'google_conversion_value': 1500,
                'google_remarketing_only': False
            },
        },

        'metrika': {
            'id': 1234567
        },
        'mixpanel': {
            'id': '0cc175b9c0f1b6a831c399e269772661'
        }
    }

    METRICS_EXCLUDE_USER_DOMAIN = 'example.com'


4. Insert js-script into page::

    {% load metrics %}
    {% metrics_js %}


5. Insert js-codes for counters::

    {% load metrics %}
    {% metrika_counter %}
    {% mixpanel_counter %}
    {% ga_counter %}


How to use
------
1. Track event in Mixpanel, GA, Yandex.Metrika in client-side::

    Metrics.track_event(category, action, user, value, data)

    // For example:
    Metrics.track_event('acquisition', 'Application_finished', 'email@example.com', 50, {demo: true});


2. Track adwords conversions in js::

    Metrics.adwords_conversion(name)  // name of conversion from settings.py


3. Track server-side events (GA and Mixpanel) with celery::

    track_event.delay(event_category, event_action, distinct_id=None, event_label='', event_value='', properties={}, utm=None)

, where utm is::

    utm = {
        "referrer": '...',
        "source": '...',
        "campaign": '...',
        "medium": '...',
        "gclid": '...',
        "dclid": '...',
    }

4. Server-side utils for mixpanel::

    mixpanel_alias.delay(new_id, old_id)
    mixpanel_people_set.delay(distinct_id, event_name, value=None, increment=False)
    mixpanel_track_charge.delay(distinct_id, amount)


Also, package contains middleware.UTMMiddleware which saves utm_* data from request or cookies in session.