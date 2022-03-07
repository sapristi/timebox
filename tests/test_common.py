from pydantic import Field

from timebox.common import ProviderCommon


def test_set_secrets():
    class Provider(ProviderCommon):
        secret_value: str = Field(secret=True)

        def __str__(self):
            return "dummy"

    p = Provider(secret_value="SECRET")
    p.set_secrets({"SECRET": "VALUE"})
    assert p.secret_value == "VALUE"
