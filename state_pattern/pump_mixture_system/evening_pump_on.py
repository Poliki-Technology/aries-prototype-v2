from state_pattern.pump_mixture_system.i_state import IState
from datetime import datetime, timedelta
import state_pattern.pump_mixture_system.idle as idle
import state_pattern.pump_mixture_system.wait_mix as wait

class EveningPumpOn(IState):
    __startTimestamp = 0
    def __pumpTimeout(self) -> bool:
        return datetime.now() - self.__startTimestamp >= timedelta(minutes=20)

    def __tankEmpty(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(3)

    def taskLoop(self) -> None:
        if self.__pumpTimeout():
            self._context.setState(idle.Idle())
            return
        if self.__tankEmpty():
            self._context.setState(wait.WaitMix())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(6, True)
        self.__startTimestamp = datetime.now()

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(6, False)
