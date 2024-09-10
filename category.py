import uuid
from dataclasses import dataclass, field


@dataclass
class Category:
    name: str
    description: str = ''
    is_active: bool = True
    id: str | uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def __str__(self) -> str:
        return (
            f'<Category: {self.name} - {self.description} ({self.is_active})>'
        )

    def __repr__(self) -> str:
        return f'<Category: {self.id}::{self.name}>'

    def __eq__(self, other) -> bool:
        return self.id == other.id and isinstance(other, Category)

    def validate(self) -> None | Exception:
        if len(self.name) > 255:
            raise ValueError('name cannot be longer than 255')

        if len(self.name) == 0:
            raise ValueError('name cannot be empty')

    def update_category(self, name, description) -> None:
        self.name = name
        self.description = description
        self.validate()

    def activate(self) -> None:
        self.is_active = True
        self.validate()

    def deactivate(self) -> None:
        self.is_active = False
        self.validate()
