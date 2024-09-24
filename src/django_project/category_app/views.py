from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

# Create your views here.


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(
            status=HTTP_200_OK,
            data=[
                {
                    'id': 'b23r-asfdo',
                    'name': 'movie',
                    'description': 'descriçao de movie',
                    'is_active': True,
                }
            ],
        )
