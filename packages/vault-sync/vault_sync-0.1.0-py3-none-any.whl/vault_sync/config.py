from uuid import UUID

from pydantic import AnyUrl, BaseModel, Extra, validator


def is_valid_uuid(value: str) -> bool:
    try:
        val = UUID(value)
        return str(val) == value
    except Exception:
        return False


class StrictModel(BaseModel):
    class Config:
        allow_mutation = False
        use_enum_values = True
        extra = Extra.forbid


class Vault(StrictModel):
    url: AnyUrl
    role_id: str
    secret_id: str
    kv_store: str

    @validator("role_id", "secret_id")
    def must_be_uuid(cls, value):
        if not is_valid_uuid(value):
            raise ValueError("must be a valid uuid")
        return value


class Config(StrictModel):
    source: Vault
    destination: Vault
