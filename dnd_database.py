'''dnd database, support for characters.py'''
print '\nloading database'
from decimal import Decimal
from dnd_db import db
from dnd_class import *

	
class db1(db):
	pass

class Item(object):
	'''item type, basic for item definition, contains copyconstructor and original flags along with default item attributes'''
	name = str()
	weight = int()
	price = Decimal()
	original = True
	mods = list()
	category = tuple()
	notes = str()
	

	def __init__(self,b={},**kwargs):		
		for a in kwargs:
			if a == 'weight':
				self.setweight(Decimal(str(kwargs[a])))
			if hasattr(self,a):
				if a in ['price']:
					setattr(self,a,Decimal(kwargs[a]))
				else:
					setattr(self,a,type(kwargs[a])(kwargs[a]))
	
	def __setattr__(self, attr, val):
		'''interrupt to prevent easy changing of self.original'''
		if attr != 'original':
			self.__dict__[attr]=val
	
	def __repr__(self):
		'''return self.name'''
		if self.name == 'wallet':
			return str(self.name)+':'+str(Decimal(str(self.price)))
		else:
			return str(self.name)
	
	def __iter__(self):
		for a in dir(self):
			if type(getattr(self,a)) in [int,str,tuple,Decimal,list,property,dict]:
				if '__' not in a:
					yield a
	
	def getweight(self):
		if self.name=='wallet':
			return Decimal(self.price/50)
		else:
			if 'weight' in self.__dict__:
				return self.__dict__['weight']
			else:
				return Decimal('0')
			
	def setweight(self,arg):
		self.__dict__['weight']=Decimal(str(arg))
		
	weight = property(getweight,setweight)
		
	def __cmp__(self,x):
		if type(x) == type(self):
			if x.mods == self.mods:
				if 'magic' in self.mods:
					if isinstance(self,Armor):
						if self.enhancement==x.enhancement:
							return 0
						else:
							return 1
					if isinstance(self,Weapon):
						if self.bonus==x.bonus:
							return 0
						else:
							return 1
				else:
					return 1
				return 0
		return 1
	
	def __call__(self,x='base'):
		'''copy constructor, optional argument can only be base or mw'''
		b={}
		for a in self.__dict__:
			b[a]=type(self.__dict__[a])(self.__dict__[a])
		result=type(self)(**b)
		result.__dict__['original'] = self
		result.mods=self.mods[:]
		try:
			result.inventory = self.inventory[:]
		except:
			pass
		if x == 'mw':
			if 'mw' not in result.mods:
				result.mods.append('mw')
			if type(result)==Armor:
				result.price+=150
				result.name='masterwork '+result.name
				if result.check <0:
					result.check+=1
			if type(result)==Weapon:
				if result.vari == 'ammo':
					result.price = 70
				else:
					result.price+=300
				result.name='masterwork '+result.name
				result.bonus = (1,0)
		return result
	
	@property
	def code(self):
		code=self.name+':'
		
		if type(self)==Armor:
			code+='armor:'
			if 'magic' in self.mods:
				mod=self.enhancement
		elif type(self)==Weapon:
			code+='weapons:'
			if 'magic' in self.mods:
				mod=self.bonus[0]
		else:
			code+='items:'
				
		if self.original == True:
			temp='self'
		else:	
			temp='self.original'
			while eval(temp).original != True:
				temp+='.original'
		code+=eval(temp).name+':'
		
		code+=str(self.mods)+':'
		
		if 'magic' in self.mods:
			code+=str(mod)
	
		return code
		
class Equipment(Item):
	extra = dict()
	aura = dict()
	material = str()
	CL  = int()
	magicBonus = list()
	
class Weapon(Equipment):
	'''weapons have {dmg=tuple(), bonus=tuple(), crit=tuple(), range=int(), type=str(), vari=str(), radius=int()}'''
	dmg = tuple()
	bonus = tuple((0,0))
	crit = tuple((20,2))
	range = int()
	type = str()
	vari = str()
	radius = int()
	
class Armor(Equipment):
	'''armor has {ac=int(), maxdex=int(-1), check=int(), spell=int(), enhancement=int()}'''
	ac = int()
	mxdex = int(-1)
	check = int()
	spell = int()
	enhancement = int()

class Container(Item):
	inventory = list()
	weightless = False
	
	def __getitem__(self, arg):
		try:
			return self.inventory[arg]
		except TypeError:
			return self.__dict__[arg]
	def __setitem__(self, arg, val):
		if isinstance(arg,Item):
			if arg.original == True:
				arg=arg()
		else:
			raise Exception('containers can only hold items')
		self.inventory[arg] = val
	
	def __repr__(self):
		return str(self.name)+':'+str(self.inventory)
	
	def append(self, arg):
		if isinstance(arg,Item):
			if arg.original == True:
				arg=arg()
		else:
			raise Exception('containers can only hold items')
		self.inventory.append(arg)
		
	def add(self, *items):
		for a in items:
			if isinstance(a,Item):
				if a.original == True:
					a=a()
				self.inventory.append(a)
				
	def rem(self, *items):
		for a in items:
			for b in self.inventory:
				if b.name == a.name:
					self.inventory.pop(self.inventory.index(b))
					return 1
		return 0
	
	@property
	def weight(self):
		if self.weightless != True:
			temp=self.__dict__['weight']
			for a in self.inventory:
				temp+=Decimal(a.weight)
			return temp
		return Decimal(str(self.__dict__['weight']))
	
	@property
	def value(self):
		temp=self.price
		for a in self.inventory:
			temp+=a.price
		return temp

	
	
class mw(object):
	'''commented out, uncomment for debug module dnd_database'''
	def __repr__(self):
		return str(self.__doc__)
##	def __radd__(self,y):
##		if y.original != True:
##			if y.mods.__contains__('mw')==False:
##				y.mods.append('mw')
##				if type(y)==Armor:
##					y.price+=150
##					y.name='masterwork '+y.name
##					if y.check <0:
##						y.check+=1
##				if type(y)==Weapon:
##					if y.vari == 'ammo':
##						y.price = 70
##					else:
##						y.price+=300
##					y.name='masterwork '+y.name
##					y.bonus = (1,0)
	pass
