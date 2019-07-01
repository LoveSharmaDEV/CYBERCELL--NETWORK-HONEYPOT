#!/usr/bin/env python
"""Fake SSH Server Utilizing Paramiko"""
import threading
import socket
import sys
import traceback
import paramiko
import subprocess
import re
import os
import shlex

LOG = open("logs/log.txt", "a")
HOST_KEY = paramiko.RSAKey(filename='keys/private.key')
PORT = 22

os.chdir('/root')


def handle_cmd(cmd_inn, chan):
      if cmd_inn.startswith("vi") :
          cmd_out = 'PERMISSION DENIED'
      elif cmd_inn.startswith('cd') :
          cmd_out = 'PERMISSION DENIED'
      elif cmd_inn.startswith('nano'):
          cmd_out = 'PERMISSION DENIED'
      else:
        cmd = subprocess.Popen(cmd_inn, stdout = subprocess.PIPE , shell = True)
        cmd_out = str(cmd.stdout.read())
        '''cmd_out = cmd_out.split('\n')
        cmd_out = " ".join(cmd_out)'''
      LOG.flush()
      chan.send(cmd_out + "\r\n")
      

class session(paramiko.ServerInterface):
    """Settings for paramiko server interface"""
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Accept all passwords as valid by default
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True


def start_server():
    """Init and run the ssh server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', PORT))
    except Exception as err:
        print('*** Bind failed: {}'.format(err))
        traceback.print_exc()
        sys.exit(1)

    while True:
        try:
            sock.listen(100)
            print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as err:
            print('*** Listen/accept failed: {}'.format(err))
            traceback.print_exc()

        LOG.write("\n\nConnection from: " + addr[0] + "\n")
        print('Got a connection!')
        try:
            transport = paramiko.Transport(client)
            transport.add_server_key(HOST_KEY)
            # Change banner to appear legit on nmap (or other network) scans
            transport.local_version = "SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3"
            server = session()
            try:
                transport.start_server(server=server)
            except paramiko.SSHException:
                print('*** SSH negotiation failed.')
                raise Exception("SSH negotiation failed")
            # wait for auth
            chan = transport.accept(20)
            if chan is None:
                print('*** No channel.')
                raise Exception("No channel")

            server.event.wait(10)
            if not server.event.is_set():
                print('*** Client never asked for a shell.')
                raise Exception("No shell request")

            try:
                chan.send("Welcome to the my control server\r\n\r\n")
                run = True
                while run:
                    chan.send("$root@kali ")
                    command = ""
                    while not command.endswith("\r"):
                        transport = chan.recv(1024)
                        # Echo input to psuedo-simulate a basic terminal
                        chan.send(transport)
                        command += transport.decode("utf-8")

                    chan.send("\r\n")
                    command = command.rstrip()
                    LOG.write("$ " + addr[0]+' '+ command + "\n")
                    print(command)
                    if command == "exit":
                        run = False
                    else:
                        handle_cmd(command, chan)

            except Exception as err:
                print('!!! Exception: {}: {}'.format(err.__class__, err))
                traceback.print_exc()
                try:
                    transport.close()
                except Exception:
                    pass

            chan.close()

        except Exception as err:
            print('!!! Exception: {}: {}'.format(err.__class__, err))
            traceback.print_exc()
            try:
                transport.close()
            except Exception:
                pass


if __name__ == "__main__":
    start_server()
