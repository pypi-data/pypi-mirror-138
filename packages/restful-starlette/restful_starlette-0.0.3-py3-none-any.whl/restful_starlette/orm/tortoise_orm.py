from enum import IntEnum
from typing import Dict, Tuple, Optional, Type, Any
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.manager import Manager
from uuid import UUID, uuid4


class TortoiseOrmKit:

    @staticmethod
    def collect_modules(tortoise_orm_settings) -> Dict:
        modules = {}
        for k, v in tortoise_orm_settings["apps"].items():
            modules[k] = v["models"]
        return modules


class CustomManager(Manager):
    """
        defined manager
    """


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True, description="创建时间")
    modified_at = fields.DatetimeField(null=True, auto_now=True, description="更新时间")


class ActiveStatusEnum(IntEnum):
    """
        active status
    """
    DEACTIVE = 0
    ACTIVE = 1


class UUIDHex(fields.UUIDField):

    def to_db_value(self, value: Any, instance: "Union[Type[Model], Model]") -> Optional[str]:
        if isinstance(value, UUID):
            return make_uuid_hex(uuid_obj=value)
        return value and str(value)


def make_uuid_hex(uuid_obj: UUID = None):
    if uuid_obj is None:
        uuid_obj = uuid4()
    return uuid_obj.hex


class TortoiseOrmAbstractModel(models.Model, TimestampMixin):
    is_active: ActiveStatusEnum = fields.IntEnumField(ActiveStatusEnum, default=ActiveStatusEnum.ACTIVE,
                                                      description="是否有效")
    id: int = fields.IntField(pk=True, description="PK")
    uid: UUID = UUIDHex(unique=True, description="UID", default=make_uuid_hex)

    class Meta:
        # table = 'base'
        # table_description = 'base'
        # indexes = (("field_a", "field_b"),)
        # ordering = ["name", "-score"]
        # unique_together=(("field_a", "field_b"), )
        abstract = True
        manager = CustomManager()

    def __str__(self) -> str:
        return f"{self.id}-{self.uid.hex}"

    # @classmethod
    # def create_pydantic_model(cls, *,
    #                           name=None,
    #                           exclude: Tuple[str, ...] = (),
    #                           include: Tuple[str, ...] = (),
    #                           computed: Tuple[str, ...] = (),
    #                           allow_cycles: Optional[bool] = None,
    #                           sort_alphabetically: Optional[bool] = None,
    #                           _stack: tuple = (),
    #                           exclude_readonly: bool = False,
    #                           meta_override: Optional[Type] = None, ):
    #     return pydantic_model_creator(cls=cls, name=name,
    #                                   exclude=exclude,
    #                                   include=include,
    #                                   computed=computed,
    #                                   allow_cycles=allow_cycles,
    #                                   sort_alphabetically=sort_alphabetically,
    #                                   _stack=_stack,
    #                                   exclude_readonly=exclude_readonly,
    #                                   meta_override=meta_override)
