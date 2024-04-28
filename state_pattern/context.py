from __future__ import annotations
import state_pattern.states as states
from gpio.gpio_controller import GpioController

# the context class contains a _state that references the concrete state and setState method to change between states.
class Context:
    _state = None
    _gpioController = None

    def __init__(self, state: states.State) -> None:
        self.setState(state)
        self._gpioController = GpioController()
        self._gpioController.post_output(1, True)

    def getGpioController(self) -> GpioController:
        return self._gpioController

    def setState(self, state: states.State):
        print(f"Context: Transitioning to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def taskLoop(self):
        self.__state.taskLoop()
