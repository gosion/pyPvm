from pvm.utils import CaseInsensitiveDict
from pvm.activities.activity import Activity
from pvm.activities.cycle import Cycle

ACTIVIES = CaseInsensitiveDict(Activity=Activity, Cycle=Cycle)


def register_activity_type(name, type):
    if name not in ACTIVIES:
        ACTIVIES[name] = type
