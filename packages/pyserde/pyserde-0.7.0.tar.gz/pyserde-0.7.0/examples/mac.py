from serde import serde, field
from serde.json import to_json, from_json
from macaddress import EUI48
from typing import Optional


@:serde
class Foo:
    addr: EUI48 = field(serializer=lambda x: str(x), deserializer=lambda x: EUI48(x))
    opt_addr: Optional[EUI48] = field(serializer=lambda x: x and str(x), deserializer=lambda x: x and EUI48(x))


f = Foo(EUI48('01-23-45-67-89-ab'), None)
print(f)
json_data = to_json(f)
print(json_data)
f = from_json(Foo, json_data)
print(f)
