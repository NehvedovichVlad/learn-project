from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def xxx(request: HttpRequest) -> HttpResponse:
    context = {
        "theme": "dark"
    }

    resp = render(request, 'hello/hello.html', context)
    return resp