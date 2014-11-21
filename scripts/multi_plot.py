import sys
import re
import matplotlib.pyplot as plt

# Constants
ATOD_VREF = 2.5
ATOD_RANGE = 512
MIN_ATOD_VAL = 500
TIME_INTERVAL = 1  # seconds


# class and helper function defs
class data_obj:
    def __init__(self, fh, interval):
        self.fh = fh  
        self.interval = interval
        self.x_axis = []
        self.data = []
    
def atod_to_volts(atod):
    return ((float(atod) * ATOD_VREF) / float(ATOD_RANGE))

def plot_traces(data_list):
    plt.xlabel('Transmission count')
    plt.ylabel('Voltage (V)')
    plt.title('Voltage vs. Transmission Count')
    
    for dobj in data_list:
        plt.plot(dobj.x_axis, dobj.data, label=dobj.interval)

    plt.legend()

    plt.show()

def get_trans_interval(filename):
    m = re.match(r'.*_(\d+)S', filename)
    label = m.groups(0)[0] + "s"
    return label

# global vars
data_list = []  # stores data objects from each file
fh_list = []    # keeps track of file handlers for each file
num_files = 0   # counter for number of files

# open files and create data objects
for i in range(0, len(sys.argv) - 1):
    filename = sys.argv[i+1]
    fh_list.append(open(filename, "r"))
    data_list.append(data_obj(fh_list[i], get_trans_interval(filename)))
    num_files = num_files + 1

# read data from the files
for j in range(0, num_files):
    trans_cnt = 0
    for line in fh_list[j]:
        pass;
        m = re.match(r'.*Battery:(\d+),.*', line)
        data_list[j].x_axis.append(trans_cnt)
        
        if m.groups(0) > MIN_ATOD_VAL:
            data_list[j].data.append(atod_to_volts(m.groups(0)[0]))
            trans_cnt = trans_cnt + TIME_INTERVAL


plot_traces(data_list)

# close all files
for fh in fh_list:
    fh.close()
