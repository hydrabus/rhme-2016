# rhme-2016 write-up Secure Filesystem v192.r1

<a name="securefs192r1"></a>
## AVR Secure Filesystem v192.r1

This is next version of Secure Filesystem with longer token 2x 192 bits.
Some examples are provided:
```
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
dfd0f4a25b7d529e89ac030c2b681e93831e95a8186823b9 | cat.txt
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
f2bca35d472116dc6d5bebe96f1a3af249be78c63219a0dc | cat.txt:finances.csv
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
7eed666977d3861dbaefd16b2ed7dc5b639e51853ca6e7b3 | cat.txt:finances.csv:joke.txt
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
51d915246394ce976f8768cf3300087cb5b9958bbec30f9c | cat.txt:joke.txt
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
ae2a5a38b4d03f0103bce59874e41a0df19cb39b328b02fa | finances.csv
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
c66b5e48f5e600982724eca3804fb59b7b0f395a6e17e1ce | finances.csv:joke.txt
897703036b2e18116b36353d92ac3dd978845fc99a735b8a |
3a3a9b3cc5239fdf4572157296903a0237a4aaeeaa8f3d15 | joke.txt
```

We directly noticed the first 192 bits which is static, looks so weird to be 
innocent. Another point is the long processing time which feels like doing 
overkilling execution on a poor ATMega328p. The final hint is the title wich is
v192.r1. 
Gathering all those hints, we found out that it might be a ECDSA over a 
192 bits field. The static part is depending on a random used during ECDSA 
signature generation and PS3 hacks makes it famous. We are now confident!

Openssl gives us:
``` 
  secp192k1 : SECG curve over a 192 bit prime field
  prime192v1: NIST/X9.62/SECG curve over a 192 bit prime field
  prime192v2: X9.62 curve over a 192 bit prime field
  prime192v3: X9.62 curve over a 192 bit prime field
  brainpoolP192r1: RFC 5639 curve over a 192 bit prime field
  brainpoolP192t1: RFC 5639 curve over a 192 bit prime field
```

We have two candidates: brainpoolP192r1 and prime192v1 which has another name 
NIST P-192r1.

Let's try these curves in order to find the private scalar which then can be 
used to generate ECDSA for passwd file.
