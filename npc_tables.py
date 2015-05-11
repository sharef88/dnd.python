import random
from dnd_db import *
from dnd_character import *

class npc(object):
	
	@staticmethod
	def traits(num=1):
		'''npcs need personalities, this returns a list of npc quirks for good roleplaying'''
		table=[['distinctive scar'], ['missing tooth'], ['missing finger'], ['bad breath'],['strong body odor', 'pleasant smelling [perfumed]'],\
		['sweaty'],['hands shake'], ['unusual eye color'], ['hacking cough'], ['sneezes and sniffles'], ['particularly low voice', 'particularly high voice'],\
		['slurs words', 'lisps', 'stutters', 'enunciates very clearly'],['speaks loudly', 'whispers'],['hard of hearing'],['tattoo'],['birthmark'],\
		['unusual skin color'],['bald', 'particularly long hair'],['unusual hair color'],['walks with a limp'],['distinctive jewelry'],\
		['wears flamboyant or outlandish clothes'],['underdressed', 'overdressed'],['nervous eye twitch'],['fiddles and fidgets nervously'],\
		['whistles a lot','sings a lot'],['flips a coin'],['good posture', 'stooped back'],['tall', 'short'],['thin', 'fat'],['visible wounds or sores'],\
		['squints'],['stares off into distance'],['frequently chewing something'],['dirty and unkempt', 'clean'],['distinctive nose'],['selfish'],\
		['obsequious'],	['bookish'],['observant', 'not very observant'],['overly critical'],['passionate artist or art lover'],\
		['passionate hobbyist (fishing, hunting, gaming, animals, etc.)'],['collector (books, trophies, coins, weapons, etc.)'],\
		['skinflint', 'spendthrift'],['pessimist', 'optimist'],['drunkard', 'teetotaler'],['well mannered', 'rude'], ['jumpy'], ['foppish'],\
		['overbearing', 'aloof'], ['proud'], ['individualist', 'conformist'], ['hot tempered', 'even tempered'], ['neurotic'], ['jealous'],\
		['brave','cowardly'], ['careless'], ['curious'], ['truthful', 'liar'], ['lazy'], ['energetic','drowsy'],\
		['reverent or pious', 'irreverent or irreligious'],	['opinionated'], ['moody'], ['cruel'],\
		['uses flowery speech or long words'], ['uses the same phrases over and over'],\
		['sexist, racist, or otherwise prejudiced'], ['facinated by magic', 'distrustful of magic'],\
		['prefers members of one class over all others'], ['jokester', 'no sense of humor']]
		return [random.choice(random.choice(table)) for b in range(num)]
	
	@staticmethod
	def gearValue(lvl):
		'''this should not be modified except through source'''
		return int(['900', '2000', '2500', '3300', '4300', '5600', '7200', '9400', '12000', '16000',\
		'21000', '27000', '35000', '45000', '59000', '77000', '100000', '130000', '170000', '220000'][lvl])
		
		
		
