from numpy import *
from django.http import HttpResponse


def generate_system(request, id):
    content = "Test"
    status_code = 200
    mimetype='text/plain'

    return HttpResponse(content, status=status_code, mimetype=mimetype)
