from uuid import UUID

from pvm.keyed_model import KeyedModel


class Walker(KeyedModel):
    """流程状态转移参与者，负责携带token
    """

    def __init__(self, id: UUID = None) -> None:
        super(Walker, self).__init__(id)
        self.token = None

    def walk(self):
        if self.token is None:
            raise Exception("Please make sure walker has a valid token")

        if self.token.destination is None:
            return None
        else:
            return self.token.destination.execute(self.token)
