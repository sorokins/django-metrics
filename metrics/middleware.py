class UTMMiddleware(object):
    def process_request(self, request):
        utm = request.session.get("utm", {})
        if "utm_referer" in request.REQUEST or request.META.has_key('HTTP_REFERER'):
            referrer = request.REQUEST.get('utm_referer', request.META['HTTP_REFERER'])
            utm['referrer'] = referrer[:2048]

        if "utm_source" in request.REQUEST:
            utm['source'] = request.REQUEST['utm_source'][:100]
            utm['referrer'] = None

        if "utm_medium" in request.REQUEST:
            utm['medium'] = request.REQUEST['utm_medium'][:50]

        if "utm_campaign" in request.REQUEST:
            utm['campaign'] = request.REQUEST['utm_campaign'][:100]

        if "gclid" in request.REQUEST:
            utm['gclid'] = request.REQUEST['gclid']

        if "dclid" in request.REQUEST:
            utm['dclid'] = request.REQUEST['dclid']

        request.session['utm'] = utm
