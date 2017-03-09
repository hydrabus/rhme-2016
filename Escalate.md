# rhme-2016 write-up Escalate

<a name="escalate"></a>
## Escalate (Side Channel Analysis - 500 pts)

For this challenge, the exact same process has been applied. The jitter has been 
put between each sbox computation. It seems that a random number generation is 
executed at the beginning. But it doesn't matter, Simple Power Analysis reveals 
that the AddRoundKey is clean and unchanged. The hard work has been done on the 
synchronization were a wide window has been set to look after points to be 
synchronized.
