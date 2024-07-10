from state_pattern.states.i_state import IState
from state_pattern.states.idle import Idle

class MorningPumpOn(IState):
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