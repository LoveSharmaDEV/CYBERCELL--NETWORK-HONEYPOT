# Fake SSH
![Example](screenshots/clippy.png "Clippy!")

* Python program to emulate an ssh server as a sort of psuedo-honeypot with some fun commands. It will accept all connections given any provided username/password for authentication.

* Utilizes paramiko for the OpenSSH protocol. A generic private key is provided for convenience, although it can be substituted out for another key if desired.

* Being a low interaction honeypot, it do not provide a much interactive interface. The code can be customised to run fixed commands that provides enough information to keep attacker engaged.

* So the interactive commands can be hard coded to give some false output or  some restriction banner saying (NOT PERMITTED OR PERMISSION DENIED).


* In this project we have have used python ***subprocess*** library to basically run remote commands on local machine and then return output to the attacker. But this feature can be fully controlled and customized for blacklisting any command or for just allowing few commands.
## Usage
This should be able to run on both python 2 and 3 with paramiko as the only requirement

`pip install paramiko`

Then simply run the file to start the server:

`sudo ./fake_ssh.py`

Note: sudo is simply needed to bind to port 22, although this can be easily changed if desired (it will present a generic OpenSSH banner/fingerprint to network scanners to find regardless of the port)

![Scan](screenshots/nmap.png "Spoofed Banner")

![Screenshot from 2019-07-01 22-11-23](https://user-images.githubusercontent.com/31883696/60452877-378e5380-9c4d-11e9-956a-521248b5b9eb.png)