class magic(object):
	'''default magic item enchantment, magic(bonus=[1-5])'''
	def __init__(self, bonus):
		'''self.bonus = (lambda x: (0*int(x<=0))+(x*int(0<x<=5))+(5*int(5<x)))(bonus)'''
		self.bonus = (lambda x: (0*int(x<=0))+(x*int(0<x<=5))+(5*int(5<x)))(bonus)
	
	def __radd__(self,y):
		'''main method, changes w/e you add it too'''
		
		#copy the item
		y=y()
		
		#you CANNOT manipulate originals, end of story
		if y.original != True:
			
			#if it isnt magic then make it so
			if 'magic' not in y.mods:
				
				#only mw can be enhanced with magic
				if 'mw' in y.mods:
					
					#cumulative bonus
					y.magicBonus = [self.bonus,self.bonus]
					
					#weapons and armor have slightly different requirements and price changes
					if type(y) == Weapon:
						y.price+=2000*pow(self.bonus,2)
						y.type+='m'
						y.bonus = (self.bonus,self.bonus)
					if type(y) == Armor:
						y.price+=1000*pow(self.bonus,2)
						y.enhancement=self.bonus
					
					#name changing					
					y.name=y.name.lstrip('masterwork ')
					y.name='magic '+y.name
					y.name+=' +'+str(self.bonus)
					y.mods.append('magic')
			
			#if its already magic, check to see if its being increased, otherwise pass
			if 'magic' in y.mods:
				
				#check the magic 10 limit
				if y.magicBonus[0]+self.bonus > 10:
					raise Exception('cannot have base enhancement > 10')
				
				self.chk  = y.magicBonus[1]
				
				if self.chk < self.bonus:
					y.magicBonus[1]=self.bonus
					y.magicBonus[0]+=self.bonus-self.chk
					
					y.name=y.name.replace(str(self.chk),str(self.bonus))
					
					#price and enhancement/bonus modifier
					if type(y) == Weapon:
						y.bonus=(self.bonus,self.bonus)
						y.price-=(2000*pow(self.chk,2))
						y.price+=(2000*pow(self.bonus,2))
					
					if type(y) == Armor:
						y.enhancement=self.bonus
						y.price-=(1000*pow(self.chk,2))
						y.price+=(1000*pow(self.bonus,2))
				
			
			return y

