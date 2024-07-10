from state_pattern.states.i_state import IState
from state_pattern.states.mix import Mix
from state_pattern.states.morning_pump_on import MorningPumpOn
from state_pattern.states.evening_pump_on import EveningPumpOn

class Idle(IState):
    def __openNutrientCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(3)

    def __morningPumpCondition(self) -> bool:
        return False # stub

    def __eveningPumpCondition(self) -> bool:
        return False # stub

    def taskLoop(self) -> None:
        if self.__openNutrientCondition():
            self._context.setState(Mix())
            return

        if self.__morningPumpCondition():
            self._context.setState(MorningPumpOn())
            return

        if self.__eveningPumpCondition():
            self._context.setState(EveningPumpOn())

    def applyState(self) -> None:
        return # do nothing

    def ceaseState(self) -> None:
        return # do nothing