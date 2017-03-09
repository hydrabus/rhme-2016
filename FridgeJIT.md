# rhme-2016 write-up FridgeJIT
<a name="fridge"></a>
## FridgeJIT (reverse - 400 pts)
Like every reverse, a password was asked.<br>
This time we have the binary and a memory dump.<br>
The strings displayed can't be found in the firmware, they shall be in the VM.<br>
First we need to find the VM opcodes to dissasemble the binary 
starting @ 0x2b8 in memory.dmp.<br>
Some instructions names are available (for the debug mode display)
in the firmware and in the memory (this part is a copy from the firmware).<br>

At first, we searched the code corresponding to the instruction NOT
because the firmware will (probably) translate this instruction with the "com"
AVR asm (one's complement).

with r2 => "/c com" gave us the choice between 3 functions.<br>
The most likely function is the first one around the address 0x13fe because it
executes every AVR instructions four time in a row (maybe a 32bits VM ?!).

To confirm, we tried with the XOR opcode:<br>
with r2 => "/c eor" gave us more possibilities..but only one is executing the
"eor" AVR instruction four times in a row and call the function @ 0xf8e like the
NOT opcode (it smells good).

The 0xf8e function allows you to know how many bytes this opcode takes by
pointing on 0x1c4+r24 (r24 is the opcode number set just before the function).<br>
eg NOP:1, PUSH:2, MOV:4, etc ...

Now, still with r2, we searched every functions around the call @ 0xf8e
```
:> /c 0xf8e
:> pd -1 @@ hit*
0x00001008      83e0           ldi r24, 0x03
0x00001098      84e0           ldi r24, 0x04
0x00001138      85e0           ldi r24, 0x05
0x000011ba      88e0           ldi r24, 0x08
0x0000123c      89e0           ldi r24, 0x09
0x000012ba      8ae0           ldi r24, 0x0a
0x000013ae      8ce0           ldi r24, 0x0c
0x0000140e      8de0           ldi r24, 0x0d
... etc
```
It seems that we found the VM opcodes location.<br>
But before dissasembling the VM, we need to know what opcode is emulated
by every functions.
```
..think..think..nyan..think..
```
And finally we wrote the script fridgejit_parser.py.<br>
After execution, you have (almost) a clear program and we can see were 
the strings displayed at the begining comes from.<br>
The interesting part is the following:
```
[0134] MOVL r5,  #018c
[0138] CALL  r5
[013a] JNZ #0184
[013d] MOVL r5,  #01b0
[0141] CALL  r5
[0143] JNZ #0184
[0146] MOVL r5,  #01cc
[014a] CALL  r5
[014c] JNZ #0184
[014f] MOVL r5,  #020c
[0153] CALL  r5
[0155] JNZ #0184
[0158] MOVL r5,  #0234
[015c] CALL  r5
[015e] JNZ #0184
[0161] MOVL r5,  #025c
[0165] CALL  r5
[0167] JNZ #0184
[016a] MOVL r5,  #0270
[016e] CALL  r5
[0170] JNZ #0184
[0173] MOVL r5,  #0288
[0177] CALL  r5
[0179] JNZ #0184
[017c] MOVL r5,  #00f8
[0180] CALL  r5
[0182] ?! 7c
[0183] ?! c2
[0184] MOVL r5,  #0050
[0188] CALL  r5
```
If every call are returning >0, then it will display "Correct" else "Incorrect!"<br>
=> We need to reverse every functions !
```python
def rol(data, shift, size=32):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)

def ror(data, shift, size=32):
    shift %= size
    body = data >> shift
    remains = (data << (size - shift)) - (body << size)
    return (body + remains)

def disp(s,offset=0):
    raw = [s[i:i+2] for i in range(0, len(s), 2)][::-1]
    if offset:
        pad = " " * offset
    else:
        pad = ""
    out = ""
    for byte in raw:
        out += chr(int(byte,16))
    print pad+out.split()[0]

s = []
s.append("%08x" % (ror(0x5dd53c4f^0x3d6782a5, 0x11)))
s.append("%08x" % ((0x536d3b6d-0x2325dbf8) & 0xffffffff))
s.append("%08x" % ((0x5f<<24 | 0x54<<16 | 0x30<<8 | 0x47) & 0xffffffff))
s.append("%08x" % ((0x2059e2bd|0x536d0018)^(0xbde9+rol(0x74c,0x10))))
s.append("%08x" % (rol(0x9317eee5^(rol(0x3815cfb2,0x13)),0x13)))
s.append("%08x" % ((0xd419837a+0x9317eee5) & 0xffffffff))
s.append("%08x" % ((0xd419837a+0x9317eee5)-(rol(0xb2ef2c90,12))))
s.append("%06x" % (0x66d7db8e^0xb2ef2c90^0xd419837a^12))
i = 0
for chunk in s:
    disp(chunk, i)
    i += 2
```
if you execute this script, you will find the code (flag) : Y0u_G0T_1t_r1ght!
