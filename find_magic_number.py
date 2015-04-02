#!/usr/bin/python
#
# Finding out magic numbers in files.
# It does that by finding patterns in the files
# and comparing them throughout the files and 
# collecting the patterns that exist in all the files
# Don't match files of different type.
# We only read the first 20 bytes of the file because
# there is where the magic number is if it exist.

import sys
import getopt
from os import walk

numberofbytes = 20
back = False

def usage():
	print("find_magic_number.py options")
	print("")
	print("options:")
	print("\t-h --help\t\tprint this help text")
	print("")
	print("\t--inputdir=<dir_with_the_files>")
	print("")
	print("\t-r\t\trecursise the directorys")
	print("")
	print("\t-n or --numberofbytes")
	print("\t\t\tnumber of bytes to read from the")
	print("\t\t\tfile for use in the pattern discovery.")

def process_file(filename, back):
	global numberofbytes
	file = open(filename, 'rb')
	bafront = bytearray()
	baback = bytearray()
	bafront.extend(file.read(numberofbytes))
	
	if back:
		file.seek(-numberofbytes,2)
		baback.extend(file.read(numberofbytes))
		
	file.close()
	return (bafront,baback)
	
def transform(data,back):
	global numberofbytes
	# create temp
	tempf=[]
	tempb=[]
	for i in range(numberofbytes):
		tempf.append([])
		tempb.append([])
	
	for i in data:
		fdata=i[0]
		bdata=i[1]
		
		x=0
		for j in fdata:
			tempf[x].append(j)
			x+=1
			
		if back:
			x=0
			for j in bdata:
				tempb[x].append(j)
				x+=1
		
	return (tempf,tempb)

def checkEqual1(listToCheck, uniqpatterns = None,biggestpattern=()):
	# try:
		# iterator = iter(iterator)
		# first = next(iterator)
		# return all(first == rest for rest in iterator)
	# except StopIteration:
		# return True
	if len(listToCheck) == 0:
		return None
	
	if uniqpatterns is None:
		uniqpatterns = set()
	
	if len(listToCheck) == 1:
		return (listToCheck[0],True,100)
	
	i = 0
	j=0
	k = len(listToCheck)
	
	if len(uniqpatterns) > 0:
		while k > j and listToCheck[j] in uniqpatterns:
			j+=1
	if k > j:
		first = listToCheck[j]
		
		for rest in listToCheck:
			if first == rest:
				i+=1
			
		procent = (i*100)/len(listToCheck)
		if len(biggestpattern) == 0:
				biggestpattern=(first,procent)
		
		if biggestpattern[1] < procent:
			biggestpattern=(first,procent)
		uniqpatterns.add(first)
		
		if procent < 50:
			return checkEqual1(listToCheck,uniqpatterns,biggestpattern)
		else:
			return (biggestpattern[0],biggestpattern[1] == 100, biggestpattern[1])
	else:
		return (biggestpattern[0],biggestpattern[1] == 100, biggestpattern[1])
	
def find_patterns(data,back):
	newdata = transform(data,back)
	patternf = []
	patternb = []
	for i in newdata[0]:
		patternfresult = checkEqual1(i)
		patternf.append(patternfresult)
	
	if back:
		for i in newdata[1]:
			patternbresult = checkEqual1(i)
			patternb.append(patternfresult)
	
	
	return (patternf,patternb)
	
def print_pattern(pattern,back):
	x=0
	print('Front pattern')
	for i in pattern[0]:
		print(hex(i[0]) + "   " + str(i[1]) + "   " + str(i[2])+ "%")
	if back:
		print('Back pattern')
		for i in pattern[1]:
			print(hex(i[0]) + "   " + str(i[1]) + "   " + str(i[2])+ "%")

try:
    opts, args = getopt.getopt(sys.argv[1:], 'm:n:hb', ['back', 'numberofbytes=','inputdir=', 'help'])
except getopt.GetoptError:
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit(2)
    elif opt in ('-m', '--inputdir'):
        inputdir = arg
    elif opt in ('-n', '--numberofbytes'):
        numberofbytes = int(arg)
    elif opt in ('-b','--back'):
        back = True
    else:
        usage()
        sys.exit(2)
		
files = []
for (dirpath, dirnames, filenames) in walk(inputdir):
    dirpath = dirpath + "/"
    files.extend([dirpath+x for x in filenames])
	
data = []
for file in files:
	data.append(process_file(file,back))

pattern = find_patterns(data,back)
print_pattern(pattern,back)	