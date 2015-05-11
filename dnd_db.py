from itertools import chain

def d(x=20,num=1,t=int()):
	import random
	'''the all important dice roller'''
	r=[]
	for a in range(num):
		r.append(random.randrange(1,x+1,1))
	if type(t)==int:
		return sum(r)
	return r
	
def namegen(region,gender):
	'''name generator with regional flags, regional flags also work with racial'''
	from dnd_character import __path__ as path
	import random
	
	first=[x.rstrip('\n') for x in open(path+'region/'+str(region)+'/'+str(gender)+'.txt','r').readlines()]
	last=[x.rstrip('\n') for x in open(path+'region/'+str(region)+'/last.txt','r').readlines()]
	
	return dict(first=random.choice(first), last=random.choice(last))

class db(dict):
	'''db class, advanced dict with transparency'''
	def __init__(self, **kwargs):
		'''emulation of dict.__init__
		self.index is the transparency dict of contained db()
		self.list==self.__dict__ is the non-transparency dict of non homogenized items'''
		#dunno how to call parent functions,,ie~ dict.__init__
		self['index'] = dict()
		self['list'] = dict()
		self['dict'] = dict()
		for a in kwargs:
			setattr(self,a,kwargs[a])
		
	
	def __repr__(self):
		'''if index is empty return self.list, else return self.index'''
		return str(self['index'])
	
	def __setattr__(self,attr,value):
		'''sorts between type(self) and not type(self)'''
		#type checking is wrong?, i use this to make sure its transparent through homogeny, so i can inherit this class to make a barrier
		if type(value) != type(self):	
			self['list'][attr] = value
			try:
				#put a duplicate reference in the search dict, potentially useless or usefull, atm manditory
				self['dict'][value.name] = value
			except AttributeError:
				pass
		if type(value) == type(self):
			self['index'][attr] = value
	
	def __getattr__(self,attr):
		'''transparency getattr, check out the code, its pretty clever'''
		#check the primary list
		if attr in self['list']:
			return self['list'][attr]
		#then check the search dict
		if attr in self['dict']:
			return self['dict'][attr]
		#check the index of sub-db
		elif attr in self['index']:
			return self['index'][attr]
		#Then go deeper
		else:
			for a in self['index']:
				try:
					return getattr(self['index'][a],attr)
				except AttributeError:
					pass
		#error...
		raise AttributeError('not found: '+str(attr))
		
	def __iter__(self):
		for a in chain((x for x in self['index']),(x for x in self['list'])):
			if a in self['index']:
				for b in self['index'][a]:
					yield b
			else:
				yield self['list'][a]
	
	#seems to return the same as above
	def itername(self):
		for a in chain((x for x in self['index']),(x for x in self['list'])):
			if a in self['index']:
				for b in self['index'][a]:
					yield b
			else:
				yield a
			
