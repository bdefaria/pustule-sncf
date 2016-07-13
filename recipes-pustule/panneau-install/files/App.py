#!/usr/bin/env python3

import os
import time
import serial
import textwrap

MAX_SMS_SIZE=140
sms_path = "/var/spool/sms/inbox/"
sms_raw_path = "/home/root/raw/"
smsfiles = None
seriallink = None
time_per_page = 5
page_number = 0
frozen = 0

# Master Finfin commands
# #FINF00   	Reset the pannel
# #FINF01XX 	Change display time per page in seconde (1 to 19)
# #FINF02MSG 	Freeze the pannel with the message
# #FINF03	Unfreeze the pannel

def get_sms():
	global smsfiles
	smsfiles = [f for f in os.listdir(sms_path) if os.path.isfile(os.path.join(sms_path, f))]

def remove_long_sms():
	global smsfiles
	for filename in smsfiles:
		f = open(sms_path+filename)
		length = 0
		for lines in f:
			if 'Length = ' in lines:
				length += int(lines.replace("Length = ",""))
		f.close()
		if length > MAX_SMS_SIZE:
			print("SMS too big (" + str(length) + ")")
			smsfiles.remove(filename)
			os.remove(sms_path+filename)

def convert_sms_to_raw():
	timestr = time.strftime("%Y%m%d%H%M%S") + "00"
	for filename in smsfiles:
		f = open(sms_path+filename)
		next(f)
		next(f)
		next(f)
		raw_str = ""
		for lines in f:
			if "; " in lines:
				raw_str = raw_str + lines.replace("; ","").replace("\n","")
		f.close()
		fraw = open(sms_raw_path+timestr,'w+')
		fraw.write(raw_str+"\n")
		fraw.close()
		timestr = str(int(timestr) + 1)

def clean_sms():
	for filename in smsfiles:
		os.remove(sms_path+filename)

def send_reset():
	print("Reset!!!!")
	seriallink.write(b"\x0f\x21\x0e\x10\x03\x09")
	time.sleep(1)

def send_page(*arg):
	page = arg[0].replace("\n","")
	templine = ""
	padded_page = ""
	wrapped_page = textwrap.fill(page, width= 20)
	for char in wrapped_page:
		if char is not '\n':
			templine+=char
		else:
			padded_page+='{s:{c}^{n}}'.format(s=templine.replace('\n',''),n=20,c=' ')
			templine=""
	padded_page+='{s:{c}^{n}}'.format(s=templine.replace('\n',''),n=20,c=' ')
	padded_page='{:<160}'.format(padded_page)
	header = b"\x02\x5c"
	num_page = b"\x30\x30"
	effect = b"\x31"
	fonte = b"\x31"
	time_page = bytes([time_per_page + 48])
	color = b"G"
	print(padded_page)
	f = open("/home/root/last",'w+')
	f.write("x0fx21x0e")
	seriallink.write(b"\x0f\x21\x0e")
	f.write("x02x5cx30x30x01x01x49Gx3a"+padded_page+"x03")
	seriallink.write(header+num_page+effect+fonte+time_page+color+b"\x3a"+str.encode(padded_page.replace("\n"," "))+b"\x03")
	f.write("x08xaaxaax09")
	seriallink.write(b"\x08\xaa\xaa\x09")
	f.close()

def init_serial():
	global seriallink
	seriallink = serial.Serial(
	port='/dev/ttyPanneau',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
	)
	seriallink.flushInput()

def handle_cmd(*arg):
	global time_per_page
	global frozen
	cmd = (arg[0].replace("#FINF",""))

	if cmd.startswith("00"):
		send_reset()
		frozen = 0
	elif cmd.startswith("01"):
		if (int(cmd) - 100) < 19 and (int(cmd) - 100) > 0:
			time_per_page = (int(cmd) - 100)
			print("New Time per page : " + str(time_per_page))
	elif cmd.startswith("02"):
		frozen = 1
		print("Freeze")
		send_page(cmd[2:])
	elif cmd.startswith("03"):
		frozen = 0
		print("Unfreeze")

def handle_sms():
	rawfiles = [f for f in os.listdir(sms_raw_path) if os.path.isfile(os.path.join(sms_raw_path, f))]
	i = 0
	page = [None] * 5
	for sms in rawfiles:
		f = open(sms_raw_path+sms)
		for line in f:
			if line.startswith("#FINF"):
				handle_cmd(line)
			else:
				if i < 5:
					page[i] = line
					i += 1
		f.close()
		os.remove(sms_raw_path+sms)

	if frozen == 0:
		while i > 0:
			send_page(page[i - 1])
			i -= 1
		

if __name__ == '__main__':
	init_serial()
	while 1:
		get_sms()
		remove_long_sms()
		convert_sms_to_raw()
		clean_sms()
		handle_sms()
		time.sleep(1)
