import hashlib
import logging
import pathlib
import pickle
import tempfile
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Cache:
    roots: List[str]
    path: pathlib.Path = field(init=False)
    mymap: Dict[str, str] = field(init=False, default_factory=dict)
    data_path: pathlib.Path = field(init=False)

    def __post_init__(self):
        resolved = [str(pathlib.Path(path).resolve()) for path in self.roots]
        str2hash = "".join(resolved)
        result = hashlib.md5(str2hash.encode())
        self.path = pathlib.Path(tempfile.gettempdir()) / f"{result.hexdigest()}.pkl"
        logging.debug(f"creating {self.path} from {str2hash}")

    def load(self):
        if self.path.exists():
            with open(self.path, "rb") as fh:
                self.mymap = pickle.load(fh)

    def delete(self):
        self.path.unlink(missing_ok=True)

    def cache(self, map):
        with open(self.path, "wb") as fh:
            pickle.dump(map, fh)

    def report_types(self, tosign):
        for _str in tosign:
            print(self.mymap[_str], _str)

    def show_results(self, tosign):
        for _str in sorted(list(tosign)):
            print(_str)
