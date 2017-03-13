# rhme-2016 write-up Revenge

<a name="revenge"></a>
## Revenge (Fault Injection - 300 pts)

This challenge is, according to the RHme2 map, linked to both the FI challenges and the exploitation ones. VM opcode blobs, as shown in the `example.hex` file, now seemed accompanied with some kind of code MAC. Our initial understanding was that we had to provide the solution.hex content to the VM, and fault the MAC verification to get it to execute.

We started with a logic analyzer which showed a timing difference when providing the correct MAC versus a modified one. It was confirmed and identified on an oscilloscope to get ready for the fault injection. But before that, we continued with some low cost analysis.

While dissecting the signed code example, it looked like we had a NOP padding that was added to have everything nicely fit in 16-byte long blocks, the last block being the MAC. Adding or removing a padding byte returned an `Input error`. We tried changing a bit in the padding, and we smiled when we saw that the MAC was still valid, as the opcode blob would execute and tell us that `Current temperature: [ERROR] sensor not connected`.

Our interpretation at that point was that only the useful code was included in the MAC, while the padding was ignored. We could set the padding bytes to whatever value we wanted and the `sensor not connected` message would show up.

What we couldn't figure out next was how the length of this padding could be determined, as it could take whatever value we wanted. So we then tried swapping unrelated opcodes, to be iso-functional, and finally modified bytes of `example.hex` one at a time to observe the side-effect upon execution.

The twenty two first positions yield an `Authentication failed`, but the following ones either return `sensor not connected`, an `Oops!` and even the beloved `[ FridgeJIT Console ]`.

It was then a matter of applying again the same tactics as for *Hide & Seek* and *The Weird Machine* to obtain the flag. No hardware FI in the end :)

Python script used bruteforce_mac_position_dependency.py:
```python
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

```
