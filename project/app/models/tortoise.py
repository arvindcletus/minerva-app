# project/app/models/tortoise.py


from tortoise import fields
from tortoise.models import Model


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class NameMixin:
    name = fields.CharField(40, unique=True)


class MyAbstractBaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class UserModel(MyAbstractBaseModel, TimestampMixin):
    # Overriding the id definition
    # from MyAbstractBaseModel
    id = fields.UUIDField(pk=True)

    # Adding additional fields
    first_name = fields.CharField(35, null=True)
    last_name = fields.CharField(35, null=True)
    username = fields.CharField(70, null=False)
    email = fields.CharField(255, null=False)
    password = fields.CharField(255, null=False)

    class Meta:
        table = "users"


class RoleModel(MyAbstractBaseModel, NameMixin, TimestampMixin):
    class Meta:
        table = "roles"
