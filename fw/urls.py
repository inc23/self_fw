from dataclasses import dataclass
from typing import Type
from view import View


@dataclass
class Urls:
    url: str
    view: Type[View]