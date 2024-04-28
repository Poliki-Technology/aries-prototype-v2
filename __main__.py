import state_pattern.context as context
import state_pattern.states as states
from dotenv import load_dotenv
import time

load_dotenv()

mainContext = context.Context(states.Yellow())

while True:
  mainContext.taskLoop()
  time.sleep(0.5)