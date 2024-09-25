from dataclasses import dataclass
from uuid import UUID

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, request: UpdateCategoryRequest) -> None:
        category = self.repository.get_by_id(id=request.id)
        if category is None:
            raise CategoryNotFound(f'Category with id: {request.id} not found!')

        if request.is_active is True:
            category.activate()
        elif request.is_active is False:
            category.deactivate()

        name = category.name
        description = category.description

        if request.name is not None:
            name = request.name

        if request.description is not None:
            description = request.description

        category.update_category(name=name, description=description)

        self.repository.update(category=category)
