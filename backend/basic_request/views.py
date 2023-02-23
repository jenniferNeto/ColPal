from django.http import HttpResponse
from django.http import HttpRequest


# Create your views here.
def index(request: HttpRequest):
    return HttpResponse(request.build_absolute_uri())
