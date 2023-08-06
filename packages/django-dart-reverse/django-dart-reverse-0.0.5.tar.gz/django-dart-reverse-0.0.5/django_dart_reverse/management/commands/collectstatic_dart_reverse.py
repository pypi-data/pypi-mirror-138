import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand
from django_dart_reverse.utils.collect_urls import collect_urls
from django.urls import get_resolver
from django.template import loader
from django.conf import settings
from django_dart_reverse.utils.reverse_class import Reverse
from typing import List
from django.template.loaders.app_directories import get_app_template_dirs


class Command(BaseCommand):
    help = 'Creates .dart file with reverse dictionary'
    requires_system_checks = False



    def __get_location(self) -> str:
        output_path = getattr(settings, 'DART_REVERSE_PATH')
        if output_path:
            return output_path

        if not hasattr(settings, 'STATIC_ROOT') or not settings.STATIC_ROOT:
            raise ImproperlyConfigured(
                'The collectstatic_dart_reverse command needs settings.DART_REVERSE_PATH or settings.STATIC_ROOT to be set.')

        return os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js')

    def __get_urls(self) -> List[Reverse]:
        urls = list()
        for value in collect_urls(get_resolver().url_patterns):
            urls.append(value)
        return urls

    def handle(self, *args, **kwargs) -> None:

        location = self.__get_location()
        urls = self.__get_urls()
        throw_exception = getattr(settings, 'DART_REVERSE_THROW_EXCEPTION', False)
        throw_warning = getattr(settings, 'DART_REVERSE_THROW_WARNING', True)
        content = loader.render_to_string('dart/dart_file.tpl',
                                          dict(urls=urls, throw_exception=throw_exception, throw_warning=throw_warning))
        file = 'reverse.dart'

        fs = FileSystemStorage(location=location)
        if fs.exists(file):
            fs.delete(file)

        fs.save(file, ContentFile(content))

        if len(sys.argv) > 1 and sys.argv[1] in ['collectstatic_dart_reverse']:
            self.stdout.write('dart-reverse file written to %s' % location)
