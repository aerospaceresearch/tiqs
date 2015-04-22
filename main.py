'''
This TIQS!
Let's find a needle in a haystack, an radio-frequency haystack with sampled i/q data.

thank you for reading my /code/. I know it's crap, but I still figure out how to do signal processing.
Each day, I learn more with your help! So thank you for your help and feel free to change parts to make it work
- Andreas, www.AerospaceResearch.net
'''

import tiqs
import matplotlib.pyplot as plt
import numpy as np

samplerate = 2048000

filename = ["ofdm_178mhz", "ofdm_208mhz", "ofdm_218mhz"]
filepath = "h:/"

for file in filename:
    if file.find(".wav"):
        stream = np.memmap(filepath+file, dtype=np.uint8, mode='r', offset=44)
    else:
        stream = np.fromfile(open(filepath+file, mode="rb"), dtype=np.uint8)

    offset = 0
    stream_chunk = stream[offset:offset+samplerate*2]

    stream_iq = tiqs.bin_to_complex(stream_chunk)
    stream_iq -= np.ones_like(stream_iq) * complex(127, 127)
    stream_iq = np.abs(stream_iq)

    stream_binned = tiqs.mean_to_bins(stream_iq, 60)
    stream_binned_gaps = tiqs.find_gaps(stream_binned)
    stream_binned_gaps1 = tiqs.gap_grower(stream_binned_gaps, 3)
    stream_binned_gaps2 = tiqs.gap_resetter(stream_binned_gaps1, 20)

    gap_length = tiqs.gap_length_counter(stream_binned_gaps2)
    gap_period = tiqs.gap_period_counter(stream_binned_gaps2)

    plt.plot(stream_binned)
    plt.plot(stream_binned_gaps2)
    plt.show()