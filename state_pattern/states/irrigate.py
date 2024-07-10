from state_pattern.states.i_state import IState
import state_pattern.states.idle as idle

class Irrigate(IState):
    def __changeStateCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(2)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(idle.Idle())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(2, False)
