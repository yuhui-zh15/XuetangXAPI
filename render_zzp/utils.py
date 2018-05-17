#encoding=utf-8
def require(**fields):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            data = args[0]
            for field, meaning in fields.iteritems():
                if field not in data:
                    raise ValueError('<%s>\n\tMissing field `%s`\n\tMeaning: %s' % (func.__name__, field, meaning))
            return func(*args, **kwargs)
        return _wrapper
    return _decorator


def normalized(name):
    puncts = {u'(', u'（', u'—', u'-'}
    for punct in puncts:
        if punct in name:
            return name[:name.index(punct)]
    return name