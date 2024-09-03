from django.urls import resolve


def add_url_name(request):
    url_name = resolve(request.path_info).url_name
    return {'url_name': url_name}