class enhance(object):
	'''in the works, similar to magic and mw, but adds extra stuff too it'''
	Armor = db(
		DMG = db(
			elemental = db(
				acid = db1(
					base = dict(price=18000, CL=3, opt='b', aura=[('abjuration','faint')], extra=[('acid resist',10)]),
					improved = dict(price=42000, CL=7, opt='b', aura=[('abjuration','moderate')], extra=[('acid resist',20)]),
					greater = dict(price=66000, CL=11, opt='b', aura=[('abjuration','moderate')], extra=[('acid resist',30)])
					),
				cold = db1(
					base = dict(price=18000, CL=3, opt='b', aura=[('abjuration','faint')], extra=[('cold resist',10)]),
					improved = dict(price=42000, CL=7, opt='b', aura=[('abjuration','moderate')], extra=[('cold resist',20)]),
					greater = dict(price=66000, CL=11, opt='b', aura=[('abjuration','moderate')], extra=[('cold resist',30)])
					),
				electric = db1(
					base = dict(price=18000, CL=3, opt='b', aura=[('abjuration','faint')], extra=[('electric resist',10)]),
					improved = dict(price=42000, CL=7, opt='b', aura=[('abjuration','moderate')], extra=[('electric resist',20)]),
					greater = dict(price=66000, CL=11, opt='b', aura=[('abjuration','moderate')], extra=[('electric resist',30)])
					),
				fire = db1(
					base = dict(price=18000, CL=3, opt='b', aura=[('abjuration','faint')], extra=[('fire resist',10)]),
					improved = dict(price=42000, CL=7, opt='b', aura=[('abjuration','moderate')], extra=[('fire resist',20)]),
					greater = dict(price=66000, CL=11, opt='b', aura=[('abjuration','moderate')], extra=[('fire resist',30)])
					),
				sonic = db1(
					base = dict(price=18000, CL=3, opt='b', aura=[('abjuration','faint')], extra=[('sonic resist',10)]),
					improved = dict(price=42000, CL=7, opt='b', aura=[('abjuration','moderate')], extra=[('sonic resist',20)]),
					greater = dict(price=66000, CL=11, opt='b', aura=[('abjuration','moderate')], extra=[('sonic resist',30)])
					)
				),
			spell_resist = db1(
				minor = dict(price='2', CL=15, opt='b', aura=[('abjuration','strong')], extra=[('spell resist',13)]),
				base = dict(price='3', CL=15, opt='b', aura=[('abjuration','strong')], extra=[('spell resist',15)]),
				improved = dict(price='4', CL=15, opt='b', aura=[('abjuration','strong')], extra=[('spell resist',17)]),
				greater = dict(price='5', CL=15, opt='b', aura=[('abjuration','strong')], extra=[('spell resist',19)])
				),
			fortification = db1(
				light = dict(price='1', CL=13, opt='b', aura=[('abjuration','strong')], extra=[('fortification',25)]),
				moderate = dict(price='3', CL=13, opt='b', aura=[('abjuration','strong')], extra=[('fortification',75)]),
				heavy = dict(price='5', CL=13, opt='b', aura=[('abjuration','strong')], extra=[('fortification',100)])
				),
			slick = db1(
				base = dict(price=3750, CL=4, opt='a', aura=[('conjuration','moderate')], extra=[('escape artist',5)]),
				improved = dict(price=15000, CL=10, opt='a', aura=[('conjuration','moderate')], extra=[('escape artist',10)]),
				greater = dict(price=33750, CL=15, opt='a', aura=[('conjuration','moderate')], extra=[('escape artist',15)])
				),
			shadow = db1(
				base = dict(price=3750, CL=5, opt='a', aura=[('illusion','faint')], extra=[('hide',5)]),
				improved = dict(price=15000, CL=10, opt='a', aura=[('illusion','moderate')], extra=[('hide',10)]),
				greater = dict(price=33750, CL=15, opt='a', aura=[('illusion','moderate')], extra=[('hide',15)])
				),
			silent_moves = db1(
				base = dict(price=3750, CL=5, opt='a', aura=[('illusion','faint')], extra=[('move silently',5)]),
				improved = dict(price=15000, CL=10, opt='a', aura=[('illusion','moderate')], extra=[('move silently',10)]),
				greater = dict(price=33750, CL=15, opt='a', aura=[('illusion','moderate')], extra=[('move silently',15)])
				),
			glamered = dict(price=2700, CL=10, opt='a', aura=[('illusion','moderate')], extra=[('glamered',True)]),
			animated =  dict(price='2', CL=12, opt='s', aura=[('transmutation','strong')], extra=[('animated',True)]),
			arrow_catching =  dict(price='1', CL=8, opt='s', aura=[('abjuration','moderate')], extra=[('arrow catching',True)]),
			arrow_deflection =  dict(price='2', CL=5, opt='s', aura=[('abjuration','faint')], extra=[('arrow deflection',True)]),
			bashing =  dict(price='1', CL=8, opt='s', aura=[('transmutation','moderate')], extra=[('bashing',True)]),
			blinding =  dict(price='1', CL=7, opt='s', aura=[('evocation','moderate')], extra=[('blinding',True)]),
			etherealness =  dict(price=49000, CL=13, opt='a', aura=[('transmutation','strong')], extra=[('etherealness',True)]),
			invulnerability =  dict(price='3', CL=14, opt='a', aura=[('abjuration','strong')], extra=[('DR', '5/magic')]),
			reflecting =  dict(price='5', CL=14, opt='s', aura=[('abjuration','strong')], extra=[('reflection',1)]),
			undead_controlling =  dict(price=49000, CL=13, opt='b', aura=[('necromancy','strong')], extra=[('undead control','26HD')]),
			wild =  dict(price='3', CL=9, opt='b', aura=[('transmutation','moderate')], extra=[('wild',True)]),
			ghost_touch =  dict(price='3', CL=15, opt='b', aura=[('transmutation','strong')], extra=[('ghost touch',True)])
			)
		)
	Weapon = db(
		DMG = db(
			alignment = db(
				anarchic = dict(price='2', CL=7, opt='a', aura=[('evocation','moderate')], extra=[('anarchic',True)]),
				axiomatic = dict(price='2', CL=7, opt='a', aura=[('evocation','moderate')], extra=[('axiomatic',True)]),
				holy = dict(price='2', CL=7, opt='a', aura=[('evocation','moderate')], extra=[('holy',True)]),
				unholy = dict(price='2', CL=7, opt='a', aura=[('evocation','moderate')], extra=[('unholy',True)])
				),
			elemental = db(
				thundering = dict(price='1', CL=5, opt='a', aura=[('necromancy','faint')], extra=[('thundering',True)]),
				shock = db1(
					base = dict(price='1', CL=8, opt='a', aura=[('evocation','moderate')], extra=[('shock',(1,6))]),
					burst = dict(price='2', CL=10, opt='a', aura=[('evocation','moderate')], extra=[('shock',(1,6)),('shock burst',True)])
					),
				frost = db1(
					base = dict(price='1', CL=8, opt='a', aura=[('evocation','moderate')], extra=[('frost',(1,6))]),
					burst = dict(price='2', CL=10, opt='a', aura=[('evocation','moderate')], extra=[('frost',(1,6)),('frost burst',True)])
					),
				flaming = db1(
					base = dict(price='1', CL=10, opt='a', aura=[('evocation','moderate')], extra=[('flaming',(1,6))]),
					burst = dict(price='2', CL=12, opt='a', aura=[('evocation','moderate')], extra=[('flaming',(1,6)),('flaming burst',True)])
					)
				),
			brilliant_energy = dict(price='4', CL=16, opt='a', aura=[('transmutation','strong')], extra=[('brilliant energy',True)]),
			dancing = dict(price='4', CL=15, opt='a', aura=[('transmutation','strong')], extra=[('dancing',True)]),
			defending = dict(price='1', CL=8, opt='m', aura=[('abjuration','moderate')], extra=[('defending',True)]),
			disruption = dict(price='2', CL=14, opt='b', aura=[('conjuration','strong')], extra=[('disruption',True)]),
			distance = dict(price='1', CL=6, opt='r', aura=[('divination','moderate')], extra=[('range',2)]),
			ghost_touch = dict(price='1', CL=9, opt='a', aura=[('conjuration','moderate')], extra=[('ghost touch',True)]),
			keen = dict(price='1', CL=10, opt='e', aura=[('transmutation','moderate')], extra=[('keen', True)]),
			ki_focus = dict(price='1', CL=8, opt='a', aura=[('transmutation','moderate')], extra=[('ki focus', True)]),
			merciful = dict(price='1', CL=5, opt='a', aura=[('conjuration','faint')], extra=[('merciful', True),('dmg',(1,6)),('vari','n')]),
			returning = dict(price='1', CL=7, opt='t', aura=[('transmutation','moderate')], extra=[('returning',True)]),
			seeking = dict(price='1', CL=12, opt='r', aura=[('diviniation','strong')], extra=[('seeking',True)]),
			speed = dict(price='3', CL=7, opt='a', aura=[('transmutation','moderate')], extra=[('haste',True)]),
			spell_storing = dict(price='1', CL=12, opt='a', aura=[('evocation','strong')], extra=[('spell storing',True)]),
			throwing = dict(price='1', CL=5, opt='m', aura=[('transmutation','faint')], extra=[('vari','t')]),
			vicious = dict(price='1', CL=9, opt='m', aura=[('necromancy','moderate')], extra=[('vicious',(1,6)),('dmg',(2,6))]),
			vorpal = dict(price='5', CL=18, opt='e', aura=[('necromancy','strong'),('transmutation','strong')], extra=[('vorpal',True)]),
			wounding = dict(price='2', CL=10, opt='a', aura=[('evocation','moderate')], extra=[('wounding',True),('con dmg',(1,6))])
			)
		)
			
	def __init__(self,enhance,power='base'):
		'''modifier-constructor, what is the power your adding to the item??'''
		self.enhance=enhance
		self.power=power
		
	def __radd__(self,y):
		'''adds the attributes to the item'''
		#copy the item
		self.result = y()
		
		#you can only enhance an item that is already magic, atleast a +1
		if 'magic' in y.mods:
			
			#check if updating a mod, if so roll the item back, needs work, can only update the latest
			#__future__
			##if self.enhance in [x[0] for x in y.mods[2:]]:
			if self.enhance == y.mods[-1][0]:
				self.result=y.original()
			
			#if its Armor, the call the armor mod
			if isinstance(y,Armor):
				if isinstance(getattr(self.Armor,self.enhance),db1):
					transferPower = getattr(getattr(self.Armor,self.enhance),self.power)
				elif isinstance(getattr(self.Armor,self.enhance),dict):
					transferPower = getattr(self.Armor,self.enhance)
				
				#difference between armor and shield mods
				if 'shields' in y.category:
					if transferPower['opt']=='a':
						raise TypeError('type error '+str(y)+' '+self.enhance)
				
				#to be specific, armor cant have certain attributes, possibly to be converted to else:
				elif 'shields' not in y.category:
					if transferPower['opt']=='s':
						raise TypeError('type error '+str(y)+' '+self.enhance)
				
				#base magic enhancement level
				self.bonus=y.enhancement
			
			#if its a weapon then call the weapon mod
			if isinstance(y,Weapon):
				if isinstance(getattr(self.Weapon,self.enhance),db1):
					transferPower = getattr(getattr(self.Weapon,self.enhance),self.power)
				elif isinstance(getattr(self.Weapon,self.enhance),dict):
					transferPower = getattr(self.Weapon,self.enhance)
				
				#check requirements
				opt = transferPower['opt']
				if opt == 'e':
					if ('s' or 'p') not in self.result.type:
						raise TypeError('type error '+str(y)+' '+self.enhance)
				elif opt == 'b':
					if 'b' not in self.result.type:
						raise TypeError('type error '+str(y)+' '+self.enhance)
				elif opt == 'r':
					if 'ranged' not in self.result.category:
						raise TypeError('type error '+str(y)+' '+self.enhance)
				elif opt == 't':
					#__future__
					pass
				
				self.bonus=y.bonus[0]
			
			#change the name
			if 'magic' in self.result.name:
				self.result.name=self.result.name.lstrip('magic')
				self.result.name = 'enhanced'+self.result.name
			
			#price and absolute magic bonus modifier
			if type(transferPower['price']) == int:
				self.result.price+=transferPower['price']
			elif type(transferPower['price']) == str:
				if self.result.magicBonus[0]+int(transferPower['price']) > 10:
					raise Exception('cannot have base enhancement > 10')
				self.result.magicBonus[0]+=int(transferPower['price'])
				
				#price changer
				if isinstance(y,Armor):
					self.result.price-=1000*self.bonus**2
					self.result.price+=1000*(self.bonus+int(transferPower['price']))**2
				if isinstance(y,Weapon):
					self.result.price-=2000*self.bonus**2
					self.result.price+=2000*(self.bonus+int(transferPower['price']))**2
			
			#if extra or aura arent there, put them there
			for a in ['extra','aura']:
				if a not in self.result.__dict__:
					self.result.__dict__[a]=dict()
				
			#extra abilities for parsing into the character, needs work on the parsing end
			for a in transferPower['extra']:
				self.result.__dict__['extra'][a[0]] = a[1]
			
			#add current power to mods
			self.result.mods.append((self.enhance,self.power))
			
			#aura changer
			strength = ['faint','moderate','strong']
			temp=transferPower['aura']
			for a in temp:
				if a[0] in self.result.__dict__['aura']:
					if strength.index(a[1])>strength.index(self.result.__dict__['aura'][a[0]]):
						self.result.__dict__['aura'][a[0]]=a[1]
				else:
					self.result.__dict__['aura'][a[0]]=a[1]
			
			#the end result
			return self.result
		else:
			#return error code
			return -1
				
