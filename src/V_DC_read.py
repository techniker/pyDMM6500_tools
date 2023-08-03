# Simple tool for talking to the Keithley DMM6500 via SCPI and get the DC V reading
# Bjoern Heller <tec(att)sixtopia.net>

import pyvisa
import time

def read_dc_voltage():
    # Replace 'TCPIP0::192.168.1.100::inst0::INSTR' with your instrument's VISA resource string
    # This example assumes the DMM6500 is connected over Ethernet, adjust the resource string accordingly.
    resource_str = 'TCPIP0::10.36.0.5::inst0::INSTR'
    
    try:
        # Initialize the PyVISA library and open the instrument connection
        rm = pyvisa.ResourceManager()
        dmm = rm.open_resource(resource_str)

        # Set up the instrument to measure DC voltage
        dmm.write("CONF:VOLT:DC")
        dmm.write("VOLT:DC:NPLC 10")  # Set the integration time to 10 PLC (Power Line Cycles)

        # Trigger a single measurement and wait for it to complete
        dmm.write("INIT")
        time.sleep(1)  # Adjust the waiting time based on the integration time set above

        # Read the measurement result
        voltage = dmm.query("FETCH?")
        
        # Close the instrument connection
        dmm.close()

        return float(voltage)

    except pyvisa.VisaIOError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    voltage_reading = read_dc_voltage()
    if voltage_reading is not None:
        print(f"DC Voltage reading: {voltage_reading:.6f} V")