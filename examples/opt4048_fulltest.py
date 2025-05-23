# SPDX-FileCopyrightText: Copyright (c) 2025 Tim C for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
from time import sleep

import board

from adafruit_opt4048 import (
    OPT4048,
    OPT4048_FLAG_CONVERSION_READY,
    OPT4048_FLAG_H,
    OPT4048_FLAG_L,
    OPT4048_FLAG_OVERLOAD,
    ConversionTime,
    FaultCount,
    IntConfig,
    Mode,
    Range,
)

READ_INTERVAL = 0.1  # seconds

print("Adafruit OPT4048 Tristimulus XYZ Color Sensor Test")

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = OPT4048(i2c)

print("OPT4048 sensor found!")

low_threshold_val = 1000
print(f"Setting low threshold to: {low_threshold_val}")
sensor.threshold_low = low_threshold_val

high_threshold_val = 10000
print(f"Setting high threshold to: {high_threshold_val}")
sensor.threshold_high = high_threshold_val

print(f"Read back low threshold: {sensor.threshold_low}")
print(f"Read back high threshold: {sensor.threshold_high}")

print("\nEnabling Quick Wake feature...")
sensor.qick_wake = True
print(f"Quick Wake status: {sensor.quick_wake}")

# Set range to auto
print("\nSetting range to Auto...")
sensor.range = Range.AUTO
time.sleep(0.1)
# Read back range setting
print(f"Current range setting value: {sensor.range} name: {Range.get_name(sensor.range)}")

# Set conversion time to 100ms
print("\nSetting conversion time to 100ms...")
sensor.conversion_time = ConversionTime.TIME_100MS

# Read back conversion time setting
print(
    f"Current conversion time setting value: {sensor.conversion_time} "
    + f"name: {ConversionTime.get_name(sensor.conversion_time)}"
)

# Set operating mode to continuous
print(f"\nSetting operating mode to Continuous...")
sensor.mode = Mode.CONTINUOUS
print(f"Current operating mode value: {sensor.mode} name: {Mode.get_name(sensor.mode)}")

# Configure interrupt settings
print("\nConfiguring interrupt settings...")
sensor.interrupt_latch = True
sensor.interrupt_polarity = True
print(f"Interrupt latch mode: {'Latched' if sensor.interrupt_latch else 'Transparent'}")
print(f"Interrupt polarity: {'Active-high' if sensor.interrupt_polarity else 'Active-low'}")

print("\nSetting fault count to 4 consecutive faults...")
sensor.fault_count = FaultCount.COUNT_4
print(
    f"Fault count setting value: {sensor.fault_count} "
    + f"name: {FaultCount.get_name(sensor.fault_count)}"
)

print("\nSetting threshold channel to Channel 1 (Y)...")
sensor.threshold_channel = 1
channels = {
    0: "(X)",
    1: "(Y)",
    2: "(Z)",
    3: "(W)",
}
print(f"Threshold channel setting: Channel {channels[sensor.threshold_channel]}")

print("\nSetting interrupt configuration to data ready for all channels...")
sensor.interrupt_config = IntConfig.DATA_READY_ALL
print(
    f"Interrupt configuration value: {sensor.interrupt_config} "
    + f"name: {IntConfig.get_name(sensor.interrupt_config)}"
)

while True:
    try:
        # Read all four channels from the sensor (raw ADC values)
        x, y, z, w = sensor.get_channels_raw()

        print("Channel readings (raw values):")
        print(f"X (CH0): {x}")
        print(f"Y (CH1): {y}")
        print(f"Z (CH2): {z}")
        print(f"W (CH3): {w}")

        # Calculate and display CIE chromaticity coordinates and lux
        CIEx, CIEy, lux = sensor.get_cie()
        print("\nCIE Coordinates:")
        print(f"CIE x: {CIEx}")
        print(f"CIE y: {CIEy}")
        print(f"Lux: {lux}")

        # Calculate and display color temperature
        color_temp = sensor.calculate_color_temperature(CIEx, CIEy)
        print(f"Color Temperature: {color_temp} K")

        # Read and print status flags
        flags = sensor.flags
        print("\nStatus Flags:")
        if flags & OPT4048_FLAG_L:
            print("- Measurement below low threshold")
        if flags & OPT4048_FLAG_H:
            print("- Measurement above high threshold")
        if flags & OPT4048_FLAG_CONVERSION_READY:
            print("- Conversion complete")
        if flags & OPT4048_FLAG_OVERLOAD:
            print("- Overflow condition detected")
        if flags == 0:
            print("- No flags set")

    except RuntimeError:
        print("Error reading sensor data")

    time.sleep(1)
