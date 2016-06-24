#!/usr/bin/env python3

import os
import time
import serial

MAX_SMS_SIZE=140
sms_path = "/var/spool/sms/inbox/"
sms_raw_path = "/home/root/raw/"
smsfiles = None
seriallink = None
loop_time = 20

#Serial Commands
def get_sms():
	global smsfiles
	smsfiles = [f for f in os.listdir(sms_path) if os.path.isfile(os.path.join(sms_path, f))]

def remove_long_sms():
	global smsfiles
	for filename in smsfiles:
		big = 0
		f = open(sms_path+filename)
		for lines in f:
			if 'Length = ' in lines:
				length = int(lines.replace("Length = ",""))
			if '[SMSBackup001]' in lines:
				big = 1
		f.close()
		if length > MAX_SMS_SIZE or big:
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
	seriallink.write(b"\x0f\x21\x0e\x10\x03\x09")
	time.sleep(1)

def send_page(*arg):
	header = b"\x02\x5c"
	num_page = b"\x00"
	effect = b"\x02"
	fonte = b"\x01"
	time_page = b"\x49"
	color = b"G"
	print(arg)
	seriallink.write(header+num_page+effect+fonte+time_page+color+b"\x3a"+str.encode(arg[0].replace("\n",""))+b"\x03")

def init_serial():
	global seriallink
	seriallink = serial.Serial(
	port='/dev/ttyO2',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
	)
	seriallink.flushInput()

def handle_sms():
	rawfiles = [f for f in os.listdir(sms_raw_path) if os.path.isfile(os.path.join(sms_raw_path, f))]
	for sms in rawfiles:
		f = open(sms_raw_path+sms)
		for line in f:
			send_page(line)
		f.close()
		os.remove(sms_raw_path+sms)

if __name__ == '__main__':
	init_serial();
	while 1:
		get_sms()
		remove_long_sms()
		convert_sms_to_raw()
		clean_sms()
		handle_sms()
		time.sleep(loop_time)
