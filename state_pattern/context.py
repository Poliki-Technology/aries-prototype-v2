from __future__ import annotations
import state_pattern.pump_mixture_system as sp
from gpio.gpio_controller import GpioController

# the context class contains a _state that references the concrete state and setState method to change between states.
class Context:
    _state = None
    _gpioController = None

    def __init__(self, state: sp.i_state.IState) -> None:
        self.setState(state)
        self._gpioController = GpioController()

    def getGpioController(self) -> GpioController:
        return self._gpioController

    def setState(self, state: sp.i_state.IState):
        print(f"Context: Transitioning to {type(state).__name__}")
        if self._state != None:
            self._state.ceaseState()
        self._state = state
        self._state.context = self
        self._state.applyState()

    def taskLoop(self):
        self._state.taskLoop()
