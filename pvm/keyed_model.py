from uuid import uuid1, UUID


class KeyedModel(object):
    """模型基类，以uuid为key
    """

    def __init__(self, id: UUID = None) -> None:
        self._id: UUID = id or uuid1()

    @property
    def id(self) -> UUID:
        return self._id