class scroll(Item):
	basePrice=25
	maxLvl=9
	def _clschk(self,creator):
		import dnd_character
		temp=dict()
		if isinstance(creator,dnd_character.Character):
			for a in creator.classlist:
				if 'spells' in getattr(Class,a):
					temp[a]=getattr(creator.classlist[a],'level')
			temp=temp.items()
			temp.sort(lambda x,y:cmp(x[1],y[1]))
			try:
				return temp[0]
			except:
				raise TypeError('cannot make scrolls')
		raise TypeError('must be character')
	
	def __init__(self, spell, creator, level=None):
		workingClass=self._clschk(creator)
		if level > workingClass[1]:
			self.level=workingClass[1]
		else:
			self.level = level
		#make the working spell list
		if workingClass[0] in ['wizard','sorcerer']:
			tempSpellList= getattr(spelllist,'wizard_sorcerer')
		else:
			tempSpellList= getattr(spelllist,workingClass[0])
		
		#check to see if the spell is in the working spell list
		if spell in [x for x in tempSpellList]:
			self.spell=getattr(tempSpellList,spell)
			self.spellType=self.spell.type
			if self.spell.level > maxLvl:
				raise ValueError()
				
	def __repr__(self):
		return 'scroll of'+str(self.spell.name)

print '\tload weapons'
weapons = db(
	PHB = db(
		simple = db(
			unarmed = db(	
				gauntlet = Weapon(name = 'gauntlet', price = 2, dmg = (1,3), crit=(20,2), weight = 1, type ='b', category=('simple','unarmed')),
				unarmed_strike = Weapon(name='unarmed strike', dmg = (1,3), vari = 'n', crit = (20,2), type = 'b', category=('simple','unarmed'))
				),
			lightmelee = db(
				dagger = Weapon(name='dagger',price=2, dmg=(1,4), crit=(19,2), range=10, weight=1, type='sp', category=('simple','lightmelee')),
				katar = Weapon(name='punching dagger', price=2, dmg=(1,4), crit=(20,3), weight=1, type='p', category=('simple','lightmelee')),
				spiked_gauntlet = Weapon(name='spiked gauntlet',price=5, dmg=(1,4), crit = (20,2), weight =1, type='p', category=('simple','lightmelee')),
				light_mace = Weapon(name='light mace', price=5, dmg=(1,6), crit=(20,2), weight=4, type='b', category=('simple','lightmelee')),
				sickle = Weapon(name='sickle', price=6, dmg=(1,6), crit=(20,2), weight=2, type='s', category=('simple','light elee'))
				),
			onehandmelee = db(
				club = Weapon(name='club', dmg=(1,6), crit=(20,2), range=10, weight=3, type='b', category=('simple','onehandedmelee')),
				heavy_mace = Weapon(name='heavy mace', price=12, dmg=(1,8), crit=(20,2), weight=8, type='b', category=('simple','onehandedmelee')),
				morningstar = Weapon(name='morningstar', price=8, dmg=(1,8), crit=(20,2), weight=6, type='bp', category=('simple','one andedmelee')),
				shortspear = Weapon(name='shortspear', price=1, dmg=(1,6), crit=(20,2), range=20, weight=3, type='p', category=('simple','onehandedmelee'))
				),
			twohandmelee = db(
				longspear = Weapon(name='longspear', price=5, dmg=(1,8), crit=(20,3), weight=9, type='p', vari='r', category=('simple','twohandedmelee')),
				quarterstaff = Weapon(name='quarterstaff', dmg=(1,6), crit=(20,2), weight=4, type='b', vari='d', category=('simple','twohanded melee')),
				spear = Weapon(name='spear', price=2, dmg=(1,8), crit=(20,3), range=20, weight=6, type='p', category=('simple','twohandedmelee'))
				),
			ranged = db(
				heavy_crossbow = Weapon(name='heavy crossbow', price=50, dmg=(1,10), crit=(19,2), range=120, weight=8, type='p', category=('simple','ranged')),
				light_crossbow = Weapon(name='light crossbow', price=35, dmg=(1,8), crit=(19,2), range=80, weight=4, type='p', category=('simple','ranged')),
				dart=Weapon(name='dart', price='0.05', dmg=(1,4), crit=(20,2), range=20, weight='0.5', type='p', vari='t', category=('simple','ranged')),
				javelin=Weapon(name='javelin', price=1, dmg=(1,6), crit=(20,2), range=30, weight=2, type='p', vari='t', category=('simple','ranged')),
				sling=Weapon(name='sling', dmg=(1,4), crit=(20,2), range=50, weight=0, type='b', category=('simple','ranged')),
				bolts=Weapon(name='crossbow bolts', price=1, weight=1, vari='ammo', category=('simple','ranged')),
				bullets=Weapon(name='sling bullets', price='0.1', weight=5, category=('simple','ranged'))
				)
			),
		martial = db(
			lightmelee = db(
				throwing_axe = Weapon(name='throwing axe', price=8, dmg=(1,6), crit=(20,2), range=10, weight=2, type='s', category=('martial','lightmelee')),
				light_hammer = Weapon(name='light hammer', price=1, dmg=(1,4), crit=(20,2), range=20, weight=2, type='b', category=('martial','lightmelee')),
				handaxe = Weapon(name='handaxe', price=6, dmg=(1,6), crit=(20,3), weight=3, type='s', category=('martial','lightmelee')),
				kukri = Weapon(name='kukri', price=8, dmg=(1,4), crit=(18,2), weight=2, type='s', category=('martial','lightmelee')),
				light_pick = Weapon(name='light pick', price=4, dmg=(1,4), crit=(20,4), weight=3, type='p', category=('martial','lightmelee')),
				sap = Weapon(name='sap', price=1, dmg=(1,6), crit=(20,2), weight=2, type='b', vari='n', category=('martial','lightmelee')),
				light_shield = Weapon(name='light shield', dmg=(1,3), crit=(20,2), type='b', category=('martial','lightmelee')),
				spiked_armor = Weapon(name='spiked armor', dmg=(1,6), crit=(20,2), type='p', category=('martial','lightmelee')),
				light_spiked_shield = Weapon(name='light spiked shield', dmg=(1,4), crit=(20,2), type='p', category=('martial','lightmelee')),
				short_sword = Weapon(name='short sword', price=10, dmg=(1,6), crit=(19,2), weight=2, type='p', category=('martial','lightmelee'))
				),
			onehandmelee = db(
				battleaxe = Weapon(name='battleaxe', price=10, dmg=(1,8), crit=(20,3), weight=6, type='s', category=('martial','onehandmelee')),
				flail = Weapon(name='flail', price=8, dmg=(1,8), crit=(20,2), weight=5, type='b', category=('martial','onehandmelee')),
				longsword = Weapon(name='longsword', price=15, dmg=(1,8), crit=(19,2), weight=4, type='s', category=('martial','onehandmelee')),
				heavy_pick = Weapon(name='heavy pick', price=8, dmg=(1,6), crit=(20,4), weight=6, type='p', category=('martial','onehandmelee')),
				rapier = Weapon(name='rapier', price=20, dmg=(1,6), crit=(18,2), weight=2, type='p', category=('martial','onehandmelee')),
				scimitar = Weapon(name='scimitar',price=15, dmg=(1,6), crit=(18,2), weight=4, type='s', category=('martial','onehandmelee')),
				heavy_shield = Weapon(name='heavy shield', dmg=(1,4), crit=(20,2), type='b', category=('martial','onehandmelee')),
				heavy_spiked_shield = Weapon(name='heavy spiked shield', dmg=(1,6), crit=(20,2), type='p', category=('martial','onehandmelee')),
				trident = Weapon(name='trident', price=15, dmg=(1,8), crit=(20,2), weight=4, type='p', category=('martial','onehandmelee')),
				warhammer = Weapon(name='warhammer', price=12, dmg=(1,8), crit=(20,3), weight=5, type='b', category=('martial','onehandmelee'))
				),
			twohandmelee = db(
				falchion = Weapon(name='falchion', price=75, dmg=(2,4), crit=(18,2), weight=8, type='s', category=('martial','twohandmelee')),
				glaive = Weapon(name='glaive', price=8, dmg=(1,10), crit=(20,3), weight=10, type='s', vari='r', category=('martial','twohandmelee')),
				greataxe = Weapon(name='greataxe', price=20, dmg=(1,10), crit=(20,3), weight=12, type='s', category=('martial','twohandmelee')),
				greatclub = Weapon(name='greatclub', price=5, dmg=(1,10), crit=(20,2), weight=8, type='b', category=('martial','twohandmelee')),
				heavy_flail = Weapon(name='heavy flail', price=15, dmg=(1,10), crit=(19,2), weight=10, type='b', category=('martial','twohandmelee')),
				greatsword = Weapon(name='greatsword', price=50, dmg=(2,6), crit=(19,2), weight=8, type='s', category=('martial','twohandmelee')),
				guisarme = Weapon(name='guisarme', price=9, dmg=(2,4), crit=(20,3), weight=12, type='s', vari='r', category=('martial','twohandmelee')),
				halberd = Weapon(name='halberd', price=10, dmg=(1,10), crit=(20,3), weight=12, type='sp', category=('martial','twohandmelee')),
				lance = Weapon(name='lance', price=10, dmg=(1,8), crit=(20,3), weight=10, type='p', vari='r', category=('martial','twohandmelee')),
				ranseur = Weapon(name='ranseur', price=10, dmg=(2,4), crit=(20,3), weight=12, type='p', vari='r', category=('martial','twohandmelee')),
				scythe = Weapon(name='scythe', price=18, dmg=(2,4), crit=(20,4), weight=10, type='sp', category=('martial','twohandmelee'))
				),
			ranged = db(
				longbow = Weapon(name='longbow', price=75, dmg=(1,8), crit=(20,3), range=100, weight=3, type='p', category=('martial','ranged')),
				composite_longbow = Weapon(name='composite longbow', price=100, dmg=(1,8), crit=(20,3), range=110, weight=3, type='p', category=('martial','ranged')),
				shortbow = Weapon(name='shortbow', price=30, dmg=(1,6), crit=(20,3), range=60, weight=2, type='p', category=('martial','ranged')),
				composite_shortbow = Weapon(name='composite shortbow', price=75, dmg=(1,6), crit=(20,3), range=70, type='p', category=('martial','ranged')),
				arrows = Weapon(name='arrows', price=1, weight=3, vari='ammo', category=('martial','ranged'))
				)
			),
		exotic = db(
			lightmelee = db(
				kama = Weapon(name='kama', price=2, dmg=(1,6), crit=(20,2),  weight=2, type='s', category=('exotic','lightmelee')),
				nunchaku = Weapon(name='nunchaku', price=2, dmg=(1,6), crit=(20,2), weight=2, type='b', category=('exotic','lightmelee')),
				sai = Weapon(name='sai', price=1, dmg=(1,4), crit=(20,2), range=10, weight=1, type='b', category=('exotic','lightmelee')),
				siangham = Weapon(name='siangham', price=3, dmg=(1,6), crit=(20,2), weight=1, type='p', category=('exotic','lightmelee'))
				),
			onehandmelee = db(
				bastard_sword = Weapon(name='bastard sword', price=35, dmg=(1,10), crit=(19,2), weight=6, type='s', category=('exotic','onehandmelee')),
				dwarven_waraxe = Weapon(name='dwarven waraxe', price=30, dmg=(1,10), crit=(20,3), weight=8, type='s', category=('exotic','onehandmelee')),
				whip = Weapon(name='whip', price=1, dmg=(20,2), crit=(20,2), weight=2, type='s', vari='r', category=('exotic','onehandmelee'))
				),
			twohandmelee = db(
				orc_double_axe = Weapon(name='orc double axe', price=60, dmg=(1,8), crit=(20,3), weight=15, type='s', vari='d', category=('exotic','twohandmelee')),
				spiked_chain = Weapon(name='spiked chain', price=25, dmg=(2,4), crit=(20,2), weight=10, type='p',vari='rt', category=('exotic','twohandmelee')),
				dire_flail = Weapon(name='dire flail',  price=90, dmg=((1,8),(1,8)), crit=(20,2), weight=10, type='bp', vari='d', category=('exotic','twohandmelee')),
				gnome_hooked_hammer = Weapon(name='gnome hooked hammer', price = 20, dmg=((1,8),(1,8)), crit=((20,3),(20,4)), weight=6, type='bp',vari='d', category=('exotic','twohandmelee')),
				two_bladed_sword = Weapon(name='two bladed sword',  price=100, dmg=(1,8), crit=(19,2), weight=10, type='s', vari='d', category=('exotic','twohandmelee')),
				dwarven_urgrosh = Weapon(name='dwarven urgrosh', price=50, dmg=((1,8),(1,6)), crit=(20,3), weight=12, type='sp', vari='d', category=('exotic','twohandmelee'))
				),
			ranged = db(
				bolas = Weapon(name='bolas', price=5, dmg=(1,4), crit=(20,2), range=10, weight=2, type='b', vari='nt', category=('exotic','ranged')),
				hand_crossbow = Weapon(name='hand crossbow', price=100, dmg=(1,4), crit=(19,2), range=30, weight=2, type='p', category=('exotic','ranged')),
				heavy_repeating_crossbow = Weapon(name='heavy repeating crossbow', price=400, dmg=(1,10), crit=(19,2), range=120, weight=12, type='p', category=('exotic','ranged')),
				light_repeating_crossbow = Weapon(name='light repeating crossbow', price=250, dmg=(1,8), crit=(19,2), range=80, weight=6, type='p', category=('exotic','ranged')),
				net = Weapon(name='net', price=20, range=10, weight=6, vari='t', category=('exotic','ranged')),
				shuriken = Weapon(name='shuriken', price=1, dmg=(1,2), crit=(20,2), range=12, weight='0.5', type='p', vari='t', category=('exotic','ranged'))
				)
			)
		),
	DMG = db(
		asian = db(
			simple = db(
				ranged = db(
					blowgun = Weapon(name='blowgun', price=1, dmg=(1,1), crit=(20,2), range=10, weight=2, type='p', category=('simple','ranged')),
					needles = Weapon(name='blowgun needles', price=1, vari='ammo', category=('simple','ranged'))
					)
				),
			martial = db(
				lightmelee = db(
					wakizashi = Weapon(name='wakizashi',  price=300, dmg=(1,6), crit=(19,2), weight=3, type='s', mods=['mw'], bonus=(1,0), category=('martial','lightmelee'))
					)
				),
			exotic = db(
				lightmelee = db(
					kusari_gama = Weapon(name='kusari-gama', price=10, dmg=(1,6), crit=(20,2), weight=3, type='s', vari='r', category=('exotic','lightmelee'))
					),
				onehandmelee = db(
					katana = Weapon(name='katana', price=400, dmg=(1,10), crit=(19,2), weight=6, type='2', mods=['mw'], bonus=(1,0), category=('exotic','onehandmelee'))
					)
				)
			),
		renaissance = db(
			exotic = db(
				onehandrange = db(
					pistol = Weapon(name='pistol', price=250, dmg=(1,10), crit=(20,3), range=50, weight=3, type='p', category=('exotic','firearm'))
					),
				twohandrange = db(
					musket = Weapon(name='musket', price=500, dmg=(1,12), crit=(20,3), range=150, weight=10, type='p', category=('exotic','firearm'))
					)
				),
			explosives = db(
				bomb = Weapon(name='bomb', price=150, dmg=(2,6), range=10, weight=1, type='f', vari='t', radius=5, category=('simple', 'explosive')),
				smoke_bomb = Weapon(name='smoke bomb', price=70, range=10, weight=1, vari='t', category=('simple', 'explosive'))
				)
			),
		modern = db(
			exotic = db(
				onehandrange = db(
					automatic_pistol = Weapon(name='automatic pistol', dmg=(2,6), crit=(20,2), range=40, weight=3, type='p', category=('exotic','firearm')),
					revolver = Weapon(name='revolver', dmg=(2,8), crit=(20,2), range=30, weight=3, type='p', category=('exotic','firearm'))
					),
				twohandrange = db(
					hunting_rifle = Weapon(name='hunting rifle', dmg=(2,10), crit=(20,2), range=80, weight=8, type='p', category=('exotic','firearm')),
					automatic_rifle = Weapon(name='automatic rifle', dmg=(2,8), crit=(20,2), range=80, weight=8, type='p', category=('exotic','firearm')),
					shotgun = Weapon(name='shotgun', dmg=(2,8), crit=(20,2), range=30, weight=7, type='p', category=('exotic','firearm')),
					grenade_launcher = Weapon(name='grenade launcher', range=70, weight=7, category=('exotic','firearm'))
					)
				),
			explosives = db(
				dynamite = Weapon(name='dynamite', dmg=(3,6), range=10, weight=1, type='b', vari='t', radius=5, category=('simple','explosive')),
				fragmentation_grenade = Weapon(name='fragmentation grenade', dmg=(4,6), range=10, weight=1,  type='s', vari='t', radius=20, category=('simple', 'explosive')),
				smoke_grenade = Weapon(name='smoke grenade', range=10, weight=2, vari='t', radius=20, category=('simple','explosive'))
				)
			),
		future = db(
			exotic = db(
				onehandrange = db(
					laser_pistol = Weapon(name='laser pistol', dmg=(3,6), crit=(20,2), range=40, weight=2, category=('exotic','firearm'))
					),
				twohandrange = db(
					antimatter_rifle = Weapon(name='antimatter rifle', dmg=(6,8), crit=(20,2), range=120, weight=10, category=('exotic','firearm')),
					flamer = Weapon(name='flamer', dmg=(3,6), crit=(20,2), range=20, weight=8, type='f', category=('exotic','firearm')),
					laser_rifle = Weapon(name='laser rifle', dmg=(3,8), crit=(20,2), range=100, weight=7, category=('exotic','firearm'))
					)
				)
			)
		),
	OA = db(
		martial = db(
			twohandmelee = db(
				nagamaki = Weapon(name='nagamaki', price = 8, dmg = (2,4), crit = (20,3), weight = 10, type = 's', category=('martial','twohandmelee')),
				naginata = Weapon(name='naginata', price = 10, dmg = (1,10), crit = (20,3), weight = 15, type = 's', vari='r', category=('martial','twohandmelee'))
				)
			)
		)
	)
