from state_pattern.pump_mixture_system.i_state import IState
import state_pattern.pump_mixture_system.mix_states as mix
import state_pattern.pump_mixture_system.morning_pump_on as morning
import state_pattern.pump_mixture_system.evening_pump_on as evening
import state_pattern.pump_mixture_system.secondary_pump_on as secondary
from scheduling.scheduling import Scheduler

class Idle(IState):
    def __openNutrientCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(3)

    def __morningPumpCondition(self) -> bool:
        return Scheduler().is_morning_pump_schedule()

    def __eveningPumpCondition(self) -> bool:
        return Scheduler().is_evening_pump_schedule()

    def __secondaryPumpCondition(self) -> bool:
        gpio = self._context.getGpioController()
        return gpio.get_input(4)

    def taskLoop(self) -> None:
        if self.__openNutrientCondition():
            self._context.setState(mix.BeginMix())
            return

        if self.__morningPumpCondition():
            self._context.setState(morning.MorningPumpOn())
            return

        if self.__eveningPumpCondition():
            self._context.setState(evening.EveningPumpOn())

        if self.__secondaryPumpCondition():
            self._context.setState(secondary.SecondaryPumpOn())

    def applyState(self) -> None:
        return # do nothing

    def ceaseState(self) -> None:
        return # do nothing
