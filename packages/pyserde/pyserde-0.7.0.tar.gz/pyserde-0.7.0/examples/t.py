from typing import Optional
from serde import serde, from_dict, field

@serde
class Foo:
    bar: Optional[list[int]] = field(default_factory=list)

if __name__ == "__main__":
    print(from_dict(Foo, {"bar": None}))
