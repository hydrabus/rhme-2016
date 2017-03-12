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
