from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from rest_framework import viewsets

from .serializer import MatchSerializer


class MatchView(viewsets.ViewSet):
    def create(self, request, format=None):
        serializer = MatchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=HTTP_200_OK)
