rhme-2016 write-up Jumpy

This challenge is a classic reverse engineering challenge and the aim is to find the password by reversing the jumpy.bin file provided

As our aim was not to do it like others by using the excellent [Radare2](https://github.com/radare/radare2) or IDA Pro ...

We have started by checking AVR Simulator and we have found the excellent [simavr](https://github.com/buserror/simavr)
In fact this simulator can be also used as as fantastic trace/debugger tool if we change one line in the makefile
Just enable this line in [Makefile](https://github.com/buserror/simavr/blob/master/Makefile)
```
CFLAGS	+= -DCONFIG_SIMAVR_TRACE=1
```

The next step was to modify simavr\examples\board_simduino to simavr\examples\board_hydra in order to add pty simulation for UART RX&TX

Shell 1
```bash 
$ export SIMAVR_UART_XTERM=1
$ ./simavr_hydra.elf -g -d -t Jumpy.hex > trace_abcdefghi012345.txt
uart_pty_connect_19200: /tmp/simavr-uart0 now points to /dev/pts/4
cat < /dev/pts/4
echo 'hello' > /dev/pts/4
picocom -b 19200 /dev/pts/4
```

Shell 2
```bash 
cat < /dev/pts/4
```

Shell 3
```bash 
echo 'abcdefghk012345' > /dev/pts/4
```

Shell 4
```bash 
avr-gdb -ex 'target remote localhost:1234' 
cont
```

Shell 2 output
```
Input: 
Better luck next time!
```

Shell 1 output
```
inf loop exit
Press Ctrl C to quit
```

Now we have a superb `trace_abcdefghi012345.txt` (of more than 30MB)
* Open the trace and search cpi 
* We can clearly see the checks on hose lines which shall be reversed to find the computation and the right characters for the password
Extract of the interesting cpi
```text
avr_run_one: 034e: cpi r24[0d], 0x0d
avr_run_one: 0392: cpi r24[d3], 0xd3 => 0x0135[0x5F/_] + 0x0136[0x74/t]				=> Char 8	 9	
avr_run_one: 06e2: cpi r24[10], 0xc0 0x15 => 0x0136[0x74/t] x 0x0137[0x30/0]	=> Char 9	 10
avr_run_one: 0646: cpi r24[22], 0xb7 0x13 => 0x012e[0x67/g] x 0x012f[0x31/1]	=> Char 1		2	
avr_run_one: 0694: cpi r24[ac], 0x82 0x17 => 0x0130[0x76/v] x 0x0131[0x33/3]	=> Char 3		4	
avr_run_one: 04d4: cpi r24[c9], 0x92 => 0x0131[0x33/3] + 0x0132[0x5F/_]				=> Char 4		5	
avr_run_one: 0570: cpi r24[d8], 0x0c 0x2b => 0x0134[0x74/t] x 0x0135[0x5F/_]	=> Char 7		8	
avr_run_one: 0726: cpi r24[cd], 0xa5 => 0x0133[0x31/1] + 0x0134[0x74/t]				=> Char 6		7	
avr_run_one: 0442: cpi r24[61], 0x8f => 0x0137[0x30/0] + 0x0138[0x5F/_] 			=> Char 10	11
avr_run_one: 05b4: cpi r24[c5], 0xa7 => 0x012f[0x31/1] + 0x0130[0x76/v]				=> Char 2		3	
avr_run_one: 0522: cpi r24[92], 0x73 0x28 => 0x0138[0x5F/_] x 0x0139[0x6D/m]	=> Char 11	12
avr_run_one: 03fc: cpi r24[97], 0x97 0x02 => 0x013a[0x33/3] x 0xD (0x013b)		=> Char 13	14
avr_run_one: 0490: cpi r24[3e], 0x2f 0x12 => 0x0133[0x31/1] x 0x0132[0x5F/_]	=> Char 6		5	
avr_run_one: 05f8: cpi r24[65], 0xa0 => 0x0139[0x6D/m] + 0x013a[0x33/3]				=> Char 12	13
avr_run_one: 075e: cpi r24[00], 0xff 0x3f => 0x013e 0x013f
```
Password is: `g1v3_1t_t0_m3`

Shell 1
```bash 
./simavr_hydra.elf Jumpy.hex
```

Shell 2
```bash 
cat < /dev/pts/4
```

Shell 3
```bash 
echo -e 'g1v3_1t_t0_m3' > /dev/pts/4
```

Shell 2 Output 
```
Input: 
FLAG:
```

Doing that with the real board output the real flag
