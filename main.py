import serial
import time
import HuanyangDev

# PD001: 0
# PD002: 0
# PD163: 1
# PD164: 2
# PD165: 3
# PD003 to change frequency from 0 to 50 Hz (0 to 5000 bc of .00 precion)


dev = HuanyangDev.HuanyangDev({
    "port": "/dev/tty.usbserial-B00326DN", 
    "rate": 19200, 
    "parity": serial.PARITY_NONE, 
    "address": 1, 
    "timeout": 0.1
    })
dev.open()

dev.write_function_data(3, 300)

for i in range(1, 15):
    print(f"PD00{i} = {dev.read_function_data(i)}")


while True:
    freq = input('frequency (0 - 50 Hz): ')

    if freq == 'q':
        dev.write_function_data(24, 1)
        break

    freq = int(freq)*100

    dev.write_function_data(3, freq)

# 0: target frequency
# 1: output frequency
# 2:output current
# 3: rpm
# 4: DC voltage
# 5: AC voltage
# 6:cont
# 7:temp

#f1, f2 = dev.read_control_data(0), dev.read_control_data(1)
#print("target frequency = {}   output frequency = {}".format(f1, f2))


dev.close()
