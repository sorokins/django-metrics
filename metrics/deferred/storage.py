from weakref import ref


class BaseStorage(object):
    def __init__(self, request):
        self.request = ref(request)

    def __iter__(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def add(self, **kwargs):
        raise NotImplementedError


class SessionStorage(BaseStorage):
    SESSION_KEY = 'deferred_events'

    def __init__(self, request):
        super(SessionStorage, self).__init__(request)
        assert self.request().session, \
            'https://docs.djangoproject.com/en/1.8/topics/http/sessions/#enabling-sessions'

    def clear(self):
        if self.SESSION_KEY in self.request().session:
            del self.request().session[self.SESSION_KEY]

    def add(self, **kwargs):
        self.request().session[self.SESSION_KEY] = list(self) + \
                                                   [kwargs, ]

    def __iter__(self):
        items = self.request().session.get(self.SESSION_KEY, [])
        return iter(items)
