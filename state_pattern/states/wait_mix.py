from state_pattern.states.i_state import IState
from state_pattern.states.mix import Mix
from datetime import datetime, timedelta

class WaitMix(IState):
    __stateTimestamp = 0
    def __changeStateCondition(self) -> bool:
        return datetime.now() - self.__stateTimestamp > timedelta(minutes=2)

    def taskLoop(self) -> None:
        if not self.__changeStateCondition():
            return
        self._context.setState(Mix())

    def applyState(self) -> None:
        self.__stateTimestamp = datetime.now()
        return

    def ceaseState(self) -> None:
        return # do nothing