print '\tload armor'
armor = db(
	light = db(
		padded = Armor(name='padded armor', price=5, ac=1, maxdex=8, check=0, spell=5, weight=10, category=('light')),
		leather = Armor(name='leather armor', price=10, ac=2, maxdex=6, check=0, spell=10, weight=15, category=('light')),
		studded_leather = Armor(name='studded leather armor', price=25, ac=3, maxdex=5, check=-1, spell=15, weight=20, category=('light')),
		chain_shirt = Armor(name='chain shirt', price=100, ac=4, maxdex=4, check=-2, spell=20, weight=25, category=('light'))
		),
	medium = db(
		hide = Armor(name='hide armor', price=15, ac=3, maxdex=4, check=-3, spell=20, weight=25, category=('medium')),
		scale_mail = Armor(name='scale mail', price=50, ac=4, maxdex=3, check=-4, spell=25, weight=30, category=('medium')),
		chainmail = Armor(name='chainmail', price=150, ac=5, maxdex=2, check=-5, spell=30, weight=40, category=('medium')),
		breastplate = Armor(name='breastplate', price=200, ac=5, maxdex=3, check=-4, spell=25, weight=30, category=('medium'))
		),
	heavy = db(
		splint_mail = Armor(name='splint mail', price=200, ac=6, maxdex=0, check=-7, spell=40, weight=45, category=('heavy')),
		banded_mail = Armor(name='banded mail', price=250, ac=6, maxdex=1, check=-6, spell=35, weight=35, category=('heavy')),
		half_plate = Armor(name='half plate', price=600, ac=7, maxdex=0, check=-7, spell=40, weight=50, category=('heavy')),
		full_plate = Armor(name='full plate', price=1500, ac=8, maxdex=1, check=-6, spell=35, weight=50, category=('heavy'))
		),
	shields = db(
		buckler = Armor(name='buckler', price=15, ac=1, check=-1, spell=5, weight=5, category=('shields')),
		light_wooden = Armor(name='light wooden shield', price=3, ac=1, check=-1, spell=5, weight=5, category=('shields')),
		light_steel = Armor(name='light steel shield', price=9, ac=1, check=-1, spell=5, weight=6, category=('shields')),
		heavy_wooden = Armor(name='heavy wooden shield', price=7, ac=2, check=-2, spell=15, weight=10, category=('shields')),
		heavy_steel = Armor(name='heavy steel shield', price=20, ac=2, check=-2, spell=15, weight=15, category=('shields')),
		tower = Armor(name='tower shield', price=30, ac=4, maxdex=2, check=-10, spell=50, weight=45, category=('shields'))
		)
	)
