import os
from datetime import datetime

OFFSET_ALLOWED = 60

class Scheduler():
  scheduler = {}

  def __init__(self):
    self.scheduler = {
      "morning": {
        "minute": int(os.getenv('MORNING_MINUTE')) or 31,
        "first_hour": int(os.getenv("MORNING_FIRST_HR")) or 6,
        "last_hour": int(os.getenv("MORNING_LAST_HR")) or 16,
      },
      "evening": {
        "minute": int(os.getenv('EVENING_MINUTE')) or 1,
        "first_hour": int(os.getenv("EVENING_FIRST_HR")) or 17,
        "last_hour": int(os.getenv("EVENING_LAST_HR")) or 23,
      }
    }

  def is_morning_pump_schedule(self):
    tstamp = datetime.now()
    s_morning = self.scheduler["morning"]
    if tstamp.hour < s_morning["first_hour"] or tstamp.hour > s_morning["last_hour"]:
      return False

    seconds_passed = tstamp.minute * 60 + tstamp.second
    target = s_morning["minute"] * 60
    return target - OFFSET_ALLOWED <= seconds_passed <= target + OFFSET_ALLOWED

  def is_evening_pump_schedule(self):
    tstamp = datetime.now()
    s_evening = self.scheduler["evening"]
    if tstamp.hour < s_evening["first_hour"] or tstamp.hour > s_evening["last_hour"]:
      return False

    seconds_passed = tstamp.minute * 60 + tstamp.second
    target = s_evening["minute"] * 60
    return target - OFFSET_ALLOWED <= seconds_passed <= target + OFFSET_ALLOWED
