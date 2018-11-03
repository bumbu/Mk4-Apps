""" <your description>
"""
___title___        = "Home status"
___license___      = "MIT"
___dependencies___ = ["dialogs", "ugfx_helper", "app", "sleep"]
___categories___   = ["Homescreens"]
___bootstrapped___ = False # Whether or not apps get downloaded on first install. Defaults to "False", mostly likely you won't have to use this at all.


import ugfx, ugfx_helper, sleep
from tilda import Sensors, Buttons
from app import *
from dialogs import *
from homescreen import *
import time

ugfx_helper.init()
# time_window = 600 # 10 minutes
time_window = 1 # 1 second
array_temp = [0]
array_hum = []
current_temp = (time.time() // time_window, 0, 0) # sum of all values from this window, number of values

def log_temperature(temp):
  global current_temp
  window_index = time.time() // time_window

  if current_temp[0] == window_index:
    current_temp = (window_index, current_temp[1] + temp, current_temp[2] + 1)
    array_temp[len(array_temp) - 1] = current_temp[1] / current_temp[2]
  else:
    array_temp.append(temp)
    current_temp = (window_index, temp, 1)

  # Remove if too many
  if len(array_temp) > ugfx.width():
    array_temp.pop(0)

# Background stuff
ugfx.backlight(0)
ugfx.clear(ugfx.html_color(0x000000))

# Colour stuff
style = ugfx.Style()
style.set_enabled([ugfx.RED, ugfx.html_color(0x000000), ugfx.html_color(0x000000), ugfx.html_color(0x000000)])
style.set_background(ugfx.html_color(0x000000))
ugfx.set_default_style(style)

# Draw vertical normal
ugfx.orientation(270)

# Temperature
ugfx.set_default_font(ugfx.FONT_TITLE)
temperatureLabel = ugfx.Label(0, ugfx.height() - 60, ugfx.width() // 2, 60, "loading...", justification=ugfx.Label.CENTER)

# Humidity
ugfx.set_default_font(ugfx.FONT_TITLE)
humidityLabel = ugfx.Label(ugfx.width() // 2, ugfx.height() - 60, ugfx.width() // 2, 60, "loading...", justification=ugfx.Label.CENTER)

# ugfx.area(0, 0, 1, 1, ugfx.RED) # left, top, width, height

# update loop
while True:
  # temperature
  temp_cal =  Sensors.get_tmp_temperature()-6
  string_temp = "%.1f C" % temp_cal
  temperatureLabel.text(string_temp)
  log_temperature(temp_cal)

  # humidity
  hum =  Sensors.get_hdc_humidity()
  string_hum = "%.1f %%" % hum
  humidityLabel.text(string_hum)

  # temperature chart
  temp_min = min(array_temp)
  temp_max = max(array_temp)
  temp_range = temp_max - temp_min
  if temp_range <= 0:
    temp_range = 1
  # temp from 0 to 200px
  chart_min = 0
  chart_max = 200
  ugfx.area(0, 0, ugfx.width(), chart_max, ugfx.BLACK) # clean chart
  # print(temp_min, temp_max, temp_range)
  for index, temp in enumerate(array_temp):
    ugfx.area(int(index), chart_max - int((temp-temp_min)/temp_range*chart_max), 1, 1, ugfx.RED)

  # if len(array_temp) % 10 > 4:
  #   ugfx.power_mode(ugfx.POWER_DEEP_SLEEP)
  #   ugfx.backlight(0)
  # else:
  #   ugfx.power_mode(ugfx.POWER_ON)

  sleep_or_exit(0.5)
