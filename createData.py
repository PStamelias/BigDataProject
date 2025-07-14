import sys
import string 
import random

def getDataFromArgs(input):
	keyFileName = ""
	n = -1
	d = -1
	l = -1
	m = -1
	for i in range(0,len(input)):
		if input[i] == '-k':
			keyFileName = input[i+1]
		elif input[i] == '-n':
			n = input[i+1]
		elif input[i] == '-d':
			d = input[i+1]
		elif input[i] == '-l':
			l = input[i+1]
		elif input[i] == '-m':
			m =	input[i+1]
	data=[keyFileName,n,d,l,m]
	return data


def  generaterandomInterger():
	return random.randint(0,10000)


def  generaterandomFloat():
	return random.uniform(1.0,100.0)


def generateRandomString(l):
	try:
		l = int(l)
	except ValueError:
		print("l does not contain a number")
	n = random.randint(1,l)
	letters = string.ascii_letters 
	digits = string.digits
	sumCharacters = letters + digits
	randomString = ''.join(random.choice(sumCharacters) for i in range(0,n))
	return randomString



def getDictFromkeyFileName(keyFileName):
	NameList = []
	ValueList = []
	f = open(keyFileName,"r")
	lines = [line.rstrip('\n') for line in f]
	for i in range(0,len(lines)):
		name,value=lines[i].split(' ',1)
		NameList.append(name)
		ValueList.append(value)
	Dict = dict(zip(NameList,ValueList))
	f.close()
	return Dict


def create_key_value(d,m,Dict,l,ListOfKeys,randomD):
	data=""
	key, val = random.choice(list(Dict.items()))
	while True:
		if key not in ListOfKeys:
			ListOfKeys.append(key)
			break
		else:
			key, val = random.choice(list(Dict.items()))
	data = data + key +" : "
	if randomD==0:
		if val == "string":
			data = data + generateRandomString(l)
		elif val == "int":
			data = data + str(generaterandomInterger())
		else:
			data = data + str(generaterandomFloat())
	else:
		randomM = random.randint(1,m)
		data = data +"{"
		randomD=randomD-1
		for i in range(0,randomM):
			ListOfKeys=[]
			data = data + create_key_value(d,m,Dict,l,ListOfKeys,randomD)
			if i!=randomM-1:
				data = data +" ; "
		data = data +" } "
	return data



def lineData(keyFileName,m,d,l):
	data = ""
	try:
		m = int(m)
	except ValueError:
		print("m does not contain a number")
	try:
		l = int(l)
	except ValueError:
		print("l does not contain a number")
	try:
		d = int(d)
	except ValueError:
		print("d does not contain a number")

	randomM = random.randint(1,m)
	keyFileTypesDict = getDictFromkeyFileName(keyFileName)
	data = data +"{ "
	ListOfKeys=[]
	for i in range(0,randomM):
		keydata = ""
		randomD = random.randint(0,d)
		if randomD==0:
			data = data + create_key_value(d,m,keyFileTypesDict,l,ListOfKeys,randomD)
		else:
			data = data + create_key_value(d,m,keyFileTypesDict,l,ListOfKeys,randomD-1)
		if i!=randomM-1:
			data = data +" ; "
	data = data +" } "
	return data



def WriteToDataFile(keyFileName,n,d,l,m):
	row = "person"
	counterRow=1
	f = open("dataToIndex.txt","w")
	try:
		n = int(n)
	except ValueError:
		print("n does not contain a number")
	for i in range(0,n):
		f.write(row+str(counterRow)+" : ")
		data = lineData(keyFileName,m,d,l)
		f.write(data)
		counterRow+=1
		f.write("\n")
	f.close()



def main():
	args = sys.argv[1:]
	data = getDataFromArgs(args)
	keyFileName = data[0]
	n = data[1]
	d = data[2]
	l = data[3]
	m = data[4]
	WriteToDataFile(keyFileName,n,d,l,m)

if __name__ == "__main__":
    main()