from state_pattern.states.i_state import IState
import state_pattern.states.mix as mix
import state_pattern.states.morning_pump_on as morning
import state_pattern.states.evening_pump_on as evening
from scheduling.scheduling import Scheduler

class Idle(IState):
    def __openNutrientCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(3)

    def __morningPumpCondition(self) -> bool:
        return Scheduler().is_morning_pump_schedule()

    def __eveningPumpCondition(self) -> bool:
        return Scheduler().is_evening_pump_schedule()

    def taskLoop(self) -> None:
        if self.__openNutrientCondition():
            self._context.setState(mix.Mix())
            return

        if self.__morningPumpCondition():
            self._context.setState(morning.MorningPumpOn())
            return

        if self.__eveningPumpCondition():
            self._context.setState(evening.EveningPumpOn())

    def applyState(self) -> None:
        return # do nothing

    def ceaseState(self) -> None:
        return # do nothing