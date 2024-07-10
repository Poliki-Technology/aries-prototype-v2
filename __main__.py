import state_pattern.context as context
from state_pattern.states.idle import Idle
from dotenv import load_dotenv
import time

load_dotenv()

mainContext = context.Context(Idle())

while True:
  mainContext.taskLoop()
  time.sleep(0.1)
