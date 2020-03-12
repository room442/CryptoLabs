My lab, that implements RSA encryption.

`schemeinstal.py BITS -f filename` — print scheme params to filename, but `main.py` reads only from `params.py`

`main.py -e filename` — encrypting, output to filename.enc 

`main.py -d filename` — decrypting, output to filename.dec

`main.py -s filename` — sign filename, output to filename.sign

`main.py -c filename --sfile sign` — check sign of the filename, given by `--sfile`