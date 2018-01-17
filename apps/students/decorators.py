def edu_level_selected(function):
    def wrap(request, *args, **kwargs):
        if 'edu_id' in request.session:
            return function(request, *args, **kwargs)
        else:
            messages.add_message(request, messages.WARNING, "Please select education Level")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
