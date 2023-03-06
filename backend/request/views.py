from rest_framework import generics
from rest_framework.response import Response

from authentication.utils import check_user_permissions
from positions.models import Viewer, Uploader, Manager

from .models import Request
from .serializers import RequestSerializer


class RequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class RequestDetailAPIView(generics.RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get(self, request, pk_pipeline):
        check_user_permissions(request, pk_pipeline, Manager)

        instance = Request.objects.filter(pipeline_id=pk_pipeline)
        print(instance)
        return Response(RequestSerializer(instance, many=True).data)
"""

TODO: Requests need their own endpoints so that anyone who is a Manager of a specific pipeline, or superuser,
can look at all the requests made for a pipeline. The endpoint will allow the user to approve or reject any of
the modifications.

"""
