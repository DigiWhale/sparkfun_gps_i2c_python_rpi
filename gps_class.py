import smbus2
import time
import pynmea2
import os

class GPS:
    def __init__(self, device_address=0x42, i2c_bus=1):
        self.I2C_BUS = i2c_bus
        self.DEVICE_ADDRESS = device_address
        self.reset_variables()
        
    def reset_variables(self):
        self.num_messages = {}
        self.num_sv_in_view = {}
        self.sv_prn_nums = {}
        self.elevation_degs = {}
        self.azimuths = {}
        self.snrs = {}
        self.latitude = None
        self.latitude_direction = None
        self.longitude = None
        self.longitude_direction = None
        self.timestamp = None
        self.status = None
        self.faa_mode = None
        self.speed_over_ground = None
        self.true_course = None
        self.datestamp = None
        self.mag_variation = None
        self.mag_var_dir = None
        self.mode_indicator = None
        self.nav_status = None
        self.gps_qual = None
        self.num_sats = None
        self.horizontal_dil = None
        self.altitude = None
        self.altitude_units = None
        self.geo_sep = None
        self.geo_sep_units = None
        self.age_gps_data = None
        self.ref_station_id = None
        self.mode = None
        self.mode_fix_type = None
        self.sv_ids = {}
        self.pdop = None
        self.hdop = None
        self.vdop = None
        
    def print_variables(self):
        os.system('clear')
        for name, value in vars(self).items():
            print(f"{name}: {value}")

    def read_from_device(self):
        with smbus2.SMBus(self.I2C_BUS) as bus:
            try:
                high, low = bus.read_i2c_block_data(self.DEVICE_ADDRESS, 0xFD, 2)
                message_length = (high << 8) | low
                print(f"Available message length: {message_length}")

                message = []
                while message_length > 0:
                    read_length = min(message_length, 32)  # Maximum of 32 bytes per read
                    part = bus.read_i2c_block_data(self.DEVICE_ADDRESS, 0xFF, read_length)
                    message.extend(part)
                    message_length -= read_length

                # Convert the read bytes to ASCII characters
                raw_message = ''.join(chr(byte) for byte in message)

                # Split the string by the NMEA sentence delimiter.
                nmea_sentences = raw_message.split('\r\n')

                # Process valid NMEA sentences
                self.parse_and_set_variables(nmea_sentences)

            except Exception as e:
                print(f"An error occurred: {e}")

    def parse_and_set_variables(self, nmea_sentences):
        # Similar to previous explanation
        for sentence in nmea_sentences:
            if sentence.startswith('$'):
                try:
                    msg = pynmea2.parse(sentence)
                    self.process_message(msg)
                except pynmea2.ParseError as e:
                    print(f"Could not parse NMEA sentence: {sentence}. Error: {e}")

    def process_message(self, msg):
        if isinstance(msg, pynmea2.GGA):
            self.latitude = msg.latitude
            self.longitude = msg.longitude
            self.timestamp = msg.timestamp
            self.gps_qual = msg.gps_qual
            self.num_sats = msg.num_sats
            self.horizontal_dil = msg.horizontal_dil
            self.altitude = msg.altitude
            self.geo_sep = msg.geo_sep
        elif isinstance(msg, pynmea2.GSV):
            key = f"{msg.msg_num}_{msg.num_messages}"
            self.num_messages[key] = msg.num_messages
            self.num_sv_in_view[key] = msg.num_sv_in_view
            self.sv_prn_nums[key] = [msg.sv_prn_num_1, msg.sv_prn_num_2, msg.sv_prn_num_3, msg.sv_prn_num_4]
            self.elevation_degs[key] = [msg.elevation_deg_1, msg.elevation_deg_2, msg.elevation_deg_3, msg.elevation_deg_4]
            self.azimuths[key] = [msg.azimuth_1, msg.azimuth_2, msg.azimuth_3, msg.azimuth_4]
            self.snrs[key] = [msg.snr_1, msg.snr_2, msg.snr_3, msg.snr_4]
        elif isinstance(msg, pynmea2.GLL):
            self.latitude = msg.latitude
            self.latitude_direction = msg.lat_dir
            self.longitude = msg.longitude
            self.longitude_direction = msg.lon_dir
            self.timestamp = msg.timestamp
            self.status = msg.status
            self.faa_mode = msg.faa_mode
        elif isinstance(msg, pynmea2.RMC):
            self.timestamp = msg.timestamp
            self.status = msg.status
            self.latitude = msg.latitude
            self.latitude_direction = msg.lat_dir
            self.longitude = msg.longitude
            self.longitude_direction = msg.lon_dir
            self.speed_over_ground = msg.spd_over_grnd
            self.true_course = msg.true_course
            self.datestamp = msg.datestamp
            self.mag_variation = msg.mag_variation
            self.mag_var_dir = msg.mag_var_dir
            self.mode_indicator = msg.mode_indicator
            self.nav_status = msg.nav_status
        elif isinstance(msg, pynmea2.VTG):
            self.true_course = msg.true_track
            self.speed_over_ground = msg.spd_over_grnd_kmph
        elif isinstance(msg, pynmea2.GSA):
            key = msg.mode_fix_type
            self.mode = msg.mode
            self.mode_fix_type = msg.mode_fix_type
            self.sv_ids[key] = [msg.sv_id01, msg.sv_id02, msg.sv_id03, msg.sv_id04, msg.sv_id05, msg.sv_id06, msg.sv_id07, msg.sv_id08, msg.sv_id09, msg.sv_id10, msg.sv_id11, msg.sv_id12]
            self.pdop = msg.pdop
            self.hdop = msg.hdop
            self.vdop = msg.vdop

    def main_loop(self):
        print("Starting to read from the GPS module.")
        try:
            while True:
                self.read_from_device()
                time.sleep(.5)  # Adjust sleep time as needed
                self.print_variables()
        except KeyboardInterrupt:
            print("Stopping the data read loop.")

if __name__ == "__main__":
    gps = GPS()
    gps.main_loop()
