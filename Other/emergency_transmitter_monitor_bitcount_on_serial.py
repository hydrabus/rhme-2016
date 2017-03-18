import serial
import time
import numpy as np

ENMORSE = {'A': '.-',     'B': '-...',   'C': '-.-.',
           'D': '-..',    'E': '.',      'F': '..-.',
           'G': '--.',    'H': '....',   'I': '..',
           'J': '.---',   'K': '-.-',    'L': '.-..',
           'M': '--',     'N': '-.',     'O': '---',
           'P': '.--.',   'Q': '--.-',   'R': '.-.',
           'S': '...',    'T': '-',      'U': '..-',
           'V': '...-',   'W': '.--',    'X': '-..-',
           'Y': '-.--',   'Z': '--..',

           '0': '-----',  '1': '.----',  '2': '..---',
           '3': '...--',  '4': '....-',  '5': '.....',
           '6': '-....',  '7': '--...',  '8': '---..',
           '9': '----.'
           }

DEMORSE = dict((v,k) for (k,v) in ENMORSE.items())

# This is not the Riscure Nano, this is the Arduino running the emergency_transmitter_morse_decoder sketch
serMonitorArduino = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def roundPatterns(lst, length=26):
    length = float(length)
    rounded_lst = [int(round(val/length)*length) for val in lst]

    # All pattern lengths are now a multiple of "length"
    return rounded_lst

def decode(rounded_lst, length=26):
  morse = []
  # Some sanitization occurs here: only consider patterns of correct length
  for count_i, count in enumerate(rounded_lst):
    if count_i % 2 == 1:
      # This is the "LED off" state, distinguish between ETU and character separator
      if count == 5*length:
          morse.append('  ')
    else:
      # This is the "LED on" state, distinguish between short and long pulses
      if count == length:
          morse.append('.')
      elif count == 3*length:
          morse.append('-')

  try:
    res = "".join([DEMORSE[v] for v in ("".join(morse)).split()])
  except KeyError:
    res = "Couldn't decode"

  return res

def main():
  serMonitorArduino.isOpen()

  # Clear serial buffers
  while serMonitorArduino.in_waiting:
    serMonitorArduino.read(1)

  bitcounts = ""
  while True:

    while not '\n' in bitcounts:
      bitcounts += serMonitorArduino.read(1)

    bitcounts_lst = bitcounts.split('\n')

    cb = []

    # Only manage the first bitcounts, up to \n
    for nb in bitcounts_lst[0].split():
      try:
        # Convert serial string to integer list
        nb = int(nb)
        cb.append(nb)
      except ValueError:
        pass

    # Clean up the collected samples to have all lengths multiple of a unique value
    rp = roundPatterns(cb)

    # Decode the Morse value
    de = decode(rp)

    print(de)

    # Pack everything back, if there is anything left the next loop will process it
    bitcounts = "\n".join(bitcounts_lst[1:])


if __name__ == '__main__':
  main()