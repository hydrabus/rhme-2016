# rhme-2016 write-up The Impostor
<a name="impostor"></a>
## The Impostor (Reverse - 300 pts)
This binary ask for a 16 bytes password.<br>
First, the FLAG string is load in the function @ 0x1300.<br>
Starting the reverse from 0x1300:<br>
&nbsp;&nbsp;&nbsp;&nbsp;-> 0xed0 (nothing interesting)<br>
&nbsp;&nbsp;&nbsp;&nbsp;-> 0xeb2 (nothing interesting)<br>
&nbsp;&nbsp;&nbsp;&nbsp;-> 0xa32 (!)<br>
The jump from 0xa32 is part of a big jump table which is called from an address
incremented by 2 at the begining of the function.<br>
Reversing this function, we can see that the base address is 0x0068.<br>
Looking at this address, the code doesn't look like an AVR code (until 0x05d4).<br>
With the help of radare2 and rasm2, we tried to desassemble this block with 
differents architectures until found something interesting (arm thumb).<br>
With the help of the Hopper decompiler, we discovered a XTEA algorithm used 
in order to encrypt 16 bytes.<br>
We just need to reverse this function with the following C code:

``` c
#include <stdio.h>
#include <stdint.h>

void tea_decrypt (uint32_t* buff, uint32_t* keys)
{
	uint32_t delta =  0xAB64E218;
	uint32_t sum = delta * 32;

	for (int i = 0; i < 32; i++) {
		buff[1] -= (((buff[0] << 4)^(buff[0] >> 5)) + buff[0]) ^ (sum + keys[(sum >> 11) & 3]);
		sum -= delta;
		buff[0] -= (((buff[1] << 4)^(buff[1] >> 5)) + buff[1]) ^ (sum + keys[sum & 3]);
	}
}

void main()
{
	uint32_t key[]  = {0x373D3943, 0x49A1C621, 0x80C6B0, 0x3C93C7B};
	uint32_t buff[] = {0xFC791D6B, 0x924E6C8F, 0x795F34A2, 0xEDAE901, 0};

	tea_decrypt (buff, key);
	tea_decrypt (&buff[2], key);
	printf("%s\n", buff);
}
```

The code was: 4rM_c0rT3xM0_4vR
