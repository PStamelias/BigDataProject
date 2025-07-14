import sys
import time
import socket

class Node:
	def __init__(self,key):
		self.NodeCharacter = key
		self.value = None
		self.childrenList = []


class Trie:
	def __init__(self, root_value=None):
		self.root = Node(root_value)

	def GetValueandKey(self,row):
		position=0
		for i in range(0,len(row)):
			if row[i]==':':
				position=i
				break
		key=row[:position]
		value=row
		return key,value

	def Insert(self,row):
		key,value=self.GetValueandKey(row)
		self.Insert_On_Trie(self.root,0,key,value)

	def Query(self,value):
		counter=0
		a=""
		for i in value:
			if not i.isspace():
				a+=i
		return self.Query_On_Trie(self.root,a,counter)
	
	def Insert_On_Trie(self,node,counter,key,value):
		if not node.childrenList:
			new_node=Node(key[counter])
			node.childrenList.append(new_node)
			if counter == len(key)-1:
				node.childrenList[0].value=value 
				return ;
			else:
				self.Insert_On_Trie(new_node,counter+1,key,value)
		else:
			found=False
			for i in range(0,len(node.childrenList)):
				if key[counter] == node.childrenList[i].NodeCharacter:
					found=True
					if counter == len(key)-1:
						node.childrenList[i].value=value
						return ;
					else:
						self.Insert_On_Trie(node.childrenList[i],counter+1,key,value)
			if found==False:
				new_node=Node(key[counter])
				node.childrenList.append(new_node)
				self.Insert_On_Trie(node,counter,key,value)

			
	def Query_On_Trie(self,node,key,counter):
		current_node=node
		while True:
			found=False
			for i in range(0,len(current_node.childrenList)):
				if key[counter] == current_node.childrenList[i].NodeCharacter:
					found=True
					if counter==len(key)-1:
						if current_node.childrenList[i].value==None:
							return "NOT-FOUND"
						return current_node.childrenList[i].value
					else:
						current_node=current_node.childrenList[i]
						counter=counter+1
						break
			if found==False:
				return "NOT-FOUND"


	def DeleteKey(self,node,key,counter):
		current_node=node
		while True:
			if current_node.childrenList==None:
				return "NOT FOUND"
			found=False
			for i in range(0,len(current_node.childrenList)):
				if current_node.childrenList[i].NodeCharacter==key[counter]:
					found=True
					if counter==len(key)-1:
						if current_node.childrenList[i].value==None:
							return "NOT-FOUND"
						else:
							current_node.childrenList[i].value=None
							if current_node.childrenList[i].childrenList==None:
								current_node.childrenList.pop(i)
							return "OK"
					current_node=current_node.childrenList[i]
					break
			counter+=1
			if found==False:
				return "NOT-FOUND"

	def Delete(self,value):
		counter=0
		a=""
		for i in value:
			if not i.isspace():
				a+=i
		return self.DeleteKey(self.root,a,0)


def PutDataToTrie(trie,data):
	data=data.replace("PUT",'')
	data=data.replace(" ", "")
	trie.Insert(data)


def GetDataFromTrie(trie,data):
	data=data.replace("GET",'').strip()
	t=trie.Query(data)
	return t

def DeleteDataFromTrie(trie,data):
	data=data.replace("DELETE",'').strip()
	t=trie.Delete(data)
	return t


def getListOfSubKeys(value):
	List_ofValues=[]
	value=value[1:-1]
	e=""
	counter1=0
	cut=True
	for i in range(0,len(value)):
		if i ==len(value)-1:
			e+=value[i]
			List_ofValues.append(e)
			break
		if value[i]=="{":
			counter1+=1
		if value[i]=='}':
			counter1-=1
		if  value[i]==';' and counter1==0:
			List_ofValues.append(e)
			e=""
			cut=False
			continue
		e+=value[i]
	return List_ofValues


def getValuesOfrow(row):
	write=False
	value=""
	for i in range(0,len(row)):
		if row[i]=='{':
			write=True
			value+=row[i]
			continue
		if write==True:
			value+=row[i]
	return value


def GetValueofKey(Line):
	position=Line.find(':')
	position+=1
	str=""
	for i in range(position,len(Line)):
		str+=Line[i]
	if "{" in str:
		return "NOT-FOUND"
	return str


def SearchSpecificValueOnkey(row,listof_keys,counter,lenList):
	List_ofValues=getListOfSubKeys(row)
	for i in range(0,len(List_ofValues)):
		conditionone=List_ofValues[i].find(listof_keys[counter])
		if conditionone==-1:
			continue
		current_string=List_ofValues[i][:conditionone+len(listof_keys[counter])+1]
		if "{" in current_string:
			continue
		if counter==lenList-1:
			return GetValueofKey(List_ofValues[i])
		newList_ofValues=getValuesOfrow(List_ofValues[i])
		return SearchSpecificValueOnkey(newList_ofValues,listof_keys,counter+1,lenList)
	return "NOT-FOUND"


def GetSpecificValueOnkey(row,listof_keys):
	return SearchSpecificValueOnkey(row,listof_keys,0,len(listof_keys))


def QueryDataFromTrie(trie,data):
	data=data.replace("QUERY",'').strip()
	key=""
	if "." in data:
		for i in range(0,len(data)):
			if data[i]=='.':
				break
			key+=data[i]
		listof_keys=[]
		e=""
		for i in range(0,len(data)):
			if data[i]=='.':
				listof_keys.append(e)
				e=""
			elif i==len(data)-1:
				e=e+data[len(data)-1]
				listof_keys.append(e)
				break
			else:
				e+=data[i]
		t=trie.Query(key)
		if t=="NOT-FOUND":
			return "NOT-FOUND"
		t="{"+t+"}"
		return 	GetSpecificValueOnkey(t,listof_keys)
	else:
		t=trie.Query(data)
		return t


def getDataFromArgs(input):
	ip_address = ""
	port = ""
	for i in range(0,len(input)):
		if input[i] == '-a':
			ip_address = input[i+1]
		elif input[i] == '-p':
			port = input[i+1]
	data=[ip_address,port]
	return data


def startServer(ip_address,port):
	trie = Trie()
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((ip_address,int(port)))
	server.listen(1)
	c,address  = server.accept()
	while True:
		data = c.recv(8192).decode('utf-8')
		response = ""
		if "PUT" in data:
			PutDataToTrie(trie,data)
			response="OK"
		elif "GET" in data:
			response=GetDataFromTrie(trie,data)
		elif "DELETE" in data:
			response=DeleteDataFromTrie(trie,data)
		elif "QUERY" in data:
			response=QueryDataFromTrie(trie,data)
		else:
			response = "ERROR:Unknown"
		c.send(response.encode('utf-8'))
	c.close()


def main():
	args = sys.argv[1:]
	sysdata = getDataFromArgs(args)
	ip_address = sysdata[0]
	port = sysdata[1]
	startServer(ip_address,port)

if __name__ == "__main__":
    main()
