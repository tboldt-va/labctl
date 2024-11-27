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
        elif sys.argv[1].lower() == "monitor" or sys.argv[1].lower() == "mon":
            mode = "monitor"
        else:
            print("usage: rigol_dp832.py [on|off|monitor] [1|2|3]")
            return

    channel = [True, True, True]
    if len(sys.argv) > 2:
        if sys.argv[2] == "1":
            channel = [True, False, False]
        elif sys.argv[2] == "2":
            channel = [False, True, False]
        elif sys.argv[2] == "3":
            channel = [False, False, True]
        else:
            print("usage: rigol_dp832.py [on|off|monitor] [1|2|3]")
            return

    if mode == "on":
        if channel[0]:
            # Set voltage and current
            dp832.write(":APPL CH1,12,3")
            # Set overcurrent protection
            dp832.write(":OUTP:OCP:VAL CH1,2")
            dp832.write(":OUTP:OCP:STAT CH1,ON")
            # Turn on the output
            dp832.write(":OUTP CH1,ON")
        if channel[1]:
            dp832.write(":APPL CH2,12,3")
            dp832.write(":OUTP:OCP:VAL CH2,2")
            dp832.write(":OUTP:OCP:STAT CH2,ON")
            dp832.write(":OUTP CH2,ON")
        if channel[2]:
            dp832.write(":APPL CH3,5,3")
            dp832.write(":OUTP:OCP:VAL CH3,2")
            dp832.write(":OUTP:OCP:STAT CH3,ON")
            dp832.write(":OUTP CH3,ON")
    elif mode == "off":
        if channel[0]:
            # Turn off the output
            dp832.write(":OUTP CH1,OFF")
        if channel[1]:
            dp832.write(":OUTP CH2,OFF")
        if channel[2]:
            dp832.write(":OUTP CH3,OFF")

    while True:
        if mode != "print":
            time.sleep(1)

        if channel[0]:
            dp832.write(":MEAS:ALL? CH1")
            vals = dp832.read().strip().split(",")
            print("CH1: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        if channel[1]:
            dp832.write(":MEAS:ALL? CH2")
            vals = dp832.read().strip().split(",")
            print("CH2: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        if channel[2]:
            dp832.write(":MEAS:ALL? CH3")
            vals = dp832.read().strip().split(",")
            print("CH3: ", vals[0], "V, ", vals[1], "A, ", vals[2], "W")

        if mode != "monitor":
            break

        print("")

    dp832.close()  # Close the connection


if __name__ == "__main__":
    main()
