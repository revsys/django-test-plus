from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Data


def view_200(request):
    return HttpResponse('', status=200)


def view_201(request):
    return HttpResponse('', status=201)


def view_302(request):
    return HttpResponse('', status=302)


def view_404(request):
    return HttpResponse('', status=404)


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
