'''
This TIQS!
Let's find a needle in a haystack, an radio-frequency haystack with sampled i/q data.

thank you for reading my /code/. I know it's crap, but I still figure out how to do signal processing.
Each day, I learn more with your help! So thank you for your help and feel free to change parts to make it work
- Andreas, www.AerospaceResearch.net
'''

import numpy as np
from pylab import *

'''
transfering the signal to complex values
'''
def bin_to_complex(x):
    assert len(x)%2 == 0
    return x[::2] + complex(0,1)*x[1::2]

'''
binning all signals.
all signals within a binduration are meaned and put into one bin
'''
def mean_to_bins(x,binduration):
    binned = []
    for i in xrange(len(x)/binduration):
        binned.append(np.mean(x[i*binduration:i*binduration+binduration]))
    return binned

'''
will find a gap where the signal level of one bin in lower than
the level between the minimum signal level of all collected bins
and the mean level of of all bins.
'''
def find_gaps(x):
    binned_min = np.min(x)
    binned_mean = np.mean(x)

    bin_gaps = []
    for bin in x:
        if bin <= (binned_min + binned_mean)/2.0:
            bin_gaps.append(1)
        else:
            bin_gaps.append(0)

    return bin_gaps

'''
will grow the gaps and perhaps merge them if two gaps are very close.
with each iteration, the gap will grow on it's left side
'''
def gap_grower(x, iterating):
    y = x[:]
    for i in range(iterating):
        for i in range(1,len(y)):
            if y[i] == 1:
                y[i-1] = 1
    return y

'''
it will reset found gaps to no-gaps = 0, if the gap lenght is smaller than the minimum
'''
def gap_resetter(x, gap_length_min):
    y = x[:]
    counter = 0
    for i in range(1,len(x)):
        if x[i] == 1 and x[i-1] == 1:
            counter += 1
        else:
            if counter < gap_length_min:
                for j in range(counter+1):
                    y[i-j-2] = 0

            counter = 0
    return y

'''
measuring the length of a gap
'''
def gap_length_counter(x):
    gap_length = []
    counter = 0
    for i in range(1,len(x)):
        if x[i] == 1 and x[i-1] == 1:
            counter += 1
        else:
            if counter > 0:
                gap_length.append(counter)
            counter = 0
    return gap_length

'''
measuring the period between gaps
'''
def gap_period_counter(x):
    gap_start = []
    gap_period = []
    for i in range(1,len(x)):
        if x[i-1] < x[i]:
            gap_start.append(i)

    for i in range(1,len(gap_start)):
        gap_period.append(gap_start[i] - gap_start[i-1])
    return gap_period

def gap_period_stacker(x, spreading):
    gap_period_count = []
    gap_period_stack = []

    for i in range(len(x)):
        if i == 0:
            gap_period_stack.append(x[i])
            gap_period_count.append(1)
        else:
            isstacked = -1
            for j in range(len(gap_period_stack)):
                if x[i] >= gap_period_stack[j] - x[i]*spreading and x[i] <= gap_period_stack[j] + x[i]*spreading:
                    isstacked = j

            if isstacked == -1:
                gap_period_stack.append(x[i])
                gap_period_count.append(1)
            else:
                gap_period_count[isstacked] = gap_period_count[isstacked] + 1

    return gap_period_count, gap_period_stack

def detect_null_symbols(stream_iq, samplerate):
    stream_binned = mean_to_bins(stream_iq, 40)
    stream_binned_gaps = find_gaps(stream_binned)
    stream_binned_gaps1 = gap_grower(stream_binned_gaps, 3)
    stream_binned_gaps2 = gap_resetter(stream_binned_gaps1, 20)

    gap_length = gap_length_counter(stream_binned_gaps2)
    gap_period = gap_period_counter(stream_binned_gaps2)

    # gaps per second, but if not a second or more, it is adapted
    gap_length_mean = 0
    gap_period_max = 0
    gap_period_count_max = 0
    gap_period_mean = 0
    gap_tendency = 0
    if len(gap_length) > 5 * float(len(stream_iq))/samplerate and len(gap_length) < 100 * float(len(stream_iq))/samplerate:
        gap_length_mean = np.mean(gap_length)
        gap_period_count, gap_period_stack = gap_period_stacker(gap_period, 0.01)
        gap_period_count_max = np.max(gap_period_count)
        gap_period_mean = np.mean(gap_period_stack)
        gap_period_max = gap_period_stack[np.argmax(gap_period_count)]
        gap_tendency = float(np.max(gap_period_count))/np.sum(gap_period_count)

    return gap_length_mean, gap_period_max, gap_period_mean, gap_period_count_max, gap_tendency