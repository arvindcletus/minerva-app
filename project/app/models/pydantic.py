# project/app/models/pydantic.py


from pydantic import BaseModel


class RolePayloadSchema(BaseModel):
    name: str


class RoleResponseSchema(RolePayloadSchema):
    id: int
