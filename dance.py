from __future__ import print_function
import numpy
import audio

points = []

def dance(length, data):
    bass = 0
    k = numpy.arange(length)            # start with [1,2,3...]
    T = length / float(audio.RATE)      # get inverse of sample rate
    frq = k / T                         # frq = [1/T, 2/T, 3/T, ...]
    frq = frq[range(length / 4)]        # only get first n / 4 freqs

    fourier = numpy.fft.rfft(data) / length    # apply fft and normalize
    fourier = abs(fourier[range(length / 4)])

    bass += fourier[1]
    bass += fourier[2]

    points.append(bass)

    if len(points) > 4:
        del points[0]

    dy = (points[len(points) - 1] - points[0]) / len(points)
    average_bass = numpy.average(points)

    if (dy > 2000):
        print(dy, points)
        return True

    return False
