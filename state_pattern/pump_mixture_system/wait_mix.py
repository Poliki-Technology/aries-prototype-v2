from state_pattern.pump_mixture_system.i_state import IState
import state_pattern.pump_mixture_system.mix_states as mix
from datetime import datetime, timedelta

class WaitMix(IState):
    __stateTimestamp = 0
    def __changeStateCondition(self) -> bool:
        return datetime.now() - self.__stateTimestamp >= timedelta(minutes=3)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(mix.BeginMix())

    def applyState(self) -> None:
        self.__stateTimestamp = datetime.now()
        return

    def ceaseState(self) -> None:
        return # do nothing
