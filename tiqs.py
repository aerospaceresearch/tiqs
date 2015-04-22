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
    counter = 0
    for i in range(1,len(x)):
        if x[i] == 1 and x[i-1] == 1:
            counter += 1
        else:
            if counter > 0:
                print "gap length =", counter
            counter = 0
    return counter

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
        print "gap period", gap_start[i] - gap_start[i-1]
        gap_period.append(gap_start[i] - gap_start[i-1])
    return gap_period