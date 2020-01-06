from enum import IntEnum


class TransitionState(IntEnum):
    def __new__(cls, value, phrase, description=""):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.phrase = phrase
        obj.description = description

        return obj

    Pending = 1, "Pending", "Pending to run."
    Passed = 1 << 1, "Passed", "Passed."
    Waiting = 1 << 2, "Waiting", "Waiting for interaction."
    Blocked = 1 << 3, "Blocked", "Cannot run forward."
