#! /usr/bin/python -i
from dnd_character import *
print 'loading characters'
from characters import *
from dnd_party import *
import dnd_character, dnd_party, dnd_database
from npc_tables import *
from dnd_character import __path__ as path


x=armor.chainmail('mw')+magic(1)+enhance('fortification','light')

def spellmaker():
	'''dynamic function for outputting properly formatted spells to __path__/test'''
	from dnd_character import __path__
	file = open(__path__+'test','a')
	x=''
	list = []
	while x != 'close':
		data = dict()
		print "----"+str(len(list))+"----"
		for a in ['name','school','components','casting time','range','target','area','duration','save','resist']:
			x=raw_input(a+':> ')
			if x == 'close':
				file.close()
				return list
			if x=='error':
				break
			data[a]=x
		
		if x not in ['close','error']:
			result=str(data['name']).replace(' ','_')+' = spell('
			for a in data:
				result+=a.replace(' ','_')+'="'+data[a]+'", '
			result=result.rstrip(', ')+'),\n'
			file.write(result)
			file.flush()
			list.append(result)
	file.close()
	return list
	
	
def spelllistmaker(num):
	from dnd_character import __path__
	#file=open(__path__+'test','a')
	x=''
	lst=[[] for b in range(num)]
	for a in range(num):
		while True:
			data=list()
			x=raw_input(str(a)+':> ')
			if x == 'close':
				return lst
			if x.isdigit():
				break
			lst[a].append(x)
	return lst
	
def parse():
	from dnd_character import __path__ as path
	path+='region/rokugan/'
	temp = open(path+'ftemp.txt','r').readlines()
	result = [x.rstrip('\n').split(' ') for x in temp]
	#result=list(set([x+'\n' for x in result]))
	#result.sort()
	return result
	

def makename():
	lst=[]
	from dnd_character import __path__ as path
	tfile=open(path+'names.txt','a')
	while True:
		x=raw_input(':> ')
		if x == 'close':
			return lst
		tfile.write(str(x.split(' '))+'\n')
		tfile.flush()
	return lst
	
def namegen(region,gender):
	'''name generator with regional flags, regional flags also work with racial'''
	from dnd_character import __path__ as path
	import random
	
	first=[x.rstrip('\n') for x in open(path+'region/'+str(region)+'/'+str(gender)+'.txt','r').readlines()]
	last=[x.rstrip('\n') for x in open(path+'region/'+str(region)+'/last.txt','r').readlines()]
	
	return dict(first=random.choice(first), last=random.choice(last))
	