# project/app/api/crud.py


from app.models.pydantic import RolePayloadSchema
from app.models.tortoise import RoleModel


async def post(payload: RolePayloadSchema) -> int:
    role = RoleModel(
        name=payload.name,
    )
    await role.save()
    return role.id
