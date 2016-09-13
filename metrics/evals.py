# encoding: utf-8

from __future__ import unicode_literals
try:
    from html import escape
except ImportError:
    from cgi import escape

from django.utils.safestring import mark_safe


class ValueEval(object):
    def __init__(self, value, skip=None):
        self.value = self.clean_value(value)
        self.skip = skip

    def is_should_skip(self, request):
        return False if self.skip is None else self.skip(request)

    def clean_value(self, value):
        return value

    def _render_value(self, value):
        return mark_safe('"{}"'.format(escape(value)))

    def render(self, request):
        return self._render_value(self.value)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.value)
    __str__ = __repr__
    __unicode__ = __repr__


class RequestEval(ValueEval):
    def clean_value(self, value):
        assert callable(value)
        return value

    def render(self, request):
        return self._render_value(self.value(request))


class JSEval(RequestEval):
    def render(self, request):
        return mark_safe(self.value(request))
