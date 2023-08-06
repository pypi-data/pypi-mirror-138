import dataclasses
import os


@dataclasses.dataclass
class Dataset:
    id: str
    alias: str

    @property
    def path(self):
        return os.path.join(self.alias, self.id)
