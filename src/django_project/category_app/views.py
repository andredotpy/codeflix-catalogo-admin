from uuid import UUID

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
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


class CategoryViewSet(viewsets.ViewSet):
    @staticmethod
    def list(request: Request) -> Response:
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(request=ListCategoryRequest())

        categories = [
            {
                'id': str(category.id),
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active,
            }
            for category in output.data
        ]

        return Response(
            status=HTTP_200_OK,
            data=categories,
        )

    @staticmethod
    def retrieve(request: Request, pk=None):
        try:
            category_id = UUID(pk)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())
        try:
            category = use_case.execute(
                request=GetCategoryRequest(id=category_id)
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        category_output = {
            'id': str(category.id),
            'name': category.name,
            'description': category.description,
            'is_active': category.is_active,
        }
        return Response(status=HTTP_200_OK, data=category_output)
