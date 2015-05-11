from dnd_character import load
def retired(who='all'):
	state='retired'
	if who == 'all':
		load('wolfah',state)
	else:
		load(who,state)
	
def standby(who='all'):
	state='standby'
	if who=='all':
		load('ellot',state)
	else:
		load(who,state)

#active
print '---'
load("sharef")
load("khellen")
load("koto")
load("toru")
