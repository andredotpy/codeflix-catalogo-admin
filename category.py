import uuid

class Category:
    def __init__(
        self,
        name,
        id= "",
        description = "",
        is_active = True
    ) -> None:
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

        if len(self.name) > 255:
            raise ValueError("name must have less than 256 characteres")

    def __str__(self) -> str:
        return f"<Category: {self.name} - {self.description} ({self.is_active})>"

    def __repr__(self) -> str:
        return f"<Category: {self.id}::{self.name}>"
