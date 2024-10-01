from dataclasses import dataclass

@dataclass
class CreateProductOutput:
    number: str
    result: bool
    exception: Exception = None