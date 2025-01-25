import serial
import time
import HuanyangDev




def printHelpDiagnostics():
   print(
       "The registers you can set are PD003 (main frequency), PD008 (max voltage), PD009 (intermediate voltage), and PD010 (min voltage)")
   print("An example command is: PD008 2000")
   print("------EXPLANATION OF REGISTERS-----")
   print(
       "[PD003: Main Frequency]: Set Range: 0.00-400.00 Hz. Unit: 0.01 Hz. Can not be set higher than the max. frequency")
   print(
       "[PD008: Main Voltage]: Set Range: 0.1-* Unit: 0.1 V. Can not be set higher than the max. physical voltage of the inverter")
   print(
       "[PD009: Intermediate Voltage]: Set Range: 0.1-500.0V Unit: 0.1 V. Can not be set higher than the max. voltage (PD008). [NOTE: if this is increased too quickly, it can cause tripping of the inverter or damage of the machine]")
   print(
       "[PD010: Min Voltage]: Set Range: 0.1-50.0V Unit: 0.1V. [NOTE: don't change too rapidly]")
   print("")







dev = HuanyangDev.HuanyangDev({"port": "/dev/tty.usbserial-B00326DN", "rate": 9600, "parity": serial.PARITY_NONE, "address": 1, "timeout": 0.1})

dev.open()

# 0: target frequency,  1: output frequency, 2:output current, 3: rpm, 4: DC voltage, 5: AC voltage,6:cont, 7:temp
f1, f2, f3, f4, f5, f6, f7, f8 = dev.read_control_data(0), dev.read_control_data(1), dev.read_control_data(2), dev.read_control_data(3), dev.read_control_data(4), dev.read_control_data(5), dev.read_control_data(6), dev.read_control_data(7)
print("-----------------------------------------------------------------------")
print("target frequency = {}   output frequency = {}   output current = {}   rpm = {}   DC voltage = {}    AC voltage = {}    cont = {}    temp = {}".format(f1, f2, f3, f4, f5, f6, f7, f8))
print("-----------------------------------------------------------------------")

dev.open()
if dev.conn.is_open:
    print("Connection successfully opened.")
else:
    print("Failed to open connection.")

inp = ""
while True:
   inp = input('(input as [Register] [Value]. see HELP for more details. type QUIT to quit): ')
   if inp.upper() == "Q" or inp.upper() == "QUIT":
       break
   if len(inp.split()) > 2:
       print('     Error: Too many inputs')
       continue
   reg = inp.split()[0]
   if reg.upper() == "HELP":
       printHelpDiagnostics()
   elif reg.upper() == "PD003":
       print("     ...changing main frequency...")
       val = float(inp.split()[1])
       sendVal = int(val*100)
       dev.write_function_data(3, sendVal)
       pd003 = dev.read_function_data(3)
       print("     PD003 = {}".format(pd003))
       dev.write_control_data(0x03)  # stop
   elif reg.upper() == "PD008":
       print("     ...changing max voltage...")
       val = float(inp.split()[1])
       sendVal = int(val * 10)
       dev.write_function_data(8, sendVal)
       pd008 = dev.read_function_data(8)
       print("     PD008 = {}".format(pd008))
       dev.write_control_data(0x08)  # stop
   elif reg.upper() == "PD009":
       print("     ...changing intermediate voltage...")
       val = float(inp.split()[1])
       sendVal = int(val * 10)
       dev.write_function_data(9, sendVal)
       pd009 = dev.read_function_data(9)
       print("     PD009 = {}".format(pd009))
       dev.write_control_data(0x09)  # stop
   elif reg.upper() == "PD010":
       print("     ...changing min voltage...")
       val = float(inp.split()[1])
       sendVal = int(val * 10)
       dev.write_function_data(10, sendVal)
       pd010 = dev.read_function_data(10)
       print("     PD010 = {}".format(pd010))
       dev.write_control_data(0x0a)  # stop
   else:
       print("     Error: Invalid register")
       continue

dev.close()
