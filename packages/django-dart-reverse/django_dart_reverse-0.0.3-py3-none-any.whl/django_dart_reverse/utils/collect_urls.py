from django.urls import get_resolver, URLResolver, URLPattern
from django_dart_reverse.utils.reverse_class import Reverse


def collect_urls(patterns: list, names: list = None):
    for pattern in patterns:
        new_list = names if names else []
        if isinstance(pattern, URLResolver):
            if pattern.app_name:
                new_list.append(pattern.app_name)
            for value in collect_urls(pattern.url_patterns, new_list):
                yield value
        else:
            yield Reverse(pattern, new_list)
