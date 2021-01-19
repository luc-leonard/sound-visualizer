import os
from pathlib import Path
from typing import Dict
from uuid import uuid4

from spleeter.separator import Separator as SpleeterSeparator


class Separator:
    def __init__(self, model: str):
        self.separator = SpleeterSeparator(model)

    def separate(self, filename: str) -> Dict[str, str]:
        random_path = Path('/tmp/') / uuid4().hex
        self.separator.separate_to_file(filename, random_path)
        files: Dict[str, str] = {}
        full_path = random_path / os.path.splitext(os.path.split(filename)[1])[0]
        print(full_path)
        for file in os.listdir(full_path):
            files[file.split('.')[0]] = str(full_path / file)
        return files
