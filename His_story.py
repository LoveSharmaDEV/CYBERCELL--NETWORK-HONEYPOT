#!/usr/bin/env python
import subprocess
import re

while True:
	try :
	   s = input()
	except:
	   break
	   
	if s.lower() == 'exit' :
		break
		
	try:
		cmd = subprocess.Popen(re.split(r'\s+' , s), stdout = subprocess.PIPE , shell = True)
		cmd_out = cmd.stdout.read()
		
		print(cmd_out)
		
		
	except OSError:
		print('Invalid Command')
