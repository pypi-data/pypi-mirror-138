from serde import serde
from dataclasses import fields
from typing import List

@serde
class Foo:
    a: list[int]


f = Foo([1,2])
ty = fields(Foo)[0].type
print(f.a.__class__)
