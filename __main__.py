import state_pattern.context as context
from state_pattern.pump_mixture_system.idle import Idle
from state_pattern.nightlight.states import LightOff
from dotenv import load_dotenv
import time

load_dotenv()

pumpMixtureContext = context.Context(Idle())
nightLightContext = context.Context(LightOff())

while True:
  pumpMixtureContext.taskLoop()
  nightLightContext.taskLoop()
  time.sleep(0.1)
