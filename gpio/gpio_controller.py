import yaml
import sys
import time
import os
import RPi.GPIO as GPIO


class GpioController:
  __input_ports = []
  __output_ports = []

  def __check_config(self, cfg):
    result = True
    if len(cfg["output"]) != len(self.__output_ports) or len(cfg["input"]) != len(self.__input_ports):
      result = False
    for i in range(len(self.__output_ports)):
      result = result and int(cfg["output"][i]) > 0 and int(cfg["output"][i]) < 40
    for i in range(len(self.__input_ports)):
      result = result and int(cfg["input"][i]) > 0 and int(cfg["input"][i]) < 40
    return result

  def __import_project_config(self):
    gpio = None
    with open('gpio/gpio_config.yml', 'r') as file:
      config = yaml.safe_load(file)
      gpio = config["gpio"]
    self.__input_ports = [-1] * gpio["input_ports"]
    self.__output_ports = [-1] * gpio["output_ports"]
    return

  def __parse_check_env_config(self):
    input_ports = os.getenv('INPUT_PORTS')
    output_ports = os.getenv('OUTPUT_PORTS')
    cfg = {
      "input": input_ports.split(' '),
      "output": output_ports.split(' ')
    }
    if not self.__check_config(cfg):
      sys.exit("GPIO is configured incorrectly. Please check 'config.yml'. Halting script...")
    self.__input_ports = [int(i) for i in cfg["input"]]
    self.__output_ports = [int(i) for i in cfg["output"]]
    for port in self.__input_ports:
      GPIO.setup(port, GPIO.IN)
    for port in self.__output_ports:
      GPIO.setup(port, GPIO.OUT)
    return

  def __init__(self) -> None:
    self.__import_project_config()
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    self.__parse_check_env_config()
    return

  def __get_raw_input(self, input_gate):
    return GPIO.input(self.__input_ports[input_gate - 1])

  def get_input(self, input_gate, signal_counts = 5, delay = 0.01):
    result = 0
    for _ in range(signal_counts):
      result += self.__get_raw_input(input_gate)
      time.sleep(delay)
    return result * 2 > signal_counts

  def post_output(self, output_gate, signal):
    GPIO.output(self.__output_ports[output_gate - 1], signal)
