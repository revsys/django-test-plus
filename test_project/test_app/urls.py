try:
    from django.urls import include, re_path as url
except ImportError:
    try:
        from django.conf.urls import url, include
    except ImportError:
        from django.conf.urls.defaults import url, include

from .views import (
    FormErrors, data_1, data_5, needs_login, view_200, view_201, view_204,
    view_301, view_302, view_400, view_401, view_403, view_404, view_405,
    view_409, view_410, view_contains, view_context_with, view_context_without,
    view_headers, view_is_ajax, view_json, view_redirect,
    CBLoginRequiredView, CBView,
    status_code_view,
)

urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^status-code-view/(?P<status>[\d]+)/$', status_code_view, name='status-code-view'),
    url(r'^view/200/$', view_200, name='view-200'),
    url(r'^view/201/$', view_201, name='view-201'),
    url(r'^view/204/$', view_204, name='view-204'),
    url(r'^view/301/$', view_301, name='view-301'),
    url(r'^view/302/$', view_302, name='view-302'),
    url(r'^view/400/$', view_400, name='view-400'),
    url(r'^view/401/$', view_401, name='view-401'),
    url(r'^view/403/$', view_403, name='view-403'),
    url(r'^view/404/$', view_404, name='view-404'),
    url(r'^view/405/$', view_405, name='view-405'),
    url(r'^view/409/$', view_409, name='view-409'),
    url(r'^view/410/$', view_410, name='view-410'),
    url(r'^view/json/$', view_json, name='view-json'),
    url(r'^view/redirect/$', view_redirect, name='view-redirect'),
    url(r'^view/needs-login/$', needs_login, name='view-needs-login'),
    url(r'^view/data1/$', data_1, name='view-data-1'),
    url(r'^view/data5/$', data_5, name='view-data-5'),
    url(r'^view/context/with/$', view_context_with, name='view-context-with'),
    url(r'^view/context/without/$', view_context_without, name='view-context-without'),
    url(r'^view/isajax/$', view_is_ajax, name='view-is-ajax'),
    url(r'^view/contains/$', view_contains, name='view-contains'),
    url(r'^view/form-errors/$', FormErrors.as_view(), name='form-errors'),
    url(r'^view/headers/$', view_headers, name='view-headers'),
    url(r'^cbview/needs-login/$', CBLoginRequiredView.as_view(), name='cbview-needs-login'),
    url(r'^cbview/$', CBView.as_view(), name='cbview'),
]
