# project/app/api/crud.py


from typing import List, Union

from app.models.pydantic import RolePayloadSchema
from app.models.tortoise import RoleModel


async def post(payload: RolePayloadSchema) -> int:
    role = RoleModel(
        name=payload.name,
    )
    await role.save()
    return role.id


async def get(id: int) -> Union[dict, None]:
    role = await RoleModel.filter(id=id).first().values()
    if role:
        return role
    return None


async def get_all() -> List:
    roles = await RoleModel.all().values()
    return roles


async def delete(id: int) -> int:
    role = await RoleModel.filter(id=id).first().delete()
    return role
