import timeit
from dataclasses import dataclass


@dataclass
class Foo:
    a: int
    b: float
    c: str
    d: bool

    def to_dict(self):
        return {"a": self.a, "b": self.b, "c": self.c, "d": self.d}

    def to_dict_typecheck(self):
        if not isinstance(self.a, int):
            raise Exception("'a' is not type of int")
        if not isinstance(self.b, float):
            raise Exception("'b' is not type of float")
        if not isinstance(self.c, str):
            raise Exception("'c' is not type of str")
        if not isinstance(self.d, bool):
            raise Exception("'d' is not type of bool")
        return {"a": self.a, "b": self.b, "c": self.c, "d": self.d}

    def to_dict_conversion(self):
        return {"a": int(self.a), "b": float(self.b), "c": str(self.c), "d": bool(self.d)}

    @classmethod
    def from_dict(cls, data):
        return cls(a=data["a"], b=data["b"], c=data["c"], d=["d"])

    @classmethod
    def from_dict_typecheck(cls, data):
        if not isinstance(data["a"], int):
            raise Exception("'a' is not type of int")
        if not isinstance(data["b"], float):
            raise Exception("'b' is not type of float")
        if not isinstance(data["c"], str):
            raise Exception("'c' is not type of str")
        if not isinstance(data["d"], bool):
            raise Exception("'d' is not type of bool")
        return cls(a=data["a"], b=data["b"], c=data["c"], d=["d"])

    @classmethod
    def from_dict_conversion(cls, data):
        return cls(a=int(data["a"]), b=float(data["b"]), c=str(data["c"]), d=bool(["d"]))


def main():
    f = Foo(10, 10.0, "foo", True)
    data = {"a": 10, "b": 10.0, "c": "foo", "d": True}
    print(timeit.timeit(lambda: f.to_dict(), number=10000000))
    print(timeit.timeit(lambda: f.to_dict_typecheck(), number=10000000))
    print(timeit.timeit(lambda: f.to_dict_conversion(), number=10000000))
    print(timeit.timeit(lambda: Foo.from_dict(data), number=10000000))
    print(timeit.timeit(lambda: Foo.from_dict_typecheck(data), number=10000000))
    print(timeit.timeit(lambda: Foo.from_dict_conversion(data), number=10000000))


if __name__ == "__main__":
    main()
