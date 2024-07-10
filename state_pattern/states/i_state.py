from abc import ABC, abstractmethod
import state_pattern.context as context

class IState(ABC):
    @property
    def context(self) -> context.Context:
        return self._context

    @context.setter
    def context(self, context: context.Context) -> None:
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