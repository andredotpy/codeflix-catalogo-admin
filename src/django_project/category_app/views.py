from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)

from src.core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from src.core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from src.django_project.category_app.repository import (
    DjangoORMCategoryRepository,
)
from src.django_project.category_app.serializers import (
    ListCategoryResponseSerializer,
    RetrieveCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    CreateCategoryRequestSerializer,
    CreateCategoryResponseSerializer,
)


class CategoryViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        categories = use_case.execute(request=ListCategoryRequest())
        response_serializer = ListCategoryResponseSerializer(
            instance=categories
        )
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    @staticmethod
    def retrieve(request: Request, pk=None) -> Response:
        request_serializer = RetrieveCategoryRequestSerializer(data={'id': pk})
        request_serializer.is_valid(raise_exception=True)
        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            category = use_case.execute(
                request=GetCategoryRequest(
                    id=request_serializer.validated_data['id']
                )
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)
        response_serializer = RetrieveCategoryResponseSerializer(
            instance=category
        )
        return Response(status=HTTP_200_OK, data=response_serializer.data)

    @staticmethod
    def create(request: Request) -> Response:
        request_serializer = CreateCategoryRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        use_case = CreateCategory(repository=DjangoORMCategoryRepository())
        try:
            created_category = use_case.execute(
                request=CreateCategoryRequest(
                    **request_serializer.validated_data,
                )
            )
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)
        response_serializer = CreateCategoryResponseSerializer(
            instance=created_category
        )
        return Response(status=HTTP_201_CREATED, data=response_serializer.data)
