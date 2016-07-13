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
color = b"G"

# Master Finfin commands
# #FINF00	Reset the pannel
# #FINF01XX	Change display time per page in seconde (1 to 19)
# #FINF02MSG	Freeze the pannel with the message
# #FINF03	Unfreeze the pannel
# #FINF04X	Set text color G for Amber R for red

# get_sms Parse gammu-smsd inbox directory to get sms filenames
def get_sms():
	global smsfiles
	smsfiles = [f for f in os.listdir(sms_path) if os.path.isfile(os.path.join(sms_path, f))]

# remove_long_sms() Check sms length and remove too long ones
def remove_long_sms():
	global smsfiles
	for filename in smsfiles:
		f = open(sms_path+filename, "r", encoding="utf-8")
		length = 0
		for lines in f:
			if 'Length = ' in lines:
				length += int(lines.replace("Length = ",""))
		f.close()
		if length > MAX_SMS_SIZE:
			print("SMS too big (" + str(length) + ")")
			smsfiles.remove(filename)
			os.remove(sms_path+filename)

# convert_sms_to_raw() Convert gammu-smsd files to raw text files
def convert_sms_to_raw():
	timestr = time.strftime("%Y%m%d%H%M%S") + "00"
	for filename in smsfiles:
		f = open(sms_path+filename, "r", encoding="utf-8")
		next(f)
		next(f)
		next(f)
		raw_str = ""
		for lines in f:
			if "; " in lines:
				raw_str = raw_str + lines.replace("; ","").replace("\n","")
		f.close()
		fraw = open(sms_raw_path+timestr,'w+', encoding="utf-8")
		fraw.write(raw_str+"\n")
		fraw.close()
		timestr = str(int(timestr) + 1)

# clean_sms() Remove sms files from gammu-smsd inbox directory
def clean_sms():
	for filename in smsfiles:
		os.remove(sms_path+filename)

# send_reset() Send the reset command
def send_reset():
	print("Reset!!!!")
	seriallink.write(b"\x0f\x21\x0e\x10\x03\x09")
	time.sleep(10)

# send_page() Try to wrap the text and send it to pannel
def send_page(*arg):
	page = arg[0].replace("\n","")
	templine = ""
	padded_page = ""
	wrapped_page = textwrap.fill(page, width= 20)
	for char in wrapped_page:
		if char is not '\n':
			if char is 'è'or char is 'é'or char is 'ê' or char is 'ë':
				templine+='e'
			elif char is 'É'or char is 'È'or char is 'Ê' or char is ' Ë':
				templine+='E'
			elif char is 'à' or char is 'á' or char is 'â'or char is 'ä':
				templine+='a'
			elif char is 'Á' or char is 'À' or char is 'Â'or char is 'Ä':
				templine+='A'
			elif char is 'ç':
				templine+='c'
			elif char is 'Ç':
				templine+='C'
			else:
				templine+=char
		else:
			padded_page+='{s:{c}^{n}}'.format(s=templine.replace('\n',''),n=20,c=' ')
			templine=""
	padded_page+='{s:{c}^{n}}'.format(s=templine.replace('\n',''),n=20,c=' ')
	padded_page='{:<160}'.format(padded_page)
	if len(padded_page) > 160:
		templine=""
		for char in page:
			if char is 'è'or char is 'é'or char is 'ê' or char is 'ë':
				templine+='e'
			elif char is 'É'or char is 'È'or char is 'Ê' or char is ' Ë':
				templine+='E'
			elif char is 'à' or char is 'á' or char is 'â'or char is 'ä':
				templine+='a'
			elif char is 'Á' or char is 'À' or char is 'Â'or char is 'Ä':
				templine+='A'
			elif char is 'ç':
				templine+='c'
			elif char is 'Ç':
				templine+='C'
			else:
				templine+=char
		padded_page='{:<160}'.format(templine)
	header = b"\x02\x5c"
	num_page = b"\x30\x30"
	effect = b"\x31"
	fonte = b"\x31"
	time_page = bytes([time_per_page + 48])
	seriallink.write(b"\x0f\x21\x0e")
	seriallink.write(header+num_page+effect+fonte+time_page+color+b"\x3a"+str.encode(padded_page.replace("\n"," "))+b"\x03")
	seriallink.write(b"\x08\xaa\xaa\x09")

# init_serial() Initialize the serial com to the pannel
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

# handle_cmd() Handle the #FINF master commands
def handle_cmd(*arg):
	global time_per_page
	global frozen
	global color
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
	elif cmd.startswith("04"):
		if cmd.replace("04","").startswith('G'):
			color = b"G"
			print("Set color to amber")
		elif cmd.replace("04","").startswith('R'):
			color = b"R"
			print("Set color to red")

# handle_sms() Handle raw sms files
def handle_sms():
	rawfiles = [f for f in os.listdir(sms_raw_path) if os.path.isfile(os.path.join(sms_raw_path, f))]
	i = 0
	page = [None] * 5
	for sms in rawfiles:
		f = open(sms_raw_path+sms, "r", encoding="utf-8")
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
	#Main loop
	while 1:
		get_sms()
		remove_long_sms()
		convert_sms_to_raw()
		clean_sms()
		handle_sms()
		time.sleep(1)
