from dataclasses import dataclass

@dataclass
class ImportOrderOutput:
    order_number: str
    result: bool
    exception: Exception = None