from state_pattern.pump_mixture_system.i_state import IState
from datetime import datetime
import state_pattern.pump_mixture_system.idle as idle

class SecondaryPumpOn(IState):
    def __prioritizeScheduledPump(self) -> bool:
        minute = datetime.now().minute
        return minute >= 58

    def __tankFilled(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(5)

    def taskLoop(self) -> None:
        if self.__prioritizeScheduledPump() or self.__tankFilled():
            self._context.setState(idle.Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(7, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(7, False)
