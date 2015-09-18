try:
    from ipware.ip import get_real_ip
except ImportError:
    get_real_ip = lambda *args, **kwargs: None


class UTMMiddleware(object):
    def process_request(self, request):
        utm = request.session.get('utm', {})
        
        if 'utm_referer' in request.REQUEST or 'utm_referer' in request.COOKIES or request.META.has_key('HTTP_REFERER'):
            referrer = request.REQUEST.get('utm_referer') or request.REQUEST.get('utm_referer') or request.META['HTTP_REFERER']
            if referrer:
                utm['referrer'] = referrer[:2048]

        if 'utm_source' in request.REQUEST or 'utm_source' in request.COOKIES:
            utm['source'] = request.REQUEST.get('utm_source') or request.COOKIES.get('utm_source')
            if utm['source']:
                utm['source'] = utm['source'][:100]
            utm['referrer'] = None

        if 'utm_medium' in request.REQUEST or 'utm_medium' in request.COOKIES:
            utm['medium'] = request.REQUEST.get('utm_medium') or request.COOKIES.get('utm_medium')
            if utm['medium']:
                utm['medium'] = utm['medium'][:50]

        if 'utm_campaign' in request.REQUEST or 'utm_campaign' in request.COOKIES:
            utm['campaign'] = request.REQUEST.get('utm_campaign') or request.COOKIES.get('utm_campaign')
            if utm['campaign']:
                utm['campaign'] = utm['campaign'][:100]

        if 'gclid' in request.REQUEST or 'gclid' in request.COOKIES:
            utm['gclid'] = request.REQUEST.get('gclid') or request.COOKIES.get('utm_gclid')
            if utm['gclid']:
                utm['gclid'] = utm['gclid'][:100]

        if 'dclid' in request.REQUEST or 'dclid' in request.COOKIES:
            utm['dclid'] = request.REQUEST.get('dclid') or request.COOKIES.get('utm_dclid')
            if utm['dclid']:
                utm['dclid'] = utm['dclid'][:100]

        user_ip = get_real_ip(request, right_most_proxy=True)
        if user_ip:
            utm['user_ip'] = user_ip

        request.session['utm'] = utm
