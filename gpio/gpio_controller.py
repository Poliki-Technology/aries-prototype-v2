import yaml
import sys
import time
import os
import RPi.GPIO as GPIO

class GpioController:
  __input_ports = []
  __output_ports = []
  __input_invert = []
  __output_invert = []

  def __check_config(self, cfg):
    result = len(cfg["output_ports"]) == len(self.__output_ports)
    result = len(cfg["input_ports"]) == len(self.__input_ports) and result
    result = len(cfg["output_invert"]) == len(self.__output_ports) and result
    result = len(cfg["input_invert"]) == len(self.__input_ports) and result
    for i in range(len(self.__output_ports)):
      result = result and int(cfg["output_ports"][i]) > 0 and int(cfg["output_ports"][i]) < 40
    for i in range(len(self.__input_ports)):
      result = result and int(cfg["input_ports"][i]) > 0 and int(cfg["input_ports"][i]) < 40
    return result

  def __import_project_config(self):
    gpio = None
    with open('gpio/gpio_config.yml', 'r') as file:
      config = yaml.safe_load(file)
      gpio = config["gpio"]
    self.__input_ports = [-1] * gpio["input_ports"]
    self.__output_ports = [-1] * gpio["output_ports"]
    self.__input_invert = [False] * gpio["input_ports"]
    self.__output_invert = [False] * gpio["output_ports"]
    return

  def __parse_check_env_config(self):
    input_ports = os.getenv('INPUT_PORTS')
    output_ports = os.getenv('OUTPUT_PORTS')
    input_invert = os.getenv('INPUT_INVERT')
    output_invert = os.getenv('OUTPUT_INVERT')
    cfg = {
      "input_ports": input_ports.split(' '),
      "output_ports": output_ports.split(' '),
      "input_invert": input_invert.split(' '),
      "output_invert": output_invert.split(' ')
    }
    if not self.__check_config(cfg):
      sys.exit("GPIO is configured incorrectly. Please check 'config.yml'. Halting script...")
    self.__input_ports = [int(i) for i in cfg["input_ports"]]
    self.__output_ports = [int(i) for i in cfg["output_ports"]]
    self.__input_invert = [bool(int(i)) for i in cfg["input_invert"]]
    self.__output_invert = [bool(int(i)) for i in cfg["output_invert"]]
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
    return bool(GPIO.input(self.__input_ports[input_gate - 1])) != bool(self.__input_invert[input_gate - 1])

  def get_input(self, input_gate, signal_counts = 5, delay = 0.01):
    print(f"GPIO:\treading input from {input_gate} {signal_counts} times.")
    result = 0
    for _ in range(signal_counts):
      result += self.__get_raw_input(input_gate)
      time.sleep(delay)
    return result * 2 > signal_counts

  def post_output(self, output_gate, signal):
    print(f"GPIO:\tset {output_gate} to {signal}.")
    GPIO.output(self.__output_ports[output_gate - 1], bool(signal) != bool(self.__output_invert[output_gate - 1]))
