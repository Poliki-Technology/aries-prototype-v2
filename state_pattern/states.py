from __future__ import annotations
from abc import ABC, abstractmethod
import state_pattern.context as context

class State(ABC):
    @property
    def context(self) -> context.Context:
        return self._context

    @context.setter
    def context(self, context: context.Context) -> None:
        self._context = context
    
    @abstractmethod
    def __changeStateCondition(self) -> bool:
        pass

    @abstractmethod
    def taskLoop(self) -> None:
        pass

class Yellow(State):
    def __changeStateCondition(self) -> bool:
        gpio = self.context().getGPIOController()
        return gpio.get_input(1)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return

        gpio = self.context().getGPIOController()
        gpio.post_output(1, False)
        gpio.post_output(2, True)
        self._context.setState(Red())

class Red(State):
    def __changeStateCondition(self) -> bool:
        gpio = self.context().getGPIOController()
        return gpio.get_input(1)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return

        gpio = self.context().getGPIOController()
        gpio.post_output(1, True)
        gpio.post_output(2, False)
        self._context.setState(Yellow())