print '\tload items'
items = db(
	null=Item(name='null',price=0,weight=0,notes='null item, placeholder'),
	wallet=Item(name='wallet',price=0),
	adventuring = db(
		backpack = Container(name='backpack', price=2, weight=2),
		barrel = Container(name='barrel', price=2, weight=30),
		basket = Container(name='basket', price='0.4', weight=1),
		bedroll = Item(name='bedroll', price='0.1', weight=5),
		bell = Item(name='bell', price=1),
		winter_blanket = Item(name='winter blanket', price='0.5', weight=3),
		block_tackle = Item(name='block and tackle', price=5, weight=5),
		wine_bottle = Item(name='glass wine bottle', price=2),
		bucket = Container(name='bucket', price='0.5', weight=2),
		caltrops = Item(name='caltrops', price=1, weight=2),
		candle = Item(name='candle', price='0.01'),
		canvas = Item(name='canvas', price='0.1', weight=1),
		map_case = Container(name='map or scroll case', price=1, weight='0.5'),
		chain = Item(name='10 ft chain', price=30, weight=2),
		chalk = Item(name='1 piece of chalk', price='0.01'),
		chest = Container(name='chest', price=2, weight=25),
		crowbar = Item(name='crowbar', price=2, weight=5),
		firewood = Item(name='one day worth of firewood', price='0.01', weight=20),
		fishhook = Item(name='fish hook', price='0.1'),
		fishing_net = Item(name='25 sq. ft. fishing net', price=4, weight=5),
		flask = Container(name='flask', price='0.03', weight='1.5'),
		flint_and_steel = Item(name='flint and steel', price=1),
		grappling_hook = Item(name='grappling hook', price=1, weight=4),
		hammer = Item(name='hammer',price='0.5', weigh=2),
		ink = Item(name='1 oz vial of ink', price=8),
		inkpen = Item(name='inkpen', price='0.1'),
		clay_jug = Container(name='clay jug', price='0.03', weight=9),
		ladder = Item(name='10 ft ladder', price='0.05', weight=20),
		common_lamp = Item(name='common lamp', price='0.1', weight=1),
		bullseye_lantern = Item(name='bullseye lantern', price=12, weight=3),
		hooded_lantern = Item(name='hooded lantern', price=7, weight=2),
		very_simple_lock = Item(name='very simple lock', price=20, weight=1),
		average_lock = Item(name='average lock', price=40, weight=1),
		good_lock = Item(name='good lock', price=80, weight=1),
		amazing_lock = Item(name='amazing lock', price=150, weight=1),
		manacles = Item(name='manacles', price=15, weight=2),
		masterwork_manacles = Item(name='masterwork manacles', price=50, weight=2),
		small_steel_mirror = Item(name='small steel mirror', price=10, weight='0.5'),
		clay_tankard = Item(name='clay tankard', price='0.02', weight=1),
		oil = Item(name='1 pint flask of oil', price='0.1', weight=1),
		paper = Item(name='1 sheet of paper', price='0.4'),
		parchment = Item(name='1 sheet of parchment', price='0.2'),
		miners_pick = Item(name="miner's pick", price=3, weight=10),
		clay_pitcher = Item(name='clay pitcher', price='0.02', weight=5),
		piton = Item(name='piton', price='0.1', weight='0.5'),
		pole = Item(name='10 foot pole', price='0.2', weight=8),
		iron_pot = Item(name='iron pot', price='0.5', weight=10),
		belt_pouch = Container(name='belt pouch', price=1, weight='0.5'),
		portable_ram = Item(name='portable ram', price=10, weight=20),
		trail_rations = Item(name='one day of trail rations', price='0.5', weight=1),
		hempen_rope = Item(name='50 ft hempen rope', price=1, weight=10),
		silk_rope = Item(name='50 ft silk rope', price=10, weight=5),
		sack = Container(name='sack', price='0.1', weight='0.5'),
		sealing_wax = Item(name='sealing wax', price=1, weight=1),
		sewing_needle = Item(name='sewing needle', price='0.5'),
		signal_whistle = Item(name='signal whistle', price='0.8'),
		signet_ring = Item(name='signet ring', price=5),
		sledge = Item(name='sledge', price=1, weight=10),
		soap = Item(name='1 lb soap', price='0.5', weight=1),
		spade = Item(name='shovel', price=2, weight=8),
		spyglass = Item(name='spyglass', price=1000, weight=1),
		tent = Item(name='tent', price=10, weight=20),
		torch = Item(name='torch', price='0.01', weight=1),
		vial = Item(name='vial', price=1, weight='0.1'),
		waterskin = Item(name='waterskin', price=1, weight=4),
		whetstone = Item(name='whetstone', price='0.02', weight=1)
		),
	alchemy = db(
		acid = Item(name='flask of acid', price=10, weight=1),
		alchemists_fire = Item(name="flask of alchemist's fire", price=20, weight=1),
		antitoxin = Item(name='vial of antitoxin', price=50),
		everburning_torch = Item(name='everburning torch', price=110, weight=1),
		holy_water = Item(name='flask of holy water', price=25, weight=1),
		smokestick = Item(name='smokestick', price=20, weight='0.5'),
		sunrod = Item(name='sunrod', price=2, weight=1),
		tanglefoot_bag = Item(name='tanglefoot bag', price=50, weight=4),
		thunderstone = Item(name='thunderstone', price=30, weight=1),
		tindertwig = Item(name='tindertwig', price=1)
		),
	tools = db(
		),
	clothing = db(
		),
	food_drink = db(
		),
	mounts = db(
		),
	transport = db(
		),
	)
print '\tcreating special items'
class special(object):
	'''special item definitions, most of them will be 'original' '''
	#standard kit, every adventurer needs one :P
	standard_kit = items.backpack()
	standard_kit.add(items.bedroll, items.waterskin, items.flint_and_steel, items.silk_rope,  items.sunrod, items.sunrod,items.sack)
	standard_kit.__dict__['original']=True
	
	
print '\tdatabase loaded\n\n'