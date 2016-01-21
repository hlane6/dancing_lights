import audio
import numpy
import os
import subprocess
import random

recent = False
timeout = 0
current_light = "white"

light_to_command = {
        "red": "KEY_F",
        "green": "KEY_F2",
        "blue": "KEY_F3",
        "dark-red": "KEY_F5",
        "light-green": "KEY_F6",
        "light-blue": "KEY_F7",
        "red-orange": "KEY_F9",
        "turquoise": "KEY_F10",
        "dark-blue": "KEY_F11",
        "orange": "KEY_F13",
        "dark-green": "KEY_F14",
        "purple": "KEY_F15",
        "yellow": "KEY_F17",
        "aqua": "KEY_F18",
        "pink": "KEY_F19"
    }

light_to_light = {
        "white": ["red", "green", "blue", "yellow"],
        "red": ["green", "blue", "light-green", "light-blue"],
        "green": ["blue", "red", "light-blue", "dark-red"],
        "blue": ["red", "green", "dark-red", "light-green"],
        "dark-red": ["light-green", "light-blue", "turquoise", "dark-blue"],
        "light-green": ["light-blue", "dark-red", "red-orange", "dark-blue"],
        "light-blue": ["dark-red", "light-green", "red-orange", "turquoise"],
        "red-orange": ["turquoise", "dark-blue", "dark-green", "purple"],
        "turquoise": ["dark-blue", "purple", "red-orange", "orange"],
        "dark-blue": ["red-orange", "orange", "turquoise", "dark-green"],
        "orange": ["dark-green", "purple", "aqua", "pink"],
        "dark-green": ["purple", "pink", "orange", "yellow"],
        "purple": ["orange", "yellow", "dark-green", "aqua"],
        "yellow": ["aqua", "pink", "green", "blue"],
        "aqua": ["yellow", "red", "blue", "pink"],
        "pink": ["yellow", "aqua", "red", "green"]
    }

def change_light(current):
    return random.choice(light_to_light[current])

def generate_command(light):
    return "irsend SEND_ONCE lights " + light_to_command[light]

points = []

def update_bass_energies(length, data):
    if length < 4:
        return 0

    bass = 0
    k = numpy.arange(length)            # start with [1,2,3...]
    T = length / float(audio.RATE)      # get inverse of sample rate
    frq = k / T                         # frq = [1/T, 2/T, 3/T, ...]
    frq = frq[range(length / 4)]        # only get first n / 4 freqs

    fourier = numpy.fft.rfft(data) / length    # apply fft and normalize
    fourier = abs(fourier[range(length / 4)])


    for i in range(2):
        bass += fourier[i]

    points.append(bass)

    if len(points) > 43:
        del points[0]

    return bass

def dance(bass):
    if (bass > numpy.average(points) * 2):
        print bass
        return True
    return False

if __name__ == '__main__':
    while True:
        length, data = audio.inp.read()
        
        try:
            a = numpy.fromstring(data, dtype='int16')
            bass = update_bass_energies(length, a)

            if not recent:
                if dance(bass):
                    current_light = change_light(current_light)
                    subprocess.call(generate_command(current_light), shell=True)
                    timeout = 0
                    recent = True
            else:
                if timeout < audio.RATE * .3:
                    timeout += audio.CHUNK
                else:
                    recent = False
        except:
            print "Frame not full"
