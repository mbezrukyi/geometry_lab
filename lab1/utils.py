import json
import math
from typing import Any


def read_json(file_path: str) -> Any:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def custom_function(x: float) -> float:
    # return math.exp(x) + 3
    return math.cos(x) + 3
