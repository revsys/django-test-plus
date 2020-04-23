import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseGone
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import generic

from .forms import DataForm, NameForm
from .models import Data

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


# Function-based test views

def status_code_view(request, status=200):
    status = int(status)
    if status in (301, 302):
        is_perm = True if status == 301 else False
        return redirect('view-200', permanent=is_perm)

    return HttpResponse('', status=status)


def view_200(request):
    return HttpResponse('', status=200)


def view_201(request):
    return HttpResponse('', status=201)


def view_204(request):
    return HttpResponse('', status=204)


def view_301(request):
    return HttpResponse('', status=301)


def view_302(request):
    return HttpResponse('', status=302)


def view_400(request):
    return HttpResponse('', status=400)


def view_401(request):
    return HttpResponse('', status=401)


def view_403(request):
    return HttpResponse('', status=403)


def view_404(request):
    return HttpResponse('', status=404)


def view_405(request):
    return HttpResponse('', status=405)


def view_409(request):
    return HttpResponse('', status=409)


def view_410(request):
    return HttpResponseGone()


def view_redirect(request):
    return redirect('view-200')


def view_json(request):
    ctype = request.META['CONTENT_TYPE']
    if not ctype.startswith('application/json'):
        raise ValueError("Request's content-type should be 'application/json'. Got '{}' instead.".format(ctype))

    data = json.loads(request.body.decode('utf-8'))
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def needs_login(request):
    return HttpResponse('', status=200)


def data_1(request):
    list(Data.objects.all())
    return HttpResponse('', status=200)


def data_5(request):
    list(Data.objects.all())
    list(Data.objects.all())
    list(Data.objects.all())
    list(Data.objects.all())
    list(Data.objects.all())
    return HttpResponse('', status=200)


def view_context_with(request):
    return render(request, 'base.html', {'testvalue': True})


def view_context_without(request):
    return render(request, 'base.html', {})


def view_is_ajax(request):
    return HttpResponse('', status=200 if request.is_ajax() else 404)


def view_contains(request):
    return render(request, 'test.html', {})


def view_headers(request):
    response = HttpResponse('', content_type='text/plain', status=200)
    response['X-Custom'] = 1
    return response


# Class-based test views

class CBView(generic.View):

    def get(self, request):
        return HttpResponse('', status=200)

    def post(self, request):
        return HttpResponse('', status=200)

    def special(self):
        if hasattr(self, 'special_value'):
            return self.special_value
        else:
            return False


class CBLoginRequiredView(generic.View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CBLoginRequiredView, self).dispatch(*args, **kwargs)

    def get(self, request):
        return HttpResponse('', status=200)


class CBDataView(generic.UpdateView):

    model = Data
    template_name = "test.html"
    form_class = DataForm

    def get_success_url(self):
        return reverse("view-200")

    def get_context_data(self, **kwargs):
        kwargs = super(CBDataView, self).get_context_data(**kwargs)
        if hasattr(self.request, "some_data"):
            kwargs.update({
                "some_data": self.request.some_data
            })
        return kwargs


class CBTemplateView(generic.TemplateView):

    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        kwargs['revsys'] = 42
        return kwargs


class FormErrors(generic.FormView):
    form_class = NameForm
    template_name = 'form_errors.html'
