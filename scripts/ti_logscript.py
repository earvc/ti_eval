import sys
import re
import matplotlib.pyplot as plt

# Constants
ATOD_VREF = 2.5
ATOD_RANGE = 512
MIN_ATOD_VAL = 500
TIME_INTERVAL = 5  # seconds

# function to convert from raw atod to voltage
def atod_to_volts(atod):
    return ((float(atod) * ATOD_VREF) / float(ATOD_RANGE))

# open data file for reading
fh = open(sys.argv[1], "r")

# data list
data = []
x_axis = []

# plot index
idx = float(0.0)

# loop to grab voltage line by line
for line in fh.readlines():
    m = re.match(r'.*Temp:(\d+)@@.*', line)
    x_axis.append(float(idx/60))
    
    if m.groups(0) > MIN_ATOD_VAL:
        data.append(atod_to_volts(m.groups(0)[0]))
        idx = idx + TIME_INTERVAL

plt.xlabel('Time (min)')
plt.ylabel('Voltage (V)')
plt.title('Voltage vs. Time @ %(time_int)d second Packet Interval'   %
        {'time_int':TIME_INTERVAL})

plt.plot(x_axis, data)
plt.show()

fh.close()
