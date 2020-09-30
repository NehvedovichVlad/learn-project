"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


def view_index(request: HttpRequest):
    index_html = Path(__file__).parent.parent.parent / "static" / "index.html"
    with index_html.open("r") as f:
        content = f.read()
    return HttpResponse(content)


def view_logo(request: HttpRequest):
    logo = Path(__file__).parent.parent.parent / "static" / "img" / "logo.png"
    with logo.open("rb") as fl:
        content = fl.read()
    return HttpResponse(content, content_type="image/png")


def view_css(request: HttpRequest):
    css_file = Path(__file__).parent.parent.parent / "static" / "styles" / "style.css"
    with css_file.open("r") as fp:
        content = fp.read()
    return HttpResponse(content, content_type="text/css")


def view_hello(request: HttpRequest):
    hello_html = Path(__file__).parent.parent.parent / "static" / "hello.html"
    with hello_html.open("r") as hel:
        content = hel.read()
    return HttpResponse(content)

@csrf_exempt
def view_hello_update(request: HttpRequest):
    print(123)
    return HttpResponse("sdfs")


def reset_hello(request: HttpRequest):
    return HttpResponse()


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", view_index),
    path("image/logo.png", view_logo),
    path("style/style.css", view_css),
    path("hello/", view_hello),
    path("hello-update", view_hello_update),
    path("reset", reset_hello),
]
