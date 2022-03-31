# project/app/api/roles.py


from fastapi import APIRouter, HTTPException

from app.api import crud
from app.models.pydantic import RolePayloadSchema, RoleResponseSchema


router = APIRouter()


@router.post("/", response_model=RoleResponseSchema, status_code=201)
async def create_role(payload: RolePayloadSchema) -> RoleResponseSchema:
    role_id = await crud.post(payload)

    response_object = {"id": role_id, "name": payload.name}
    return response_object
