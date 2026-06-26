from abc import ABC, abstractmethod
from typing import Iterable, Mapping


class Storage(ABC):
    """Base interface for saving parsed messages."""

    @abstractmethod
    def save(self, target: str, messages: Iterable[Mapping]) -> str:
        """Persist messages for a given target. Returns the output file path."""
        raise NotImplementedError
