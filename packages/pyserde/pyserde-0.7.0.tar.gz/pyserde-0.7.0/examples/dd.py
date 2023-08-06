from serde import serde, to_dict, from_dict, to_tuple, from_tuple
from typing import Optional, Union


@serde
class OptDefault:
    """
    Optionals.
    """

    n: Optional[int] = None
    i: Optional[int] = 10


@serde
class Foo:
    a: Union[int, float]


if __name__ == "__main__":
    """
    o = OptDefault()
    data = to_dict(o)
    print(data)
    o = from_dict(OptDefault, data)
    print(o)
    data = to_tuple(o)
    print(data)
    o = from_tuple(OptDefault, data)
    print(o)
    """

    f = from_dict(Foo, {"a": "10"})
    print(f)
