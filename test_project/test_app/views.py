from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseGone
from django.shortcuts import render, redirect
from django.views import generic

from .models import Data


# Function-based test views

def view_200(request):
    return HttpResponse('', status=200)


def view_201(request):
    return HttpResponse('', status=201)


def view_302(request):
    return HttpResponse('', status=302)


def view_401(request):
    return HttpResponse('', status=401)


def view_403(request):
    return HttpResponse('', status=403)


def view_404(request):
    return HttpResponse('', status=404)


def view_405(request):
    return HttpResponse('', status=405)


def view_410(request):
    return HttpResponseGone()


def view_redirect(request):
    return redirect('view-200')


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


class CBTemplateView(generic.TemplateView):

    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        kwargs['revsys'] = 42
        return kwargs
