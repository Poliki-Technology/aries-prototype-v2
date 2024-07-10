from state_pattern.states.i_state import IState
import state_pattern.states.idle as idle

class MorningPumpOn(IState):
    def __changeStateCondition(self) -> bool:
        return True # stub

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(idle.Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(4, False)