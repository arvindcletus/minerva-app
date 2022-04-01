# project/app/models/tortoise.py


from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class NameMixin:
    name = fields.CharField(max_length=40, unique=True)


class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class RoleModel(MyAbstractBaseModel, NameMixin, TimestampMixin):
    class Meta:
        table = "roles"


class UserModel(MyAbstractBaseModel, TimestampMixin):
    role_id = fields.ForeignKeyField("models.RoleModel", related_name="roles")
    first_name = fields.CharField(35, null=True)
    last_name = fields.CharField(35, null=True)
    username = fields.CharField(70, unique=True)
    email = fields.CharField(255, unique=True)
    password_hash = fields.CharField(128)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


RoleSchema = pydantic_model_creator(RoleModel)
