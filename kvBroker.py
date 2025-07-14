import sys
import socket
import random

def getDataFromArgs(input):
	serveFile = ""
	dataToIndex = ""
	k = -1
	for i in range(0,len(input)):
		if input[i] == '-k':
			k = input[i+1]
		elif input[i] == '-s':
			serveFile = input[i+1]
		elif input[i] == '-i':
			dataToIndex = input[i+1]
	data=[serveFile,dataToIndex,k]
	return data






def getDataFromIndexFile(File):
	f = open(File,"r")
	data=[]
	lines = [line.rstrip('\n') for line in f]
	for i in range(0,len(lines)):
		data.append(lines[i])
	f.close()
	return data




def getDataFromServerFile(File):
	f = open(File,"r")
	data=[]
	lines = [line.rstrip('\n') for line in f]
	for i in range(0,len(lines)):
		data.append(lines[i])
	f.close()
	return data



def GenerateUniqueNumbers(k,SocketListLen):
	return random.sample(range(0,SocketListLen),k)



def CommandsRead(ServersData,k,dataIndex):
	SocketList = []
	for server in ServersData:
		address,port = server.split(' ',1)
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((address,int(port)))
		SocketList.append(client_socket)


	for data in dataIndex:
		SpecificServersTakeData = GenerateUniqueNumbers(int(k),len(SocketList))
		for i in range(0,len(SpecificServersTakeData)):
			message = "PUT "+data
			SocketList[SpecificServersTakeData[i]].send(message.encode('utf-8'))
			response = SocketList[SpecificServersTakeData[i]].recv(8192).decode('utf-8')
			print(response)


	while True:
		query = input()
		for i in range(0,len(SocketList)):
			try:
				SocketList[i].send(query.encode('utf-8'))
				response = SocketList[i].recv(8192).decode('utf-8')
				if response:
					print(response)
				else:
					print("Connection Lost from ",SocketList[i])
			except(ConnectionResetError,BrokenPipeError):
				print("Connection Lost from ",SocketList[i])
			



def main():
	args = sys.argv[1:]
	sysdata = getDataFromArgs(args)
	serveFile = sysdata[0]
	dataToIndexFile = sysdata[1]
	k = sysdata[2]
	dataIndex = getDataFromIndexFile(dataToIndexFile)
	ServersData = getDataFromServerFile(serveFile)
	CommandsRead(ServersData,k,dataIndex)

if __name__ == "__main__":
    main()
