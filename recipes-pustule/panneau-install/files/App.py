#!/usr/bin/python3

from os import listdir
from os.path import isfile, join
import time

sms_path = "/var/spool/sms/"
sms_raw_path = "/home/root/raw/"
smsfiles = ""
MAX_SMS_SIZE=140


def get_sms():
	global smsfiles
	smsfiles = [f for f in listdir(sms_path) if isfile(join(sms_path, f))]

def remove_long_sms():
	global smsfiles
	for filename in smsfiles:
		f = open(sms_path+filename)
		for lines in f:
			if 'Length = ' in lines:
				length = int(lines.replace("Length = ",""))
				if length > MAX_SMS_SIZE:
					smsfiles.remove(filename)
		f.close()

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


if __name__ == '__main__':
	get_sms()
	remove_long_sms()
	convert_sms_to_raw()
