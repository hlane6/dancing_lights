import alsaaudio as aa

CHANNELS = 1
RATE = 44100
FORMAT = aa.PCM_FORMAT_S16_LE
CHUNK = 1024

inp = aa.PCM(aa.PCM_CAPTURE, aa.PCM_NORMAL, 'hw:1,0')
inp.setchannels(CHANNELS)
inp.setrate(RATE)
inp.setformat(FORMAT)
inp.setperiodsize(CHUNK)
