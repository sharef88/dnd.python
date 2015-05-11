'''functions and objects for the creation and manipulation of characters'''
print 'load dnd_character'
import random
from dnd_database import *
from dnd_db import *
__path__=__file__.rstrip(__name__+'.py')

def clear():
	from os import system
	from sys import platform
	if platform == 'win32':
		system('cls')
	elif platform == 'linux2':
		system('clear')

def msg(x):
	from os import system
	ipmsgpath='/home/sharef/Desktop/ipmsg206'
	x=str(x)
	system('wine '+ipmsgpath+'/ipmsg.exe /MSG 192.168.1.101 '+x)	

def itemdecoder(code):
	item=code.split(':')
	adb=eval(item[1])
	original = getattr(adb,item[2])
	mods=eval(item[3])
	if 'mw' in mods:
		result=original('mw')
		if 'magic' in mods:
			result+=magic(eval(item[4]))
			if len(mods)>mods.index('magic')+1:
				for a in mods[mods.index('magic')+1:]:
					result+=enhance(str(a[0]),str(a[1]))
	else:
		result=original()
	result.name=item[0]
	return result

def save(item,mode='file'):
	if type(item) == Character:
		#create b
		b=''
		
		#save name, line 1
		b=str(item.savename)+'\n'
		
		#basic character save
		b+='Character(save="'+str(item.savename)+'",name="'+str(item.name)+'"'
		for a in item.classlist:
			b+=','+str(a)+'='+str(item.classlist[a])
		b+=')\n'
		
		#save attributes
		b+='setatt('
		for a in item.attributes:
			b+=str(a)+'='+str(item.attributes[a])+','
		b=b.rstrip(',')
		b+=')\n'
		
		#save skills
		b+='setskill('
		for a in item.skills['skills']:
			b+=str(a)+'='+str(item.skills['skills'][a])+','
		b=b.rstrip(',');b+=')\n'
		
		#save hp
		b+='stats.hp='+str(item.hp)+'\n'
		
		b+='update()\n'
		
		#some organization, not important except to make the save file more readable
		b+='\n'
		
		#save equipment
		b+='equipment\n'
		for a in item.equipment.__dict__:
			b+=str(a)+'='+item.equipment[a].code+'\n'
		
		#more organization
		b+='\n'
		
		#save the inventory
		b+='inventory\n'
		for a in item.inventory:
			if isinstance(a,Container):
				b+='\nstart container='+a.code+'\n'
				for c in a.inventory:
					b+=c.code
					if c.name=='wallet':
						b+=str(c.price)
					b+='\n'
				b+='end container\n'
			else:
				b+=a.code
				if a.name=='wallet':
					b+=str(a.price)
				b+='\n'
		
		#a little extra, very unnescisary, but an entertaining idea, hopefully i can implement it better later
		if mode == 'file':
			file=open(__path__+'characters/'+str(item.savename),'w')
			file.writelines([b])
			file=open(__path__+'characters.py','r+')
			x=file.readlines()
			
			if 'load("'+str(item.savename)+'")\n' in x:
				pass
			else:
				x.append('load("'+str(item.savename)+'")\n')
			file.seek(0)
			file.writelines(x)
			file.close()
			return str(item.savename)+' saved'
		if mode == 'msg':
			msg(b)
			return str(item.savename)+' sent'
		if mode == 'console':
			return b
	#duh, error checking
	else:
		raise Exception('can only save characters at this time')
def load(item,state='active'):
	#open the character file 
	path=__path__+'characters/'
	if state=='active':
		pass
	elif state == 'retired':
		path+='/retired/'
	elif state == 'standby':
		path+='/standby/'
	else:
		raise Exception('bad state arg')
	
	try:
		file=open(path+str(item),'r')
	except:
		raise IOError('no such character')
	
	#get filelines...could be rewritten a bit better
	filelines=file.readlines()
	file.close()
	
	#clean the filelines
	for a in range(len(filelines)):
		filelines[a]=filelines[a].rstrip('\n')
	
	#create the character slot in char
	char[str(filelines[0])]=eval(filelines[1])
	
	character=getattr(char,str(item))
	
	#create the character
	for a in filelines[2:filelines.index('equipment')]:
		if a != '':
			exec('char.'+str(item)+'.'+filelines[filelines.index(a)])
	
	#take the rest of the file and separate it into equipment and inventory
	id=filelines.index('equipment'),filelines.index('inventory')
	equ=filelines[id[0]+1:id[1]]
	inv=filelines[id[1]+1:]
	
	#create equipment
	for a in equ:
		if a !='':	
			b=a.split('=')
			c=itemdecoder(b[1])
			character.equipment.equip(c,b[0])
	
	#create inventory, need to add support for type(Container)
	temp='inventory'
	i=0
	for a in inv:
		if a != '':
			if 'start container' in a:
				temp='inventory['+str(i)+']'
				a=a.split('=')[1]
				character.inventory.add(itemdecoder(a))
			elif 'end container' in a:
				temp='inventory'
			else:
				i+=1
				b=itemdecoder(a)
				if b.name=='wallet':
					b.price=Decimal(a.split(':')[-1])
				
				if temp=='inventory':
					character.inventory.add(b)
				else:
					eval('character.inventory.'+temp).add(b)
		
	#error checking, of course...should be rewritten
	if str(item) in char:
		getattr(char,str(item)).update()
		print 'loaded '+str(item)
		return 1
	else:
		raise Exception('error loading '+str(item))
	
