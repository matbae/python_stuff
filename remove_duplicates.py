#!/usr/bin/python
#
# remove duplicates

import sys
import getopt
from os import walk
import os
import hashlib
import datetime

def log(logstring,logging,logfile):
	if logging:
		output = open(logfile,'a')
		output.write(str(datetime.datetime.now()) + ': ' + logstring + os.linesep)
		output.close()
		
		
def process(files,logging, logfile):
	
	md5list = []
	for file in files:
		md5 = hashlib.md5()
		log('Processing ' + str(file),logging,logfile)
		input = open(file,'rb')
		md5.update(input.read())
		digest = md5.hexdigest()
		log('Digest for ' + str(file) + ' is ' + str(digest), logging, logfile)
		if digest in md5list:
			log('Deleting ' + file, logging, logfile)
			try:
				print('removing file ' + file)
				os.remove(file)
			except OSError:
				log('Failed to deleting ' + file, logging, logfile)
		else:
			print('Adding file ' + file + ' to md5list')
			md5list.append(digest)
	log('md5list is ' + str(md5list), logging, logfile)

def usage():
	print('To be constructed')
	
try:
    opts, args = getopt.getopt(sys.argv[1:], 'l:i:h', ['logfile=','inputdir=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

logging = False
logfile = ""
	
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-i', '--inputdir'):
        inputdir = arg
    elif opt in ('-l', '--logfile'):
        logging = True
        logfile = arg
    else:
        usage()
        sys.exit(2)
		
files = []
for (dirpath, dirnames, filenames) in walk(inputdir):
    dirpath = dirpath + "/"
    files.extend([dirpath+x for x in filenames])

log(str(len(files)) + ' files in files',logging,logfile)	

process(files, logging, logfile)