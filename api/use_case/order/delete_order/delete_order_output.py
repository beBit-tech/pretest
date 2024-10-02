from dataclasses import dataclass

@dataclass
class DeleteOrderOutput:
    result: bool
    exception: Exception = None