class Template:
	'''template class, struct style'''
	class newdict(dict):
		'''replacement dict, mostly for looks and usage of dot notation in parallel to subscripting'''
		def __getattr__(self,attr):
			return self[attr]
		def __setattr__(self,name,val):
			self[name] = val
			
	class Attribute(dict):
		'''attribute struct'''
		def __init__(self,parent):
			self.parent = parent
			for a in self:
				self[a]=11
		def __iter__(self):
			for a in ['str','dex','con','int','wis','cha']:
				yield a
		def setatt(self, **att):
			for a in att:
				self[a] = att[a]
			self.parent.update('hp')
			self.update
		def update(self):
			'''updater for generating new, random attributes'''
			top = max(self.parent.classlist.values())
			b=0
			for a in self.parent.classlist:
				if self.parent.classlist[a] == top:
					b = a
					break
			att=self.parent.gen.att(3)
			arch=self.parent.classlist[b].arch
			for a in arch:
				self[a] = max(att)
				att.remove(max(att))
				
	class Stat(newdict):
			def __init__(self,parent):
				self.parent = parent
				for a in self:
					self[a]=0
				
			def __iter__(self):
				for a in ['level','bab','fort','ref','will','hp','load']:
					yield a
			@property
			def load(self):
				if self.parent.attributes['str'] <=10:
					maxload=self.parent.attributes['str']*10
				if self.parent.attributes['str'] >10:
					maxload=pow(1.1487,self.parent.attributes['str']-10)*100
				return int(maxload/3),int(2*maxload/3),int(maxload)
			def update(self):	
				self.fort = 0
				self.ref = 0
				self.will = 0
				for a in self.parent.classlist:
					for b in ['fort','ref','will']:
						self[b]=getattr(self.parent.classlist[a],b)+self[b]
				self.fort += self.parent.bonus('con')
				self.ref += self.parent.bonus('dex')
				self.will += self.parent.bonus('wis')
				self.bab = 0
				for a in self.parent.classlist:
					self.bab +=self.parent.classlist[a].bab
					
	class Skills(dict):
			'''skills object for character'''
			def __init__(self, parent):
				self.parent = parent
				self['skillpts']=0
				self['skills']=dict()
				self['classSkills']=list()
			def __getattr__(self,attr):
				try:
					return self[attr]
				except:
					if 'knowledge' in attr:
						b=self.parent.bonus(self.parent.attributes['int'])
					elif 'craft' in attr:
						b=self.parent.bonus(self.parent.attributes['int'])
					elif 'perform' in attr:
						b=self.parent.bonus(self.parent.attributes,['cha'])
					elif 'profession' in attr:
						b=self.parent.bonus(self.parent.attributes['wis'])
					else:
						b=self.parent.bonus(self.parent.attributes[str(getattr(skills,attr)[0])])
					try:
						return b+self.skills[attr]
					except:
						return 'not found'
			
			def __iter__(self):
				for a in self['skills']:
					yield a
			
			def setskill(self,type='non', **skill):
				for a in skill:
					if type == 'classskill':	
						self['classskill'][a]=skill[a]
					else:
						self['skills'][a]=skill[a]
				
	class Generate(object):
			con = 1
			level = 1
			dice = 6
			def __init__(self,parent,occ = 'commoner'):
				self.parent = parent
				self.con = self.parent.attributes['con']
				for a in self.parent.classlist:
					self.occ = self.parent.classlist[a]
				self.level = self.occ.level
				self.dice = self.occ.HD
			def att(self, power = 2):
				self.power = power
				c = []
				for a in range(6):
					d = []
					for b in range(4):
						d.append(random.randrange(power,7,1))
					c.append(sum(d) - min(d))
				self.rawatt = c
				return c
			
			
			def hp(self, dice=dice, lvl=level, con=con):
				if type(con) == str:
					con = self.parent.bonus(self.parent.attributes['con'])
				total=sum([dice+con]+[x+con for x in d(dice,lvl-1,[])])
				return total

	class Occupation(object):
		def __init__(self, parent, name, level):
			self.name = str(name)
			self.parent = parent
			
			#psion special case, to be fixed later, joined with wizard specializations, cleric domains and shujenga orders
			if self.name in Class.psion['dicipline']:
				self.derived = Class.psion(self.name)
			else:
				self.derived = getattr(Class,name)
			self.derived = type(self.derived)(**self.derived)
			
			#stat setting
			self.level = level
			self.bab = int(self.level*self.derived['bab'])
			self.HD = self.derived['dice']
			
			self.hp=0
			for a in range(self.level):
				self.hp+=d(self.HD)
			
			#archtype parsing
			if self.derived.has_key('arch'):
				self.arch = self.derived['arch']
			else:
				self.arch = ['str','con','dex','int','wis','cha']
			
			#save setting
			for a in self.derived['saves']:
				if self.derived['saves'][a] == 'good':
					setattr(self,a,(self.level//2)+2)
				if self.derived['saves'][a] == 'poor':
					setattr(self,a,self.level//3)
			
			#if magic class, set spells, gotta add relavent stat to Class(db)
			if 'spells' in self.derived:
				self.spells = self.derived['spells'][self.level-1][:]
				if 'known' in self.derived:
					self.known = self.derived['known'][self.level-1][:]
			
			#if esper class set spells, same issue with stat as magic classes
			if 'powers' in self.derived:
				temp=self.derived['powers'][self.level-1][:]
				try:
					self.power= Template.newdict(points = temp[0], known=temp[1], max=temp[2])
				except:
					self.power = Template.newdict(points = temp[0], known=temp[1])
			
			#set skills, gotta work on this part to determine class skills vs crossclass skills
			self.skill = self.derived['skill']
			self.skills = {}
			for a in self.derived['skills']:
				self.skills[a] = 0
				self.parent.skills['classSkills'].append(a)
			
			#cleanup
			del self.derived
		
		def __repr__(self):
			return str(self.level)
			
	class Demographics(dict):
		def __init__(self,parent):
			self.parent=parent
	class Inventory(object):
		def __init__(self,parent='none',*args):
			self.parent=parent
			self.inventory=list()
			for a in args:
				self.__dict__.append(a)

		def __iter__(self):
			for a in self.inventory:
				yield a
				
		def __repr__(self):
			return str(self.inventory)
			
		def __getattr__(self,attr):
			return self.__dict__[attr]
			
		def __getitem__(self,attr):
			return self.inventory[attr]
			
		def __setitem__(self,attr,value):
			self.inventory[attr]=value
			
		def __setattr(self,attr,val):
			self.__dict__[attr]=val

		def add(self,*args):
			for a in args:
				if a.original==False:
					self.inventory.append(a)
				else:
					self.inventory.append(a())
					
		@property
		def weight(self):
			x=0
			for a in self.inventory:
				x+=Decimal(str(a.weight))
			return x

		@property
		def value(self):
			x=0
			for a in self.inventory:
				try:
					x+=a.value
				except:
					x+=Decimal(str(a.price))
			return x

	class EquipmentInventory(object):
		def __init__(self):
			null=items.null()
			dic=dict(head=null(),hand=null(),offhand=null(),body=null(),cloak=null(),boots=null(),gloves=null(),eyes=null())
			for a in dic:
				self.__dict__[a]=dic[a]
			self.inventory = self.__dict__
		
		def __iter__(self):
			for a in self.__dict__:
				yield a
				
		def __getitem__(self,attr):
			return getattr(self,attr)
		
		def __setattr__(self,attr,val):
			if isinstance(val,Equipment):
				if attr in self.__dict__:
					if val.original==True:
						attr=attr()
					self.__dict__[attr]=val
		
		def __repr__(self):
			return str(self.__dict__)
		
		@property
		def weight(self):
			x=0
			for a in self.__dict__:
				x+=self.__dict__[a].weight
			return x
			
		@property
		def value(self):
			x=0
			for a in self.__dict__:
				x+=self.__dict__[a].price
			return x
			
		@property
		def ac(self):
			ac=0
			for a in self.__dict__:
				try:
					ac+=getattr(self,a).ac+getattr(self,a).enhancement
				except:
					pass
			return ac

		def equip(self,item,slot='default'):
			if Item in type(item).__mro__:
				if item.original == True:
					item=item()
				if slot == 'default':
					if type(item)==Weapon:
						slot='hand'
					if type(item)==Armor:
						if item.__dict__['category']=='shields':
							slot='offhand'
						elif item.__dict__['category']!='shields':
							slot='body'
				setattr(self,slot,item)		

char=Template.newdict()
class Character(object):
	'''Character generation and manipulation for d&d e3.5, created by andy wilson, aka sharef\naddclass, update, bonus, and gen(generate) are the methods of creation and manipulation\nattribute, stat and skills are character statistics'''
	def __init__(self, save='unnamed', name = 'unnamed', **kwargs): 
		'''constructor for dnd characters,\n
		attaches and integrates the following classes to the character:\nattributes\nclasslist\nstats\nskills\nequipment\ninventory'''
		
		#default kwargs saftey
		if kwargs == {}:
			kwargs={'commoner':1}
		
		#demographics
		self.savename = save
		self.name = name
		
		#stat blocks, equipment is defined through Template.Inventory
		self.skills = Template.Skills(self)
		self.attributes = Template.Attribute(self)
		self.stats = Template.Stat(self)
		self.classlist = Template.newdict()
		self.inventory = Template.Inventory(self)
		self.equipment = Template.EquipmentInventory()
		self.demographics = Template.Demographics(self)
		
		#classslist parsing
		b=1; self._1st = ''
		for a in kwargs:
			self.classlist[a]=Template.Occupation(self,a,kwargs[a])
			if b == 1:
				self._1st = a
				a=0
		
		#internal generator
		self.gen = Template.Generate(self)
		
		#update it...
		self.update('first')
		self.update('all')
	def __iter__(self):
		'''iterate through the relavent sub-instances of character:\nclasslist\nattributes\nstats\nskills\nequipment\ninventory'''
		for a in ['classlist','attributes','stats','skills','equipment','inventory']:
			yield a
	def __repr__(self):
		return self.name
	def __getattr__(self,attr):
		if attr == 'setatt':
			return getattr(self.attributes,'setatt')
		if attr == 'load':
			return self.stats.load
		try:
			return self.attributes[attr]
		except:
			try:
				return self.stats[attr]
			except:
				try:
					return self.classlist[attr]
				except:
					try:
						return getattr(self.skills,attr)
					except:
						pass
		raise Exception('not found')

	def save(self):
		'''internal save(self)'''
		return save(self)
		
	def bonus(self,stat):
		'''basic bonus(stat=type(str,int)) calculator int(stat-10)/2)'''
		if type(stat) == str:
			stat = self.attributes[stat]
		return int((stat-10)/2)
		
	def addclass(self,parent,level):
		'''addclass(parent,level), parses Class into classlist'''
		self.classlist[parent]=Template.Occupation(self,parent,level)
		self.update()
		self.update('hp')
	
	def remclass(self,parent):
		'''cleanly remove class from classlist'''
		self.classlist.pop(parent)
		self.update()
		self.update('hp')
		
	def update(self,stat='all'):
		'''updater, in the process of being rewritten, options=[statshp,skills,attribute,all,first]'''
		def hp():
			self.stats.hp = self.stats.level+self.bonus('con')
			for a in self.classlist:
				self.stats.hp+=self.classlist[a].hp
		
		def skill():
			pass
		if stat == 'stats':
			self.stats.update()
		elif stat == 'hp':
			hp()
		elif stat == 'skills':
			skill()
		elif stat == 'attribute':
			self.attributes.update()		
		elif stat == 'all':
			self.stats.update()
			skill()
			self.stats.level = 0
			for a in self.classlist:
				self.stats.level = self.stats.level+self.classlist[a].level
		elif stat == 'first':
			self.attributes.update()
			self.stats.update()
			skill()
			hp()
			self.stats.level = 0
			for a in self.classlist:
				self.stats.level = self.stats.level+self.classlist[a].level
		else:
			print 'choose from following options: saves, hp, bab, skills, attribute, first, all'
	
	def display(self,what = 'all'):
		def attribute():
			for a in self.attributes:
				print a, self.attributes[a], self.bonus(a)
		def stats():
			for a in self.stats:
				print a, self.stats[a]
		def classes():
			for a in self.classlist:
				print a, self.classlist[a]
		print '\n',self.name
		
		if what == 'all':
			for a in self:
				temp=getattr(self,a)
				print ""
				for b in temp:
					if b=='load':
						print 'load',temp.load
					else:
						try:
							print b,temp[str(b)]
						except:
							try:
								print getattr(temp,str(b))
							except:
								pass
		if what == 'attributes':
			attributes()
		if what == 'stats':
			stats()
		if what =='classes':
			classes()