class CaseInsensitiveDict(object):
    def __init__(self, *args, **kwargs):
        self._raw = dict(
            [(x.lower(), (x, y)) for x, y in dict(*args, **kwargs).items()]
        )

    def __getitem__(self, key):
        return self._raw[key.lower()][1]

    def __setitem__(self, key, value):
        self._raw[key.lower()] = (key, value)

    def __delitem__(self, key):
        del self._raw[key.lower()]

    def __contains__(self, key):
        return self._raw.__contains__(key.lower())

    def get(self, key, *args, **kwargs):
        return dict(self.items()).get(key, *args, **kwargs)

    def __repr__(self):
        return dict(self.items()).__repr__()

    def items(self):
        return self._raw.values()

    def keys(self):
        return dict(self.items()).keys()

    def values(self):
        return dict(self.items()).values()

    def lower_items(self):
        return ((k, v[1]) for k, v in self._raw.items())

    def __eq__(self, other):
        return dict(self.lower_items()) == dict(other.lower_items())

    def __len__(self):
        return len(self._raw)

    def __iter__(self):
        return (k for k, v in self._raw.values())

    def clone(self):
        return CaseInsensitiveDict(self._raw.values())


if __name__ == "__main__":
    d = CaseInsensitiveDict(a=1, b=2, Activity=3)
    d1 = CaseInsensitiveDict(a=1, b=2, Activity=3)
    d2 = CaseInsensitiveDict([("a", 1), ("b", 2), ("Activity", 3)])
    print(d)
    print(d2)
    print(d["activity"])
    print(d.get("Activity", 0))
    print(d == d1)
    d3 = d.clone()
    print(d3)
    d3["c"] = 4
    print(d3)
    print(d)
    print(d.keys())
    print("activity" in d)
    print("Activity" in d)
    print("c" in d)
    print("c" in d3)
