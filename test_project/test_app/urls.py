try:
    from django.conf.urls import url, patterns, include
except ImportError:
    from django.conf.urls.defaults import url, patterns, include

from .views import (
    data_1, data_5, needs_login, view_200, view_201, view_302,
    view_401, view_403, view_404, view_405, view_410, view_context_with,
    view_context_without, view_is_ajax, view_redirect
)

urlpatterns = patterns(
    '',
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^view/200/$', view_200, name='view-200'),
    url(r'^view/201/$', view_201, name='view-201'),
    url(r'^view/302/$', view_302, name='view-302'),
    url(r'^view/401/$', view_401, name='view-401'),
    url(r'^view/403/$', view_403, name='view-403'),
    url(r'^view/404/$', view_404, name='view-404'),
    url(r'^view/405/$', view_405, name='view-405'),
    url(r'^view/410/$', view_410, name='view-410'),
    url(r'^view/redirect/$', view_redirect, name='view-redirect'),
    url(r'^view/needs-login/$', needs_login, name='view-needs-login'),
    url(r'^view/data1/$', data_1, name='view-data-1'),
    url(r'^view/data5/$', data_5, name='view-data-5'),
    url(r'^view/context/with/$', view_context_with, name='view-context-with'),
    url(r'^view/context/without/$', view_context_without, name='view-context-without'),
    url(r'^view/isajax/$', view_is_ajax, name='view-is-ajax'),
)
