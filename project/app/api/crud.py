# project/app/api/crud.py


from app.models.pydantic import RolePayloadSchema
from app.models.tortoise import RoleModel
from typing import Union


async def post(payload: RolePayloadSchema) -> int:
    role = RoleModel(
        name=payload.name,
    )
    await role.save()
    return role.id


async def get(id: int) -> Union[dict, None]:
    name = await RoleModel.filter(id=id).first().values()
    if name:
        return name
    return None
