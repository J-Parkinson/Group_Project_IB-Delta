from enum import Enum


class uploadState(Enum):
    Unloaded = 0
    Loaded = 1
    Running = 2
    Saving = 3
