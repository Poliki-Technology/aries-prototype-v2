from abc import ABC, abstractmethod
from state_pattern.context import Context

class IState(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def taskLoop(self) -> None:
        pass

    @abstractmethod
    def applyState(self) -> None:
        pass

    @abstractmethod
    def ceaseState(self) -> None:
        pass