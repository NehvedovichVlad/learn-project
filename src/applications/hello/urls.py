from django.urls import path

from applications.hello.views import view_index, view_update, view_reset

urlpatterns = [
    path("", view_index),
    path("update/", view_update),
    path("reset/", view_reset),
]