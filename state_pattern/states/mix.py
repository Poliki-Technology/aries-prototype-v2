from state_pattern.states.i_state import IState
import state_pattern.states.irrigate as irr

class Mix(IState):
    def __changeStateCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(1)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(irr.Irrigate())

    def applyState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, True)

    def ceaseState(self) -> None:
        gpio = self._context.getGpioController()
        gpio.post_output(1, False)
