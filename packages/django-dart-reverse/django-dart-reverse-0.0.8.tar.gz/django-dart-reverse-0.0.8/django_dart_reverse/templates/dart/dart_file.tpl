class InvalidReverseParamsException implements  Exception {
    InvalidReverseParamsException();
  }

String? reverse(String name, [Map? params]) {
    List data = [
    {% for url in urls %}
    {
    'name':'{{url.name}}',
    'url':(Map? params)=> {% if url.num_params > 0 %}{% for param in url.params %}(params?["{{param}}"] != null) &&{% endfor %} true ?{% endif %} '{{url.path}}'{% if url.num_params > 0 %}: throw new InvalidReverseParamsException(){% endif %},
    'num_params':{{url.num_params}}},
    {% endfor %} ];
    for (var value in data) {
    if (value['name'] == name && value['num_params'] == (params?.length ?? 0)) {
    {% if not throw_exception %}
    try {
    {% endif %}
      return value['url'](params);
    {% if not throw_exception %}
    }
    on InvalidReverseParamsException {
        {% if throw_warning %}
        print('Warning: Reverse parameters were named incorrectly.');
        print(params);
        {% endif %}
    }
    {% endif %}
    }
  }
  return null;
}




