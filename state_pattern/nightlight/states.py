from state_pattern.pump_mixture_system.i_state import IState
from datetime import datetime

class LightOn(IState):
    def __changeState(self) -> bool:
        hr = datetime.now().hour
        return hr < 18 or hr == 23

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(LightOff())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(8, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(8, False)

class LightOff(IState):
    def __changeState(self) -> bool:
        return 18 <= datetime.now().hour <= 22

    def taskLoop(self) -> None:
        if self.__changeState():
            self._context.setState(LightOn())

    def applyState(self) -> None:
        return

    def ceaseState(self) -> None:
        return
