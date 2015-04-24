'''
This TIQS!
Let's find a needle in a haystack, an radio-frequency haystack with sampled i/q data.

thank you for reading my /code/. I know it's crap, but I still figure out how to do signal processing.
Each day, I learn more with your help! So thank you for your help and feel free to change parts to make it work
- Andreas, www.AerospaceResearch.net
'''

import tiqs
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

    gap_length_mean, gap_period_max, gap_period_mean, gap_period_count_max, gap_tendency = tiqs.detect_null_symbols(stream_iq, samplerate)
    print "average gap length is", gap_length_mean,"with a best period of",gap_period_max,"and an average of", gap_period_mean,"with", gap_period_count_max,"periods leading to a dab liklyhood of", gap_tendency