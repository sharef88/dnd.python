from dnd_character import *

class init(list):
	def __init__(self,party=None,*args, **kwargs):
		if isinstance(party,Party):
			if len(party.members)!=len(args):
				raise Exception('not enough numbers')
			for a in range(len(args)):
				kwargs[party.members[a].savename]=args[a]
		elif party==None:
			pass
		else:
			raise Exception('error in var party')
		
		self.original=kwargs.items()
		self.value = []
		print self.original
		for a in self.original:
			#expand self.original to include the dex score, if there is one
			#~feats~ need actual initiative support, not just dex
			try:
				try:
					#is it a character that has dex score?
					dex=getattr(char,str(a[0])).bonus('dex')
				except:
					#otherwise .... characters that exist get preference to ones that dont
					dex=0
				#the tuple is good!
				self.original[self.original.index(a)]=(a[0],a[1]+dex,dex)
			except:
				pass
		
		#sort it
		self.original.sort(lambda x,y:cmp(d(20),d(20)))
		print self.original
		self.original.sort(lambda x,y:cmp(y[2],x[2]))
		print self.original
		self.original.sort(lambda x,y:cmp(y[1],x[1]))
		
		#attach the character and make more lists
		for a in self.original:
			self.value.append(a[0])
			try:
				self.append((getattr(char,a[0]),a[1]))
			except:
				self.append(a)
		
		print self
	def __getattr__(self,attr):
		result = 0
		b=''
		for a in self.original:
			if type(a)==tuple:
				if a[0] == attr:
					b = a[0]
					print 'tuple'
			if type(a) == str: 
				if a == attr:
					print 'string'
					b=str(a)
		try:
			result = eval(b)
		except NameError:
			result = b
		return result
	def __repr__(self):
		result = []
		for a in self:
			if type(a) == tuple:
				result.append(a[0])
		return str(result)
	def next(self):
		self.append(self.pop(0))
		self.original.append(self.original.pop(0))
		self.value.append(self.value.pop(0))
		print self[0][0]
	def add(self, *arg):
		for a in arg:
			self.original.append((a,0,0))
			self.value.append(a)
			b=a
			try:
				b=eval(a)
			except NameError:
				b=a
			self.append((b,0,0))
	def rem(self,*arg):
		for a in arg:
			index = self.value.index(a)
			del self[index]
			del self.original[index]
			del self.value[index]
	def disp(self):
		print 'self', self ; 
		print 'original', self.original
		print 'value',self.value

class Party(object):
	def __init__(self, *members):
		try:
			self.members = [char[x] for x in members]
		except:
			raise Exception(x+' does not exist in char')
	
	def __getitem__(self,arg):
		try:
			return getattr(self,arg)
		except:
			return self.members[arg]
			
	def __repr__(self):
		return str(self.members)
	
	@property
	def wealth(self):
		'''the sum of the members equipment and inventory values'''
		return sum([sum(y) for y in [(x.inventory.value,x.equipment.value) for x in self.members]])
	
	@property
	def load(self):
		'''the sum of the members equipment and inventory weight properties '''
		return sum([sum(y) for y in [(x.inventory.weight,x.equipment.weight) for x in self.members]])
			
	@property
	def capacity(self):
		'''the sum of the members load values'''
		return [sum([y[z] for y in [x.load for x in self.members]]) for z in range(3)]
			
	@property
	def level(self):
		'''the average of the members levels'''
		return int(sum([x.level for x in self.members])/len(self.members))
			
	@property
	def stats(self):
		'''wrapper for easily displaying the rest of the party properties, not needed'''
		return {'level':self.level, 'wealth':self.wealth, 'load':self.load, 'capacity':self.capacity}