class Community(object):
	'''a class to return a community, complete with named npcs :D'''
	def __init__(self, region,size=None):
		#this function is run when you 'instance' the class, thus Community('rokugan','thorp') runs this function
		
		self.data=dict()
		
		self.data.update(self.randomstart(size))
		self.data['power center']=self.powergen(self.data['size'])
		self.data.update(self.populationgen(self.data['size']))
		self.data['populationnumbers']=dict()
		for a in self.data['classnumbers']:
			self.data['populationnumbers'][a]=len(self.data['classnumbers'][a])
		if self.data['size'] not in ['small_city','large_city','metropolis']:
			self.data['residents']=self.genresidents(region,self.data['size'],self.data['population'],self.data['classnumbers'])
		else:
			print 'it takes too long to generate large community residents'
		
	def __repr__(self):
		#this is just a 'pretty print' for this class
		temp=self.data.copy()
		del temp['classnumbers']
		del temp['residents']
		return 'data: '+str(temp)
	
	@property
	def table(self):
		#this will be modified to have more in it, currently it is just a list of what size community names are acceptables......not sure if i have it used anywhere
		#@proerpy is a decorator that makes this look like a variable instead of a function, and you cant modify this at runtime
		return ['thorp','hamlet','village','small_town','large_town','small_city','large_city','metropolis']
	
	def randomstart(self,arg=None):
		randtable=dict(thorp=(0,10), hamlet=(11,30), village=(31,50), small_town=(51,70), large_town=(71,85), small_city=(86,95), large_city=(96,99), metropolis=(100,100))
		GPlimittable = dict(thorp=40, hamlet=100, village=200, small_town=800, large_town=3000, small_city=15000, large_city=40000, metropolis=100000)
		lst=[]
		if arg == None:
			for a in randtable:
				temp=randtable[a][1]-randtable[a][0]+1
				for b in range(temp):
					lst.append(a)
			size=random.choice(lst)
		else:
			if arg in self.table:
				size=arg
		GPlimit=GPlimittable[size]
		return dict(size=size, GPlimit=GPlimit)
		
	def powergen(self,arg):
		#this function (method) returns who holds power in a community
		modtable=dict(thorp=(-1,1), hamlet=(0,1), village=(1,1), small_town=(2,1), large_town=(3,1), small_city=(4,2), large_city=(5,3), metropolis=(6,4))
		randtable=dict(lawful_good=(1,35), neutral_good=(36,39), chaotic_good=(40,41), lawful_neutral=(42,61), true_neutral=(62,63),
			chaotic_neutral=(64,64), lawful_evil=(65,90), neutral_evil=(91,98), chaotic_evil=(99,100))
		if arg not in self.table:
			raise KeyError('value not valid')
		temp=modtable[arg]
		roll = [x+temp[0] for x in d(20,temp[1],[])]
		data=[]
		result=list()
		for x in roll:
			if x < 13:
				data.append('conventional')
				if d(100) > 95:
					data.append('monstrous')
			elif x < 18:
				data.append('nonstandard')
			else:
				data.append('magical')				
		lst=[]
		for a in randtable:
			temp=randtable[a][1]-randtable[a][0]+1
			for b in range(temp):
				lst.append(a)
		for a in data:
			result.append((a,random.choice(lst)))
		return result
		
	def populationgen(self, arg):
		modtable = dict(thorp=(-3,1), hamlet=(-2,1), village=(-1,1), small_town=(0,1), large_town=(3,1), small_city=(6,2), large_city=(9,3), metropolis=(12,4))
		classtable = dict(adept=(1,6), aristocrat=(1,4), barbarian=(1,4), bard=(1,6), cleric=(1,6), commoner=(4,4), druid=(1,6), expert=(3,4), fighter=(1,8), 
			monk=(1,4), paladin=(1,3), ranger=(1,3), rogue=(1,8), sorcerer=(1,4), warrior=(2,4), wizard=(1,4))
		populationtable=dict(thorp=(20,80), hamlet=(81,400), village=(401,900), small_town=(901,2000), large_town=(2001,5000),
		small_city=(5001, 12000), large_city=(12001,25000), metropolis=(25001,30000))
		
		populationpercent = dict(commoner=90, warrior=5, expert=3, aristocrat=1, adept=1)
		
		population=random.randrange(populationtable[arg][0],populationtable[arg][1])
		
		if arg not in self.table:
			raise KeyError('value not valid')
		mod=modtable[arg]
		maxlvl=dict()
		
		#find max npc of each class, between
		for a in classtable:
			temp=[]
			for b in xrange(mod[1]):
				y=mod[0]
				if arg in ['thorp','hamlet']:
					if a in ['ranger','druid']:
						if d(100) > 96:
							y=mod[0]+10
									
				x=d(classtable[a][1],classtable[a][0])+y
				if x > 0:
					temp.append(x)
			if temp != []:
				maxlvl[a]=temp
		
		#each max lvl spawns an equivalent number of residents
		data = dict()
		for a in maxlvl:
			data[a]=[]
			for b in maxlvl[a]:
				data[a].append(b)
				c=2
				while b>3:
					b=b/2
					for x in xrange(c):
						data[a].append(b)
					c=c*2
		
		#common residents take up the rest of the town
		remainder=population-len(sum([data[a] for a in data],[]))
		for a in populationpercent:
			temp=int(remainder*populationpercent[a]/100.0)
			temp1=[1 for x in xrange(temp)]
			if temp1 != []:
				if a in data:
					data[a]+=temp1
				else:
					data[a]=temp1
		
								
		return dict(classnumbers=data, population=population)
		
	def genresidents(self,region,size,population,classnumbers):
		#to generate the actual character objects for each resident
		modtable=dict(thorp=(0,1), hamlet=(1,1), village=(2,1), small_town=(3,1), large_town=(4,1), small_city=(5,2), large_city=(6,3), metropolis=(7,4))
		last=[namegen(region,'last')['last'] for x in xrange(int(population/d(4,modtable[size][1]*3)+modtable[size][0]))]
		
		result=dict(all=dict(),family=dict(),classes=dict())
		for a in classnumbers:
			for b in classnumbers[a]:
				name=[namegen(region,random.choice(['male','female']))['first'],random.choice(last)]
				temp=[x.split('_')[:2] for x in result['all']]
				if name in temp:
					name.append(str(temp.count(name)+1))
				#divide the names by family, if the family doesnt already exist in the result then put it there
				if name[1] not in result['family']:
					result['family'][name[1]]=dict()
				#make the character...
				char=Character('_'.join(name),' '.join(name),**{a:b})
				result['all'][char.savename]=char
				char=result['all'][char.savename]
				result['family'][name[1]][char.savename]=char
				#same with family above, but with classes, or occupations				
				if char._1st not in result['classes']:
					result['classes'][char._1st]=dict()
				result['classes'][char._1st][char.savename]=char
				
		return result
		
def func(y):
	for a in y:
		print a
		for b in y[a]:
			print '\t'+str(b)
				
		