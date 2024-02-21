
# GPS Data Reader for Raspberry Pi

This Python script is designed to interface with a GPS module via the I2C protocol on a Raspberry Pi. It reads NMEA sentences from the GPS module, parses them, and extracts various pieces of information such as location, speed, and satellite data. The script then makes this information available through class variables.

## Prerequisites

- Python 3.x installed on your Raspberry Pi
- `smbus2` and `pynmea2` libraries installed. You can install these using pip:

```bash
pip install smbus2 pynmea2
```

- A GPS module that supports NMEA sentences over I2C connected to your Raspberry Pi.

## Running the Script

To run the script, navigate to the directory containing the `gps.py` file in your terminal and execute:

```bash
python gps.py
```

## How It Works

The script defines a `GPS` class with methods for reading data from the GPS module, parsing the data, and setting class variables based on the parsed information.

### Class Initialization

The `GPS` class is initialized with the device address of the GPS module and the I2C bus number. These can be customized if different from the default settings.

### Reading from the Device

The `read_from_device` method reads raw NMEA sentences from the GPS module, splits them into individual sentences, and passes each one to the `parse_and_set_variables` method for parsing.

### Parsing NMEA Sentences

The `parse_and_set_variables` method uses the `pynmea2` library to parse NMEA sentences. Depending on the sentence type, it extracts relevant information like latitude, longitude, altitude, number of satellites, etc., and sets them as class variables.

### Available Data Points

The class variables include but are not limited to:
- Latitude and longitude
- Number of satellites in view
- Altitude
- Speed over ground
- GPS quality indicator
- Timestamps
- Magnetic variation

### Utility Methods

The class also includes a `print_variables` method to clear the terminal and print all current class variables, providing a real-time overview of the parsed GPS data.

## Customization

You can extend the functionality of the `GPS` class by adding more parsing logic for additional NMEA sentence types or by incorporating more advanced GPS features.

## Stopping the Script

The script runs in a continuous loop, reading and parsing GPS data. To stop it, simply press `CTRL+C` in the terminal.

