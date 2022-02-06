from os import listdir
from pathlib import Path
from typing import Dict, Any, Callable


class FileImporter:
    def import_raw_from(self, folder: str, on_finish_import: Callable):
        self._list_files(Path(folder))
        raw = [self._to_dict(f) for f in self._files]
        if on_finish_import:
            for r in raw:
                on_finish_import(**r)

    def _list_files(self, path: Path):
        files = [f for f in listdir(path) if ".pdf" in f]
        self._files = files

    @staticmethod
    def _to_dict(fname: str) -> Dict[str, Any]:
        d = dict()
        split = fname.split("_")
        d["creation_date"] = f"20{split[0][:2]}-{split[0][2:4]}-{split[0][4:]}"
        d["issuer"] = split[1]
        d["nr"] = split[2]
        d["amount"] = float(split[3][:-4])
        return d
