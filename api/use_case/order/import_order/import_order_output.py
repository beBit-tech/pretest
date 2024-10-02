from dataclasses import dataclass

@dataclass
class ImportOrderOutput:
    number: str
    result: bool
    exception: Exception = None