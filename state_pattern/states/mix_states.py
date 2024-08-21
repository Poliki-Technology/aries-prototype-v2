from state_pattern.states.i_state import IState
from datetime import datetime, timedelta
import state_pattern.states.idle as idle

class BeginMix(IState):
    __startTimestamp = None
    def __changeState(self) -> bool:
        return datetime.now() - self.__startTimestamp > timedelta(seconds=5)

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(MixState1())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, True)
        self.__startTimestamp = datetime.now()

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, False)
        self.__startTimestamp = None

class MixState1(IState):
    def __changeState(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(1)

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(MixState2())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(3, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(3, False)

class MixState2(IState):
    __startTimestamp = None
    def __changeState(self) -> bool:
        return datetime.now() - self.__startTimestamp > timedelta(seconds=5)

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(MixState3())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, True)
        self.__startTimestamp = datetime.now()

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, False)
        self.__startTimestamp = None

class MixState3(IState):
    def __changeState(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(2)

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(idle.Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, False)
