from functools import wraps

from django.http import Http404


def ajax_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return function(request, *args, **kwargs)
    # wrap.__name__ = function.__name__
    # wrap.__doc__ = function.__doc__
    return wrap