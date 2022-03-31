# project/app/api/roles.py


from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import RolePayloadSchema, RoleResponseSchema
from app.models.tortoise import RoleSchema


router = APIRouter()


@router.post("/", response_model=RoleResponseSchema, status_code=201)
async def create_role(payload: RolePayloadSchema) -> RoleResponseSchema:
    role_id = await crud.post(payload)

    response_object = {"id": role_id, "name": payload.name}
    return response_object


@router.get("/{id}/", response_model=RoleSchema)
async def read_role(id: int) -> RoleSchema:
    role = await crud.get(id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role
