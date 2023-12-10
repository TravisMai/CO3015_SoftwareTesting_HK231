import os
from pathlib import Path
import math


def gen_file_in_path(temp_dir: str | Path, file_size: float) -> Path:
    """This function return a temp path to file with size with size at least `file_size` bytes"""
    file_name = str(file_size).replace(".", "_") + "KB.txt"
    file_path = Path(temp_dir, file_name)
    file_size_in_bytes = math.ceil(file_size * 1024)

    with open(file_path, "wb") as file:
        file.write(b"x" * file_size_in_bytes)

    return file_path.resolve()
