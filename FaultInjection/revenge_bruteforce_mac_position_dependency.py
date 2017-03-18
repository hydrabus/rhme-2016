import sys
import serial
import time

import operator

def reset(ser):
  ser.rts = False
  ser.dtr = False
  time.sleep(0.1)
  ser.rts = True
  ser.dtr = True

def main():
  ser = serial.Serial(
          port="/dev/ttyUSB0",
          baudrate=19200,
          parity=serial.PARITY_NONE,
          stopbits=serial.STOPBITS_ONE,
          bytesize=serial.EIGHTBITS)

  reset(ser)
  time.sleep(2)
  ser.reset_input_buffer()

  # Valid signature
  #               [                              ][                              ][                              ][                              ][                              ][                              ][                              ][                              ][                              ][                              ][                              ][                              ]
  payload_orig = "05000a0d0400206401000500657404006365010005006e6e04006f6301000500207404006f6e01000500207204006f73010005006e6504007320010005005d5204004f5201000500524504005b20010005003a65040072750100050074610400726501000500706d0400657401000500207404006e650100050072720400754301000306041000340120000016141800260000001400256706201c200430000108030913140023000000000000000000b2b79ddf74e033ff037e81c1bddc349e"

  for pos in range((len(payload_orig) - 32)//2):
    if pos == 157 or pos == 159 or pos == 163:
      print "Position", pos
      print "Skipped to avoid infinite loop"
      continue
    payload = list(bytearray.fromhex(payload_orig))
    # Make sure we change the value
    if payload[pos] == 0:
      # FF is an invalid VM opcode
      payload[pos] = 255
    else:
      # 00 is a VM NOP
      payload[pos] = 0

    ser.write("".join(["%02x" % c for c in payload]) + "\n")
    ser.timeout = 0.5
    print "Position", pos
    print "".join([c for c in ser.readall() if ord(c) != 0x1b])
    reset(ser)
    time.sleep(2)
    ser.reset_input_buffer()

if __name__ == '__main__':
    main()

