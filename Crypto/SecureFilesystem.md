# rhme-2016 write-up Secure Filesystem

<a name="securefs"></a>
## Secure Filesystem (Crypto - 100 pts)

This challenge is presented as a secure filesystem with a token system to 
authenticate itself. Some examples are provided:
```
96103df3b928d9edc5a103d690639c94628824f5 | cat.txt
933d86ae930c9a5d6d3a334297d9e72852f05c57 | cat.txt:finances.csv
83f86c0ba1d2d5d60d055064256cd95a5ae6bb7d | cat.txt:finances.csv:joke.txt
ba2e8af09b57080549180a32ac1ff1dde4d30b14 | cat.txt:joke.txt
0b939251f4c781f43efef804ee8faec0212f1144 | finances.csv
4b0972ec7282ad9e991414d1845ceee546eac7a1 | finances.csv:joke.txt
715b21027dca61235e2663e59a9bdfb387ca7997 | joke.txt
```

From that we understand that a 160 bits value is used as authentication token.
We notice also that it is linked to the filename list we want to access.

The question to answer is what is the cryptographic function used to generate 
such tokens? What is the key? What is the data?

First, the token length gives a strong hint on which function has been used to 
generate the token. As a hash function, we do have the choice between SHA-1, 
RIPEMD-160, HAVAL-160, Tiger-160. To be honest, we strongly believed it was 
Tiger because we wanted to.

Second, what could be the secret key used to be authenticated to the file system.
How can we break a HMAC with a full length key? After long research and several 
tries we found a nice github repository with a tool exploiting length extension 
attack on hash function. It smells good : https://github.com/bwall/HashPump.
We actually don't care of the key value, only a guess on key length has to be 
done. Let's guess password length for 0 to 32 and try to hash passwd file by 
using a give token.

The flag is found.
