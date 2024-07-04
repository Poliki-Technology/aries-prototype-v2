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
    def taskLoop(self) -> None:
        pass

    @abstractmethod
    def applyState(self) -> None:
        pass

    @abstractmethod
    def ceaseState(self) -> None:
        pass

class Idle(State):
    def __openNutrientCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(3)

    def __morningPumpCondition(self) -> bool:
        return False # stub

    def __eveningPumpCondition(self) -> bool:
        return False # stub

    def taskLoop(self) -> None:
        if self.__openNutrientCondition():
            self._context.setState(StateOne())
            return

        if self.__morningPumpCondition():
            self._context.setState(MorningPumpOn())
            return

        if self.__eveningPumpCondition():
            self._context.setState(EveningPumpOn())

    def applyState(self) -> None:
        return # do nothing

    def ceaseState(self) -> None:
        return # do nothing

class StateOne(State):
    def __changeStateCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(1)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(StateTwo())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, True)
        gpio.post_output(3, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, False)
        gpio.post_output(3, False)

class StateTwo(State):
    def __changeStateCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(2)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, False)

class MorningPumpOn(State):
    def __changeStateCondition(self) -> bool:
        return True # stub

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, False)

class EveningPumpOn(State):
    def __changeStateCondition(self) -> bool:
        return True # stub

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(5, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(5, False)
