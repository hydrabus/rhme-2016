# rhme-2016 write-up Key Server

<a name="keyserver"></a>
## Key Server (Crypto - 200 pts)

The purpose is to generate a RSA PKCS1_v1_5 SHA-1 signature of "admin" with one 
of the administrator's key:
+ Alice
+ Bob
+ Carl
+ David
+ Edward
+ Fleur
+ Gary

We have only the public modulus of the public key. In RSA public modulus, 
denoted $n$, is equal to the product of two prime numbers, denoted $p$ and $q$.
These two prime numbers are secret and once found the private can be recovered.

To generate a huge prime number, a randomly generated seed is used as a starting 
point to found the next prime. If this seed is poorly generated, collision may 
happen. Let's try if we have a collision on prime numbers.

$gcd(alice_{n}, bob_n) = 1$ which means no co factor. 
$alice_n = alice_p * alice_q$ and $bob_n = bob_p * bob_q$. 
All prime numbers are different.
This statement is true for all couples of public key ... except one!


$p = gcd(bob_n, gary_n) =$ `0xf3432ec95a2d8ec3e2dc6c52c1eb97d03601d6a0c1e89848fe
54f55b31a9fc35de1ce9210ff84fd79be293924de45320c86e5dc9d970b68079737a1bb2e34935`
 
So $gary_q = gary_n/p$ and we have gary_p and gary_q.
We could have bob's prime numbers as well.
 
Now we have to compute the signature of “admin” using a public exponent 
which is unknown. 
Public exponent are often small numbers: $3$, $5$, $17$, $257$ or $65537$.
We have to compute the associated private exponent, denoted $d$ which is equal 
to $e^{-1} \mod (p-1)(q-1)$, of all possible public exponent, denoted $e$, and 
compute the associated signature.

After multiple tries, the correct public exponent is `65537 = 0x10001`

The correct private key is 

`0x8499c5e0fe2848379d0eac9cfdbe21c5540104819a9
7156a4d1b19456bb682db77e26bff4ab857144a85f4214b8ca866ec0033a61edf865b349906782b9
c2fc4d57d6621f731ec7009bdeafe59256afdc8fd84f2fe7d70e9f84756f48008a15c20a5d38dacd
2bcd1b5f2b0b855b911e6a3a8cb9072b9f6f7847933aa260521a1`

The sha-1 hash of "admin" is `0xD033E22AE348AEB5660FC2140AEC35850C4DA997`

PKCS1 format is `0001 FFPADDING 00 ASN1_HASH HASH_VALUE`

After formating, the input to sign is equal to 

`0x0001fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
fffffffffffffffffffffffffff 00 3021300906052b0e03021a05000414 
d033e22ae348aeb5660fc2140aec35850c4da997`

The generate signature is equal to 

`0x80103B7FC74600B844BB73667C2C8F23AFA717E25E549756819A53BD875A79ECC80DBD9E415DF4
D4356FB623DA62A6388D0D1BF277DBAA6021C5E5FD51A2BA088BFDEE2CEA800E50155AEA1AD7A101
8EC7621E2DAC9D16CA6C1910EE3F0382E0A0ECA1124D6B357A8D669CBA6C0D24F384A5FC2890DB54
341C383289E32C727F`

`FLAG:e5bcdc1d710fca2194afb67c30e2f4e4`
