from cProfile import label

from django.apps import AppConfig


class HelloConfig(AppConfig):
    name = 'hello'
    name = f'applications.{label}'
