from typing import List
from django.urls import URLPattern
import re
from django.utils.safestring import mark_safe


class Reverse:
    name: str = None
    params: List[str] = None
    path: str = None
    num_params: int = None

    def __init__(self, pattern: URLPattern, name_prefix: List[str] = None):
        if pattern.name:
            self.name = f'{":".join(name_prefix)}:{pattern.name}' if name_prefix else pattern.name
        else:
            self.name = ':'.join(name_prefix)
        self.params = self.__get_params(pattern)
        self.path = self.__get_path(pattern)
        self.num_params = len(self.params)

    def __get_params(self, pattern: URLPattern) -> List[str]:
        regex = '<[a-zA-Z_]*:[a-zA-Z_]*>'
        return [param.split(':')[1].replace('>', '') for param in re.findall(regex, str(pattern.pattern))]

    def __get_path(self, pattern: URLPattern) -> str:
        path = str(pattern.pattern)
        path = path.replace('$', '\\$')
        for param in self.params:
            regex = f'<[a-zA-Z_]*:{param}>'
            path = path.replace(re.findall(regex, path)[0], '${params?["%s"]}' % param)
        return mark_safe(path)

    def __get_param_identifier(self) -> str:
        return self.name.upper().replace(':', '_')

