''' This TIQS!
Let's find a needle in a haystack, an radio-frequency haystack with sampled i/q data.

thank you for reading my /code/. I know it's crap, but I still figure out how to do cross correlation.
Each day, I learn more with your help! So thank you for your help and feel free to change parts to make it work
- Andreas, www.AerospaceResearch.net

I use those two I/Q files in http://filebin.net/8nevid3yk3

Some sources and my thanks:
* http://nbviewer.ipython.org/urls/www.tablix.org/~avian/stuff/tworecordingsforcorrelation.ipynb
* https://www.reddit.com/r/DSP/comments/2rdxpx/how_to_do_normalized_cross_correlation_with/
* http://forum.db3om.de/ftopic21899.html
'''


import numpy as np

def bin_to_complex(x):
    assert len(x)%2 == 0
    return x[::2] + complex(0,1)*x[1::2]

file_path1 = "d:/tmp/signal1/out1.raw"
file_path2 = "d:/tmp/signal1/out2.raw"

sequence1 = np.fromfile(open(file_path1, mode="rb"), dtype=np.uint8)
haystack = np.array(-127+sequence1[0:4000000], dtype=np.int8)


N_haystack = 20000
n = len(haystack) - len(haystack)%N_haystack
'''print "test", N_haystack, n, n/N_haystack, len(haystack)'''

sequence2 = np.fromfile(open(file_path2, mode="rb"), dtype=np.uint8)
needle = np.array(-127+sequence2[3000000:3000000+2048], dtype=np.int8)

''' preparing the needle '''
N_needle = len(needle)
N_full = N_haystack + (N_needle - 2)*2
''' N_full is filled with the haystack, the overlapping needle (N_needle-2) and the overlapping zeros (N_needle-2) '''

''' filling the needle with zeros to make it ass lon as the haystack counterpart. Otherwise fft won't work '''
needle_zerofilled = np.zeros(N_full)
for i in xrange(N_needle):
    needle_zerofilled[i] = needle[i]

''' converting the i/q sequence to a complex sequence '''
needle_compl = bin_to_complex(needle_zerofilled)

''' preparing the needle for later calculations that will save some computing per iteration '''
needle_conjfft = np.conjugate(np.fft.fft(needle_compl))
needle_norm = np.linalg.norm(needle_compl)
''' this includes the constant length/norm of the sequence. Thus it is prepared once here '''

''' preparing the final normalized cross correlation list '''
haystack_correlated_normed = []


''' now, the full haystack will be processed with correlation ... '''
for i in xrange(n/N_haystack):
    ''' slicing the haystack but with more sampled, due to edge effects '''
    haystack_part = haystack[N_haystack*i:N_haystack*i+N_haystack+(N_needle-2)]


    ''' even though the edge effects were considered, the remaining part could be less long then required
    thus it will be filled with zeros in thes cases '''

    haystack_part_zerofilled = np.zeros(N_full, dtype=complex)
    for j in range(0,len(haystack_part)):
        haystack_part_zerofilled[j] = haystack_part[j]
    haystack_part_compl = bin_to_complex(haystack_part_zerofilled)


    ''' correlating the haystack '''
    haystack_part_correlated = np.fft.ifft(np.fft.fft(haystack_part_compl) * needle_conjfft)

    ''' windowing over the haystack part to create the norm of this window '''
    haystack_part_norm = []
    for j in xrange(N_haystack/2):
        haystack_part_norm.append( (np.linalg.norm(haystack_part_compl[j:j+N_needle/2])) * needle_norm)

    ''' normalizing the correlated haystack '''
    haystack_correlated_normed.append(abs(haystack_part_correlated[0:N_haystack/2])/haystack_part_norm)

    ''' just to see the progress... '''
    if i%10==0:
        print i


''' only output '''
print "output ", np.argmax(haystack_correlated_normed), np.argmin(haystack_correlated_normed), np.max(haystack_correlated_normed), np.min(haystack_correlated_normed), np.mean(haystack_correlated_normed)