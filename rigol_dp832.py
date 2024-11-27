import pyvisa
import time
import sys


def main():
    rm = pyvisa.ResourceManager()

    # List available resources (use this to find your Rigol DP832's resource string)
    # print(rm.list_resources())

    # Replace this with your Rigol DP832's resource string
    resource_string = "USB0::6833::3601::DP8C269M00413::0::INSTR"
    dp832 = rm.open_resource(resource_string)

    print(dp832.query("*IDN?"))  # Get instrument identification

    mode = "print"
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "on":
            mode = "on"
        elif sys.argv[1].lower() == "off":
            mode = "off"
        elif sys.argv[1].lower() == "monitor":
            mode = "monitor"
        else:
            print("usage: rigol_dp832.py [on|off|monitor]")
            return

    if mode == "on":
        # Set voltage and current for each channel
        dp832.write(":APPL CH1,12,3")
        dp832.write(":APPL CH2,12,3")
        dp832.write(":APPL CH3,5,3")

        # Set overcurrent protection for each channel
        dp832.write(":OUTP:OCP:VAL CH1,2")
        dp832.write(":OUTP:OCP:STAT CH1,ON")

        dp832.write(":OUTP:OCP:VAL CH2,2")
        dp832.write(":OUTP:OCP:STAT CH2,ON")

        dp832.write(":OUTP:OCP:VAL CH3,2")
        dp832.write(":OUTP:OCP:STAT CH3,ON")

        # Turn on the output
        dp832.write(":OUTP CH1,ON")
        dp832.write(":OUTP CH2,ON")
        dp832.write(":OUTP CH3,ON")
    elif mode == "off":
        # Turn off the output
        dp832.write(":OUTP CH1,OFF")
        dp832.write(":OUTP CH2,OFF")
        dp832.write(":OUTP CH3,OFF")

    while True:
        if mode != "print":
            time.sleep(1)

        dp832.write(":MEAS:ALL? CH1")
        vals = dp832.read().strip().split(",")
        print("CH1: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        dp832.write(":MEAS:ALL? CH2")
        vals = dp832.read().strip().split(",")
        print("CH2: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        dp832.write(":MEAS:ALL? CH3")
        vals = dp832.read().strip().split(",")
        print("CH3: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        if mode != "monitor":
            break

        print("")

    dp832.close()  # Close the connection


if __name__ == "__main__":
    main()
