from serde import serde, SerdeSkip
from serde.json import from_json
from typing import Optional


def des(cls, o):
    raise SerdeSkip()


@serde(deserializer=des)
class Foo:
    a: Optional[str]
    b: str


if __name__ == "__main__":
    print(from_json(Foo, '{"a": "foo", "b": "bar"}'))  # -> Foo(a='foo')
    print(from_json(Foo, '{}'))           # -> KeyError: 'a'


"""
def from_dict(data, reuse_instances = True):
  if reuse_instances is Ellipsis:
    reuse_instances = True

  if data is None:
    return None

  return cls(
    serde_custom_class_deserializer(
      Optional[str],
      data,
      data.get("a"),
      default=lambda: (serde_custom_class_deserializer(str, data, data.get("a"), default=lambda: data["a"])) if data.get("a") is not None else None),
  )
"""
