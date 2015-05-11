from dnd_db import db
print '\tloading class data'

class Arch(dict):
	'''class for the archtype concept'''
	def __init__(self,*args,**kwargs):	
		self.attr = args
		if kwargs != {}:
			for a in kwargs:
				self[a]=kwargs[a]
	
	def __getattr__(self,attr):
		return self[attr]

class psion(dict):
	def __init__(self,**args):
		'''constructor/copy-constructor'''
		for a in args:
			self[a]=type(args[a])(args[a])
	def __call__(self,dicipline):
		'''modifies the psion instance to have additional skills'''
		b={}
		for a in self:
			b[a]=self[a]
		result=type(self)(**b)
		result['skills']+=result['dicipline'][dicipline]['skills']
		del result['dicipline']
		return result

arch = Arch(
	"str","con","dex","int","wis","cha", 
	mage = Arch(
		"int","wis","cha","dex","con","str",
		innate =Arch("cha","int","dex","wis","con","str"),
		book = Arch("int","dex","wis","con","cha","str")
		),
	melee = Arch(
		"str","dex","con","wis","int","cha",
		damage = Arch("str","dex","con","wis","int","cha"),
		tank = Arch("con","str","wis","dex","int","cha")
		),
	rogue = Arch(
		"dex","int","cha","str","wis","str",
		skills = Arch("int","cha","dex","wis","str","con"),
		damage = Arch("dex","int","str","cha","wis","con")
		),
	priest = Arch(
		"wis","int","cha","con","str","dex",
		divine= Arch("wis","con","str","int","dex","cha")
		)
	)
	
skills = db(
	#skill:[attribute, must be trained, armor penalty]
	appraise=["int",0,0],
	balance=["dex",0,1], 
	bluff=["cha",0,0],
	climb=["str",0,1],
	concentration=["con",0,0],
	craft=["int",0,0],
	decipher_script=["int",1,0],
	diplomacy=["cha",0,0],
	disable_device=["int",1,0],
	disguise=["cha",0,0],
	escape_artist=["dex",0,1],
	forgery=["int",0,0],
	gather_information=["cha",0,0],
	handle_animal=["cha",1,0],
	heal=["wis",0,0],
	hide=["dex",0,1],
	intimidate=["cha",0,0],
	jump=["str",0,1],
	knowledge=["int",1,0],
	listen=["wis",0,0],
	move_silently=["dex",0,1],
	open_lock=["dex",1,0],
	perform=["cha",1,0],
	profession=["wis",1,0],
	ride=["dex",0,0],
	search=["int",0,0],
	sense_motive=["wis",0,0],
	sleight_of_hand=["dex",1,1],
	spellcraft=["int",1,0],
	spot=["wis",0,0],
	survival=["wis",0,0],
	swim=["str",0,2],
	tumble=["dex",1,1],
	use_magic_device=["cha",1,0],
	use_rope=["dex",0,0],
	speak_language=["int",1,0],
	autohypnosis=["wis",1,0],
	psicraft=["int",1,0],
	use_psionic_device=["cha",1,0]
	)
Class = db(
	standard = db(
		DMG = db(
			adept={"bab": .5,  "dice":6, "skill":2, "arch":arch.priest.divine.attr, 'attr':'cha', 'cast':'divine',
				"saves":{"fort":"poor",  "ref":"poor", "will":"good"},
				"skills":["concentration","craft","handle_animal","heal","knowledge","profession","spellcraft","survival"], 
				"spells":[[3,1],[3,1],[3,2],[3,2,0],[3,2,1],[3,2,1],[3,3,2],[3,3,2,0],[3,3,2,1],[3,3,2,1],[3,3,3,2],[3,3,3,2,0],[3,3,3,2,1],[3,3,3,2,1],[3,3,3,3,2],[3,3,3,3,2,0],[3,3,3,3,2,1],[3,3,3,3,2,1],[3,3,3,3,3,2],[3,3,3,3,3,2]],
				"spelllist":[
					['create water', 'cure minor wounds', 'detect magic', 'ghost sound', 'guidance', 'light', 'mending', 'purify food and drink', 'read magic', 'touch of fatigue'],
					['bless', 'burning hands', 'cause fear', 'command', 'comprehend languages', 'cure light wounds', 'detect chaos', 'detect evil', 'detect good', 'detect law', 'endure elements', 'obscuring mist', 'protection from chaos', 'protection from evil', 'protection from good', 'protection from law', 'sleep'],
					['aid', 'animal trance', 'bears endurance', 'bulls strength', 'cats grace', 'cure moderate wounds', 'darkness', 'delay poison', 'invisibility', 'mirror image', 'resist energy', 'scorching ray', 'see invisibility', 'web'], ['animate dead', 'bestow curse', 'contagion', 'continual flame', 'cure serious wounds', 'daylight', 'deeper darkness', 'lightning bolt', 'neutralize poison', 'remove curse', 'remove disease', 'tongues'],
					['cure critical wounds', 'minor creation', 'polymorph', 'restoration', 'stoneskin', 'wall of fire'],
					['baleful polymorph', 'break enchantment', 'commune', 'heal', 'major creation', 'raise dead', 'true seeing', 'wall of stone']
					]
				},
			aristocrat={"bab":.75,  "dice":8, "skill":4,  "arch":arch.rogue.skills.attr,
				"saves":{"fort":"poor", "ref":"poor", "will":"good"},
				"skills":["appraise","bluff","diplomacy","disguise","forgery","gather_information","handle_animal","intimidate","knowledge","listen","perform","ride","sense_motive","speak_language","spot","swim","survival"]
				},
			commoner={"bab":.5,  "dice":4, "skill":2,  "arch":arch.rogue.skills.attr,
				"saves":{"fort":"poor", "ref":"poor", "will":"poor"},
				"skills":["climb","craft","handle_animal","jump","listen","profession","ride","spot","swim","use_rope"]
				},
			expert={"bab":.75,  "dice":6, "skill":6,  "arch":arch.melee.damage.attr,
				"saves":{"fort":"poor", "ref":"poor", "will":"good"},
				"skills":[]
				},
			warrior={"bab":1, "dice":8, "skill":2,  "arch":arch.melee.tank.attr,
				"saves":{"fort":"good", "ref":"poor", "will":"poor"}, 
				"skills":["climb","handle_animal","intimidate","jump","ride","swim"]
				}
			),
		PHB=db(
			barbarian={"bab":1,  "dice":12, "skill":4, "arch":arch.melee.damage.attr,
				"saves":{"fort":"good", "ref":"poor", "will":"poor"},
				"skills":["climb","craft","handle_animal","intimidate","jump","listen","ride","survival","swim"]
				},
			bard={"bab":.5,   "dice":6, "skill":6, "arch":arch.mage.innate.attr, 'attr':'cha', 'cast':'arcane',
				"saves":{"fort":"poor", "ref":"good","will":"good"},
				"skills":["appraise","balance","bluff","climb","concentration","craft","decipher_script","diplomacy","disguise","escape_artist","gather_information","hide","jump","knowledge","listen","move_silently","perform","profession","sense_motive","sleight_of_hand","speak language","spellcraft","swim","tumble","use_magic_device"],
				"spells":[[2], [3, 0], [3, 1], [3, 2, 0], [3, 3, 1], [3, 3, 2], [3, 3, 2, 0], [3, 3, 3, 1], [3, 3, 3, 2], [3, 3, 3, 2, 0], [3, 3, 3, 3, 1], [3, 3, 3, 3, 2], [3, 3, 3, 3, 2, 0], [4, 3, 3, 3, 3, 1], [4, 4, 3, 3, 3, 2], [4, 4, 4, 4, 3, 3, 2, 0], [4, 4, 4, 4, 3, 3, 1], [4, 4, 4, 4, 4, 3, 2], [4, 4, 4, 4, 4, 4, 3], [4, 4, 4, 4, 4, 4, 4] ],
				"known":[[4],[5,2],[6,3],[6,3,2],[6,4,3],[6,4,3],[6,4,4,2],[6,4,4,3],[6,4,4,3],[6,4,4,4,2],[6,4,4,4,3],[6,4,4,4,3],[6,4,4,4,4,2],[6,4,4,4,4,3],[6,4,4,4,4,3],[6,5,4,4,4,4,2],[6,5,5,4,4,4,3],[6,5,5,5,4,4,3],[6,5,5,5,5,4,4],[6,5,5,5,5,5,4]],
				"spelllist":[
					['lullaby', 'summon instrument', 'light', 'read magic', 'mending', 'message', 'resistance', 'prestidigitation', 'flare', 'open/close', 'daze', 'mage hand', 'know direction', 'dancing lights', 'daze', 'ghost sound'],\
					['hypnotism', 'lesser confusion', 'erase', 'sleep', 'detect secret doors', "nystul's magic aura", 'comprehend languages', 'cure light wounds', 'remove fear', 'summon monster I', 'disguise self', 'animate rope', 'grease', 'charm person', 'silent image', 'obscure object', 'magic mouth', 'unseen servant', 'ventriloquism', 'alarm', 'expeditious retreat', 'undetectable alignment', "tasha's hideous laughter", 'feather fall', 'cause fear', 'identify'],\
					['tongues', 'hold person', 'animal messenger', 'sound burst', 'hypnotic pattern', 'delay poison', 'pyrotechnics', 'animal trance', 'cats grace', 'summon swarm', 'heroism', 'locate object', 'summon monster II', 'invisibility', 'blur', 'eagles splendor', 'enthrall', 'mirror image', 'detect thoughts', 'shatter', 'minor image', 'calm emotions', 'misdirection', 'foxs cunning', 'glitterdust', 'cure moderate wounds', 'darkness', 'rage', 'alter self', 'daze monster', 'whispering wind', 'suggestion', 'blindness deafness', 'scare', 'silence'],\
					['charm monster', 'secret page', 'remove curse', 'illusory script', 'displacement', 'blink', 'daylight', 'dispel magic', 'cure serious wounds', 'fear', 'slow', 'good hope', 'glibness', 'leomunds tiny hut', 'confusion', 'major image', 'scrying', 'caseous form', 'sculpt sound', 'clairaudience clairvoyance', 'lesser geas', 'speak with animals', 'crushing despair', 'deep slumber', 'summon monster III', 'haste', 'sepia snake sigil', 'invisibility sphere', 'phantom steed', 'see invisibility'],\
					['zone of silence', 'rainbow pattern', 'shout speak with plants', 'hold monster', 'legend lore', 'repel vermin', 'shadow conjuration', 'summon monster IV', 'dimension door', 'locate creature', 'leomunds secure shelter', 'neutralize poison', 'break enchantment', 'detect scrying', 'modify memory', 'greater invisibility', 'freedom of movement', 'dominate person', 'cure critical wounds', 'hallucinatory terrain'],\
					['false vision', 'summon monster V', 'song of discord', 'seeming', 'greater dispel magic', 'mirage arcana', 'greater heroism', 'nightmare', 'mind fog', 'shadow walk', 'mislead', 'persistent image', 'mass suggestion', 'dream', 'mass cure light wounds', 'shadow evocation'],\
					['animate objects', 'programmed image', 'mass eagles splendor', 'greater shout', 'mass charm monster', 'mass cure moderate wounds', 'summon monster VI', 'geas quest', 'ottos irresistible dance', 'find the path', 'sympathetic vibration', 'eyebite', 'analyze dweomer', 'project image', 'greater scrying', 'permanent image', 'heros feast', 'mass foxs cunning', 'mass cats grace', 'veil']
					]
				
				},
			cleric={"bab":.75, "dice":8, "skill":2, "arch":arch.priest.divine.attr, 'attr':'wis', 'cast':'divine',
				"saves":{"fort":"good", "ref":"poor", "will":"good"}, 
				"skills":["concentration","craft","diplomacy","heal","knowledge_arcana","knowledge_history","knowledge_religion","knowledge_the planes","profession","spellcraft"],
				"spells":[[3,1],[4,2],[4,2,1],[5,3,2],[5,3,2,1],[5,3,3,2],[6,4,3,2,1],[6,4,3,3,2],[6,4,4,3,2,1],[6,4,4,3,3,2],[6,5,4,4,3,2,1],[6,5,4,4,3,3,2],[6,5,5,4,4,3,2,1],[6,5,5,4,4,3,3,2],[6,5,5,5,4,4,3,2,1],[6,5,5,5,4,4,3,3,2],[6,5,5,5,5,4,4,3,2,1],[6,5,5,5,5,4,4,3,3,2],[6,5,5,5,5,5,4,4,3,3],[6,5,5,5,5,5,4,4,4,4]],
				"spelllist":[
					['cure minor wounds', 'light', 'read magic', 'mending', 'resistance', 'detect magic', 'virtue', 'inflict minor wounds', 'create water', 'purify food and drink', 'guidance', 'detect poison'],\
					['obscuring mist', 'sanctuary', 'comprehend languages', 'bless water', 'cure light wounds', 'bless', 'remove fear', 'hide from undead', 'magic stone', 'shield of faith', 'command', 'inflict light wounds', 'curse water', 'bane', 'entropic shield', 'detect alignment', 'detect undead', 'doom', 'summon monster I', 'endure elements', 'deathwatch', 'divine favor', 'magic weapon', 'protection from alignment', 'cause fear'],\
					['eagles splendor', 'owls wisdom', 'augury', 'lesser restoration', 'death knell', 'hold person', 'consecrate', 'sound burst', 'delay poison', 'darkness', 'make whole', 'gentle repose', 'bulls strength', 'summon monster II', 'desecrate', 'find traps', 'status', 'enthrall', 'shatter', 'calm emotions', 'cure moderate wounds', 'shield other', 'spiritual weapon', 'undetectable alignment', 'bears endurance', 'zone of truth', 'align weapon', 'remove paralysis', 'aid', 'resist energy', 'inflict moderate wounds', 'silence'],\
					['wind wall', 'remove curse', 'protection from energy', 'stone shape', 'dispel magic', 'cure serious wounds', 'inflict serious wonds', 'daylight', 'prayer', 'meld into stone', 'bestow curse', 'continual flame', 'animate dead', 'water breathing', 'create food and water', 'locate object', 'deeper darkness', 'speak with dead', 'invisibility purge', 'magic vestment', 'remove disease', 'magic circle against alignment', 'glyph of warding', 'searing light', 'obscure object', 'water walk', 'contagion', 'helping hand', 'summon monster III', 'remove blindness deafness', 'blindness_deafness'],\
					['tongues', 'death ward', 'giant vermin', 'lesser planar ally', 'divination', 'inflict critical wounds', 'divine power', 'repel vermin', 'dismissal', 'summon monster IV', 'poison', 'imbude with spell ability', 'discern lies', 'restoration', 'freedom of movement', 'dimensional anchor', 'air walk', 'control water', 'sending', 'greater magic weapon', 'cure critical wounds', 'neutralize poison', 'spell immunity'],\
					['disrupting weapon', 'commune', 'mark of justice', 'dispel alignment', 'righteous might', 'hallow', 'symbol of pain', 'true seeing', 'plane shift', 'raise dead', 'break enchantment', 'symbol of sleep', 'atonement', 'mass inflict light wounds', 'insect plague', 'spell resistance', 'wall of stone', 'scrying', 'summon monster V', 'mass cure light wounds', 'unhallow', 'flame strike', 'greater command', 'slay living'],\
					['harm', 'wind walk', 'word of recall', 'blade barrier', 'undeath to death', 'mass inflict moderate wounds', 'symbol of persuasion', 'animate objects', 'mass bears endurance', 'planar ally', 'mass bulls strength', 'forbiddance', 'heal', 'geas quest', 'symbol of fear', 'find the path', 'create undead', 'greater glyph of warding', 'mass eagles splendor', 'greater dispel magic', 'antilife shell', 'mass cure moderate wounds', 'summon monster VI', 'mass owls wisdom', 'heros feast', 'banishment'],\
					['greater restoration', 'mass inflict serious wounds', 'ethereal jaunt', 'dictum', 'regenerate', 'refuge', 'symbol of stunning', 'control weather', 'word of chaos', 'blasphemy', 'mass cure serious wounds', 'repulsion', 'summon monster VII', 'greater scrying', 'resurrection', 'symbol of weakness', 'holy word', 'destruction'],\
					['unholy aura', 'shield of law', 'discern location', 'antimagic field', 'greater planar ally', 'create greater undead', 'cloak of chaos', 'fire storm', 'mass cure critical wounds', 'symbol of insanity', 'summon monster VIII', 'holy aura', 'mass inflict critical wounds', 'greater spell immunity', 'dimensional lock', 'symbol of death', 'earthquake'],\
					['true resurrection', 'implosion', 'miracle', 'mass heal', 'summon monster IX', 'storm of vengeance', 'energy drain', 'astral projection', 'etherealness', 'soul bind', 'gate']
					]
				},
			druid={"bab":.75,  "dice":8,  "skill":4, "arch":arch.priest.divine.attr, 'attr':'wis', 'cast':'divine',
				"saves":{"fort":"good", "ref":"poor", "will":"good"},
				"skills":["concentration","craft","diplomacy","handle_animal","heal","knowledge_nature","listen","profession","ride","spellcraft","spot","survival","swim"],
				"spells":[[3,1],[4,2],[4,2,1],[5,3,2],[5,3,2,1],[5,3,3,2],[6,4,3,2,1],[6,4,3,3,2],[6,4,4,3,2,1],[6,4,4,3,3,2],[6,5,4,4,3,2,1],[6,5,4,4,3,3,2],[6,5,5,4,4,3,2,1],[6,5,5,4,4,3,3,2],[6,5,5,5,4,4,3,2,1],[6,5,5,5,4,4,3,3,2],[6,5,5,5,5,4,4,3,2,1],[6,5,5,5,5,4,4,3,3,2],[6,5,5,5,5,5,4,4,3,3],[6,5,5,5,5,5,4,4,4,4]],
				"spelllist":[
					['cure minor wounds', 'light', 'read magic', 'mending', 'resistance', 'detect magic', 'virtue', 'flare', 'create water', 'know direction', 'purify food and drink', 'guidance', 'detect poison'],\
					['entangle', 'cure light wounds', 'obscuring mist', 'speak with animals', 'endure elements', 'produce flame', 'longstrider', 'magic fang', 'shillelagh', 'pass without trace', 'magic stone', 'hide from animals', 'charm animals', 'calm animals', 'faerie fire', 'detect animals or plants', 'jump', 'detect snares and pits', 'summon natures ally I', 'goodberry'],
					['owls wisdom', 'wood shape', 'chill metal', 'flaming sphere', 'warp wood', 'animal messenger', 'delay poison', 'cats grace', 'fog cloud', 'summon swarm', 'reduce animal', 'animal trance', 'summon natures ally II', 'fire trap', 'gust of wind', 'bulls strength', 'spider climb', 'lesser restoration', 'hold animal', 'bears endurance', 'resist energy', 'barkskin', 'flame blade', 'tree shape', 'heat metal', 'soften earth and stone'],
					['wind wall', 'quench', 'greater magic fang', 'protection from energy', 'stone shape', 'meld into stone', 'cure moderate wounds', 'water breathing', 'poison', 'speak with plants', 'diminish plants', 'remove disease', 'plant growth', 'dominate animal', 'call lightning', 'summon natures ally III', 'sleet storm', 'snare', 'contagion', 'daylight', 'neutralize poison', 'spike growth'],
					['spike stones', 'repel vermin', 'summon natures ally IV', 'scrying', 'antiplant shell', 'rusting grasp', 'ice storm', 'dispel magic', 'cure serious wounds', 'reincarnate', 'flame strike', 'blight', 'freedom of movement', 'command plants', 'giant vermin', 'air walk', 'control water'],
					['stoneskin', 'awaken', 'transmute rock to mud', 'summon natures ally V', 'unhallow', 'baleful polymorph', 'wall of throns', 'death ward', 'cure critical wounds', 'call lightning storm', 'commune with nature', 'tree stride', 'transmute mud to rock', 'atonement', 'control winds', 'wall of fire', 'hallow insect plague', 'animal growth'],
					['mass bulls strength', 'mass bears endurance', 'greater dispel magic', 'antilife shell', 'repel wood', 'summon natures ally VI', 'wall of stone', 'move earth', 'ironwood', 'find the path', 'stone tell', 'mass owls wisdom', 'mass cure light wounds', 'transport via plants', 'fire seeds', 'spellstaff', 'mass cats grace', 'liveoak'],
					['animate plants', 'wind walk', 'changestaff', 'heal', 'control weather', 'creeping doom', 'true seeing', 'firestorm', 'greater scrying', 'summon natures ally VII', 'sunbeam', 'mass cure moderate wounds', 'transmute metal to wood'],
					['word of recall', 'summon natures ally VIII', 'reverse gravity', 'earthquake', 'animal shapes', 'mass cure serious wounds', 'repel metal or stone', 'control plants', 'sunburst', 'finger of death', 'whirlwind'],
					['elemental swarm', 'mass cure critical wounds', 'shapechange', 'regenerate', 'summon natures ally IX', 'foresight', 'sympathy', 'shambler', 'antipathy', 'storm of vengeance']
					]
				},
			fighter={"bab":1,  "dice":10, "skill":2, "arch":arch.melee.tank.attr,
				"saves":{"fort":"good", "ref":"poor", "will":"poor"},
				"skills":["climb","craft","handle_animal","intimidate","jump","ride","swim"]
				},
			monk={"bab":.75,  "dice":8, "skill":4, "arch":arch.melee.damage.attr,
				"saves":{"fort":"good", "ref":"good", "will":"good"},
				"skills":["balance","climb","concentration","craft","diplomacy","escape_artist","hide","jump","knowledge_arcana","knowledge_religion","listen","move_silently","perform","profession","sense_motive","spot","swim","tumble"]
				},
			paladin={"bab":1,  "dice":10, "skill":2, "arch":arch.melee.tank.attr, 'attr':'wis', 'cast':'divine',
				"saves":{"fort":"good", "ref":"poor", "will":"poor"},
				"skills":["concentration","craft","diplomacy","handle_animal","heal","knowledge_nobility","knowledge_religion","profession","ride","sense_motive"],
				"spells":[[],[],[],[0],[0],[1],[1],[1,0],[1,0],[1,1],[1,1,0],[1,1,1],[2,1,1,0],[2,1,1,1],[2,2,1,1],[2,2,2,1],[3,2,2,1],[3,3,3,2],[3,3,3,3]],
				"spelllist":[
					['cure light wounds', 'bless weapon', 'endure elements', 'read magic', 'resistance', 'lesser restoration', 'divine favor', 'magic weapon', 'virtue', 'protection from alignment', 'create water', 'bless', 'detect undead', 'bless water', 'detect poison'],
					['undetectable alignment', 'eagles splendor', 'owls wisdom', 'delay poison', 'zone of truth', 'bulls strength', 'remove paralysis', 'shield other', 'resist energy'],
					['heal mount', 'cure moderate wounds', 'greater magic weapon', 'discern lies', 'remove curse', 'magic circle against alignment', 'daylight', 'dispel magic', 'prayer', 'remove blindness deafness'],
					['holy sword', 'dispel evil', 'mark of justice', 'death ward', 'neutralize poison', 'break enchantment', 'restoration', 'cure serious wounds', 'dispel chaos']
					]
				},
			ranger={"bab":1, "dice":8, "skill":6, "arch":arch.rogue.damage.attr, 'attr':'wis', 'cast':'divine',
				"saves":{"fort":"good", "ref":"good", "will":"poor"},
				"skills":["climb","concentration","craft","handle_animal","heal","hide","jump","knowledge_dungeoneering","knowledge_geography","knowledge_nature","listen","move_silently","profession","ride","serch","spot","survival","swim","use_rope"],
				"spells":[[],[],[],[0],[0],[1],[1],[1,0],[1,0],[1,1],[1,1,0],[1,1,1],[2,1,1,0],[2,1,1,1],[2,2,1,1],[2,2,2,1],[3,2,2,1],[3,3,3,2],[3,3,3,3]],
				"spelllist":[
					['entangle', 'hide from animals', 'delay poison', 'speak with animals', 'endure elements', 'charm animal', 'read magic', 'magic fang', 'detect animals or plants', 'jump', 'calm animals', 'animal messenger', 'pass without trace', 'detect snares and pits', 'summon natures ally I', 'resist energy', 'alarm', 'longstrider', 'detect poison'],
					['cure light wounds', 'owls wisdom', 'wind wall', 'cats grace', 'protection from energy', 'hold animal', 'spike growth', 'speak with plants', 'summon natures ally II', 'bears endurance', 'snare', 'barkskin'],
					['water walk', 'cure moderate wounds', 'repel vermin', 'remove disease', 'plant growth', 'darkvision', 'reduce animal', 'neutralize poison', 'summon natures ally III', 'diminish plants', 'greater magic fang', 'tree shape', 'command plants'],
					['summon natures ally IV', 'nondetection', 'animal growth', 'commune with nature', 'tree stride', 'cure serious wounds', 'freedom of movement']
					]
				},
			rogue={"bab":.75,  "dice":6, "skill":8, "arch":arch.rogue.skills.attr,
				"saves":{"fort":"poor", "ref":"good", "will":"poor"},
				"skills":["appraise","balance","bluff","climb","craft","decipher_script","diplomacy","disable_device","disguise","escape_artist","forgery","gather_information","hide","intimidate","jump","knowledge_local","listen","move_silently","open_lock","perform","profession","search","sense_motive","sleight_of_hand","spot","swim","tumble","use_magic_device","use_rope"]
				},
			sorcerer={"bab":.5,  "dice":4,  "skill":2, "arch":arch.mage.innate.attr, 'attr':'cha', 'cast':'arcane',
				"saves":{"fort":"poor", "ref":"poor", "will":"good"}, 
				"skills":["bluff","concentration","craft","knowledge_arcana","profession","spellcraft"],
				"spells":[[5,3],[6,4],[6,5],[6,6,3],[6,6,4],[6,6,5,3],[6,6,6,4],[6,6,6,5,3],[6,6,6,6,4],[6,6,6,6,5,3],[6,6,6,6,6,4],[6,6,6,6,6,5,3],[6,6,6,6,6,6,4],[6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,6,6,6]],
				"known":[[4,2],[5,2],[5,3],[6,3,1],[6,4,2],[7,4,2,1],[7,5,3,2],[8,5,3,2,1],[8,5,4,3,2],[9,5,4,3,2,1],[9,5,5,4,3,2],[9,5,5,4,3,2,1],[9,5,5,4,4,3,2],[9,5,5,4,4,3,2,1],[9,5,5,4,4,4,3,2],[9,5,5,4,4,4,3,2,1],[9,5,5,4,4,4,3,3,2],[9,5,5,4,4,4,3,3,2,1],[9,5,5,4,4,4,3,3,3,2],[9,5,5,4,4,4,3,3,3,3]],
				"spelllist":[
					['detect magic', 'open close', 'touch of fatigue', 'light', 'read magic', 'mending', 'resistance', 'prestidigitation', 'arcane mark', 'flare', 'detect poison', 'daze', 'mage hand', 'dancing lights', 'disrupt undead', 'acid splash', 'message', 'ghost sound', 'ray of frost'],
					['shocking grasp', 'obscuring mist', 'color spray', 'shield', 'hypnotism', 'ray of enfeeblement', 'jump', 'erase', 'sleep', 'detect secret doors', 'nystuls magic aura', 'comprehend languages', 'charm person', 'animate rope', 'enlarge person', 'tensers floating disk', 'chill touch', 'disguise self', 'burning hands', 'grease', 'reduce person', 'magic missile', 'protection from alignment', 'silent image', 'detect undead', 'mage armor', 'summon monster I', 'unseen servant', 'ventriloquism', 'endure elements', 'hold portal', 'mount', 'expeditious retreat', 'magic weapon', 'feather fall', 'cause fear', 'identify', 'truestrike', 'alarm'],
					['false life', 'owls wisdom', 'scorching ray', 'spectral hand', 'continual flame', 'rope trick', 'ghoul touch', 'arcane lock', 'levitate', 'hypnotic pattern', 'web', 'pyrotechnics', 'leomunds trap', 'cats grace', 'fog cloud', 'summon swarm', 'darkvision', 'locate object', 'summon monster II', 'invisibility', 'blur', 'gust of wind', 'melfs acid arrow', 'eagles splendor', 'mirror image', 'spider climb', 'command undead', 'detect thoughts', 'touch of idiocy', 'shatter', 'minor image', 'misdirection', 'foxs cunning', 'see invisibility', 'glitterdust', 'obscure object', 'magic mouth', 'darkness', 'knock', 'bears endurance', 'flaming sphere', 'alter self', 'resist energy', 'daze monster', 'whispering wind', 'tashas hideous laughter', 'blindness deafness', 'scare', 'protection from arrows'],
					['halt undead', 'tongues', 'wind wall', 'secret page', 'ray of exhaustion', 'illusory script', 'displacement', 'blink', 'sleet storm', 'daylight', 'dispel magic', 'explosive runes', 'flame arrow', 'slow', 'water breathing', 'gentle repose', 'summon monster III', 'shrink item', 'heroism', 'nondetection', 'lightning bolt', 'leomunds tiny hut', 'arcane sight', 'major image', 'magic circle against alignment', 'protection from energy', 'gaseous form', 'vampiric touch', 'clairaudience clairvoyance', 'fly', 'greater magic weapon', 'deep slumber', 'hold person', 'range', 'haste', 'keen edge', 'suggestion', 'sepia snake sigil', 'invisibility sphere', 'stinking cloud', 'phantom steed', 'fireball'],
					['phantasmal killer', 'charm monster', 'mass reduce person', 'minor creation', 'rainbow pattern', 'leomunds secure shelter', 'evards black tentacles', 'stone shape', 'bestow curse', 'fear', 'fire shieldd', 'animate dead', 'polymorph', 'dimensional anchor', 'arcane eye', 'otilukes resilient sphere', 'shadow conjuration', 'summon monster IV', 'shout', 'detect scrying', 'enervation', 'solid fog', 'illusory wall', 'stoneskin', 'confusion', 'scrying', 'ice storm', 'remove curse', 'wall of fire', 'lesser globe of invulnerability', 'lesser geas', 'fire trap', 'crushing despair', 'contagion', 'mass enlarge person', 'locate creature', 'greater invisibility', 'dimension door', 'hallucinatory terrain', 'wall of ice'],
					['overland flight', 'feeblemind', 'mind fog', 'cloudkill', 'rarys telepathic bond', 'wall of stone', 'prying eyes', 'symbol of pain', 'shadow evocation', 'teleport', 'transmute rock to mud', 'hold monster', 'animal growth', 'waves of fatigue', 'nightmare', 'contact other plane', 'leomunds secret chest', 'break enchantment', 'symbol of sleep', 'permanency', 'blight', 'lesser planar binding', 'mordenkainens faithful hound', 'bigbys interposing hand', 'seeming', 'false vision', 'summon monster V', 'passwall', 'mordenkainens private sanctum', 'magic jar', 'baleful polymorph', 'telekinesis', 'dominate person', 'sending', 'cone of cold', 'mirage arcana', 'fabricate', 'major creation', 'wall of force', 'persistent image', 'transmute mud to rock', 'dream', 'dismissal'],
					['stone to flesh', 'acid fog', 'mass bears endurance', 'undeath to death', 'greater heroism', 'guards  and wards', 'planar binding', 'chain lightning', 'legend lore', 'mass bulls strength', 'true seeing', 'flesh to stone', 'disintegrate', 'circle of death', 'shadow walk', 'eyebite', 'analyze dweomer', 'globe of invulnerability', 'antimagic field', 'mass suggestion', 'mass foxs cunning', 'mass cats grace', 'tensers transformation', 'programmed image', 'move earth', 'symbol of persuasion', 'symbol of fear', 'create undead', 'repulsion', 'otilukes freezing sphere', 'veil', 'control water', 'greater dispel magic', 'mass eagles splendor', 'summon monster VI', 'geas quest', 'mislead', 'wall of iron', 'bigbys forceful hand', 'mass owls wisdom', 'permanent image', 'contingency'],
					['forcecage', 'phase door', 'teleport object', 'prismatic spray', 'limited wish', 'control weather', 'drawmijis instant summons', 'sequester', 'mordenkainens magnificent mansion', 'greater scrying', 'project image', 'control undead', 'symbol of weakness', 'finger of death', 'waves of exhaustion', 'mordenkainens sword', 'plane shift', 'delayed blast fireball', 'summon monster ', 'greater shadow conjuration', 'spell turning', 'power word blind', 'greater teleport', 'reverse gravity', 'insanity', 'statue', 'bigbys grasping hand', 'ethereal jaunt', 'greater arcane sight', 'simularcrum', 'mass invisibility', 'symbol of stunning', 'mass hold person', 'vision', 'banishment'],
					['power word stun', 'greater shadow evocation', 'dimensional lock', 'mass charm monster', 'binding', 'discern location', 'greater shout', 'scintillating pattern', 'temporal stasis', 'protection from spells', 'moment of prescience', 'create greater undead', 'horrid wilting', 'antipathy', 'maze', 'sunburst', 'screen', 'iron body', 'clone', 'symbol of insanity', 'ottos irrestible dance', 'prismatic wall', 'demand', 'incendiary cloud', 'greater prying eyes', 'mind blank', 'polymorph any object', 'sympathy', 'trap the soul', 'otilukes telekinetic sphere', 'summon monster VIII', 'polar ray', 'bigbys clenched fist', 'symbol of death', 'greater planar binding'],
					['astral projection', 'power word kill', 'time stop', 'imprisonment', 'prismatic sphere', 'energy drain', 'mordenkainens disjunction', 'soul bind', 'dominate monster', 'meteor swarm', 'summon monster IX', 'mass hold monster', 'gate', 'bigbys crushing hand', 'shapechange', 'freedom', 'teleportation circle', 'wail of the banshee', 'refuge', 'wish', 'shades', 'foresight', 'etherealness', 'weird']
					]
				},
			wizard={"bab":.5,  "dice":4, "skill":2, "arch":arch.mage.book.attr, 'attr':'int', 'cast':'arcane',
				"saves":{"fort":"poor", "ref":"poor", "will":"good"},
				"skills":["concentration","craft","decipher_script","knowledge_all","profession","spellcraft"],
				"spells":[[3,1],[4,3],[4,2,1],[4,3,2],[4,3,2,1],[4,3,3,2],[4,4,3,2,1],[4,4,3,3,2],[4,4,4,3,2,1],[4,4,4,3,3,2],[4,4,4,4,3,2,1],[4,4,4,4,3,3,2],[4,4,4,4,4,3,2,1],[4,4,4,4,4,3,3,2],[4,4,4,4,4,4,3,2,1],[4,4,4,4,4,4,3,3,2],[4,4,4,4,4,4,4,3,2,1],[4,4,4,4,4,4,4,3,3,2],[4,4,4,4,4,4,4,4,3,3],[4,4,4,4,4,4,4,4,4,4]],
				"spelllist":[
					['detect magic', 'open close', 'touch of fatigue', 'light', 'read magic', 'mending', 'resistance', 'prestidigitation', 'arcane mark', 'flare', 'detect poison', 'daze', 'mage hand', 'dancing lights', 'disrupt undead', 'acid splash', 'message', 'ghost sound', 'ray of frost'],
					['shocking grasp', 'obscuring mist', 'color spray', 'shield', 'hypnotism', 'ray of enfeeblement', 'jump', 'erase', 'sleep', 'detect secret doors', 'nystuls magic aura', 'comprehend languages', 'charm person', 'animate rope', 'enlarge person', 'tensers floating disk', 'chill touch', 'disguise self', 'burning hands', 'grease', 'reduce person', 'magic missile', 'protection from alignment', 'silent image', 'detect undead', 'mage armor', 'summon monster I', 'unseen servant', 'ventriloquism', 'endure elements', 'hold portal', 'mount', 'expeditious retreat', 'magic weapon', 'feather fall', 'cause fear', 'identify', 'truestrike', 'alarm'],
					['false life', 'owls wisdom', 'scorching ray', 'spectral hand', 'continual flame', 'rope trick', 'ghoul touch', 'arcane lock', 'levitate', 'hypnotic pattern', 'web', 'pyrotechnics', 'leomunds trap', 'cats grace', 'fog cloud', 'summon swarm', 'darkvision', 'locate object', 'summon monster II', 'invisibility', 'blur', 'gust of wind', 'melfs acid arrow', 'eagles splendor', 'mirror image', 'spider climb', 'command undead', 'detect thoughts', 'touch of idiocy', 'shatter', 'minor image', 'misdirection', 'foxs cunning', 'see invisibility', 'glitterdust', 'obscure object', 'magic mouth', 'darkness', 'knock', 'bears endurance', 'flaming sphere', 'alter self', 'resist energy', 'daze monster', 'whispering wind', 'tashas hideous laughter', 'blindness deafness', 'scare', 'protection from arrows'],
					['halt undead', 'tongues', 'wind wall', 'secret page', 'ray of exhaustion', 'illusory script', 'displacement', 'blink', 'sleet storm', 'daylight', 'dispel magic', 'explosive runes', 'flame arrow', 'slow', 'water breathing', 'gentle repose', 'summon monster III', 'shrink item', 'heroism', 'nondetection', 'lightning bolt', 'leomunds tiny hut', 'arcane sight', 'major image', 'magic circle against alignment', 'protection from energy', 'gaseous form', 'vampiric touch', 'clairaudience clairvoyance', 'fly', 'greater magic weapon', 'deep slumber', 'hold person', 'range', 'haste', 'keen edge', 'suggestion', 'sepia snake sigil', 'invisibility sphere', 'stinking cloud', 'phantom steed', 'fireball'],
					['phantasmal killer', 'charm monster', 'mass reduce person', 'minor creation', 'rainbow pattern', 'leomunds secure shelter', 'evards black tentacles', 'stone shape', 'bestow curse', 'fear', 'fire shieldd', 'animate dead', 'polymorph', 'dimensional anchor', 'arcane eye', 'otilukes resilient sphere', 'shadow conjuration', 'summon monster IV', 'shout', 'detect scrying', 'enervation', 'solid fog', 'rarys mnemonic enhancer', 'illusory wall', 'stoneskin', 'confusion', 'scrying', 'ice storm', 'remove curse', 'wall of fire', 'lesser globe of invulnerability', 'lesser geas', 'fire trap', 'crushing despair', 'contagion', 'mass enlarge person', 'locate creature', 'greater invisibility', 'dimension door', 'hallucinatory terrain', 'wall of ice'],
					['overland flight', 'feeblemind', 'mind fog', 'cloudkill', 'rarys telepathic bond', 'wall of stone', 'prying eyes', 'symbol of pain', 'shadow evocation', 'teleport', 'transmute rock to mud', 'hold monster', 'animal growth', 'waves of fatigue', 'nightmare', 'contact other plane', 'leomunds secret chest', 'break enchantment', 'symbol of sleep', 'permanency', 'blight', 'lesser planar binding', 'mordenkainens faithful hound', 'bigbys interposing hand', 'seeming', 'false vision', 'summon monster V', 'passwall', 'mordenkainens private sanctum', 'magic jar', 'baleful polymorph', 'telekinesis', 'dominate person', 'sending', 'cone of cold', 'mirage arcana', 'fabricate', 'major creation', 'wall of force', 'persistent image', 'transmute mud to rock', 'dream', 'dismissal'],
					['stone to flesh', 'acid fog', 'mass bears endurance', 'undeath to death', 'greater heroism', 'guards  and wards', 'planar binding', 'chain lightning', 'legend lore', 'mass bulls strength', 'true seeing', 'flesh to stone', 'disintegrate', 'circle of death', 'shadow walk', 'eyebite', 'analyze dweomer', 'globe of invulnerability', 'antimagic field', 'mass suggestion', 'mass foxs cunning', 'mass cats grace', 'tensers transformation', 'programmed image', 'move earth', 'symbol of persuasion', 'symbol of fear', 'create undead', 'repulsion', 'otilukes freezing sphere', 'veil', 'control water', 'greater dispel magic', 'mass eagles splendor', 'summon monster VI', 'geas quest', 'mordenkainens lucubration', 'mislead', 'wall of iron', 'bigbys forceful hand', 'mass owls wisdom', 'permanent image', 'contingency'],
					['forcecage', 'phase door', 'teleport object', 'prismatic spray', 'limited wish', 'control weather', 'drawmijis instant summons', 'sequester', 'mordenkainens magnificent mansion', 'greater scrying', 'project image', 'control undead', 'symbol of weakness', 'finger of death', 'waves of exhaustion', 'mordenkainens sword', 'plane shift', 'delayed blast fireball', 'summon monster ', 'greater shadow conjuration', 'spell turning', 'power word blind', 'greater teleport', 'reverse gravity', 'insanity', 'statue', 'bigbys grasping hand', 'ethereal jaunt', 'greater arcane sight', 'simularcrum', 'mass invisibility', 'symbol of stunning', 'mass hold person', 'vision', 'banishment'],
					['power word stun', 'greater shadow evocation', 'dimensional lock', 'mass charm monster', 'binding', 'discern location', 'greater shout', 'scintillating pattern', 'temporal stasis', 'protection from spells', 'moment of prescience', 'create greater undead', 'horrid wilting', 'antipathy', 'maze', 'sunburst', 'screen', 'iron body', 'clone', 'symbol of insanity', 'ottos irrestible dance', 'prismatic wall', 'demand', 'incendiary cloud', 'greater prying eyes', 'mind blank', 'polymorph any object', 'sympathy', 'trap the soul', 'otilukes telekinetic sphere', 'summon monster VIII', 'polar ray', 'bigbys clenched fist', 'symbol of death', 'greater planar binding'],
					['astral projection', 'power word kill', 'time stop', 'imprisonment', 'prismatic sphere', 'energy drain', 'mordenkainens disjunction', 'soul bind', 'dominate monster', 'meteor swarm', 'summon monster IX', 'mass hold monster', 'gate', 'bigbys crushing hand', 'shapechange', 'freedom', 'teleportation circle', 'wail of the banshee', 'refuge', 'wish', 'shades', 'foresight', 'etherealness', 'weird']
					]
				}
			)
		),
	psionic = db(
		#powers = (power points,powers known,max powerlevel)
		EPH=db(
			psion=psion(bab=.5, dice=4, skill=2, arch=arch.mage.book.attr, attr='int',
				saves={"fort":"poor", "ref":"poor", "will":"good"},
				skills=["concentration","craft","knowledge_all","profession","psicraft"],
				powers=[(2, 3, 1), (6, 5, 1), (11, 7, 2), (17, 9, 2), (25, 11, 3), (35, 13, 3), (46, 15, 4), (58, 17, 4), (72, 19, 5), (88, 21, 5), (106, 22, 6), (126, 24, 6), (147, 25, 7), (170, 27, 7), (195, 28, 8), (221, 30, 8), (250, 31, 9), (280, 33, 9), (311, 34, 9), (343, 36, 9)],
				dicipline=dict(
					seer={"skills":["gather_information","listen","spot"]},
					shaper={"skills":["bluff","disguise","use_psionic_device"]},
					kineticist={"skills":["autohypnosis","disable_device","intimidate"]},
					egoist={"skills":["autohypnosis","balance","heal"]},
					nomad={"skills":["climb","jump","ride","survival","swim"]},
					telepath={"skills":["bluff","diplomacy","gather_information","sense_motive"]}
					)
				),
			psychic_warrior={"bab":.75, "dice":8, "skill":2, "arch":arch.melee.tank.attr, 'attr':'wis',
				"saves":{"fort":"good","ref":"poor","will":"poor"},
				"skills":["autohypnosis","climb","concentration","craft","jump","knowledge_psionics","profession","ride","search","swim"],
				"powers":[(0, 1, 1), (1, 2, 1), (3, 3, 1), (5, 4, 2), (7, 5, 2), (11, 6, 2), (15, 7, 3), (19, 8, 3), (23, 9, 3), (27, 10, 4), (35, 11, 4), (43, 12, 4), (51, 13, 5), (59, 14, 5), (67, 15, 5), (79, 16, 6), (91, 17, 6), (103, 18, 6), (115, 19, 6), (127, 20, 6)]
				},
			soulknife={"bab":.75, "dice":10, "skill":4, "arch":arch.melee.damage.attr,
				"saves":{"fort":"poor", "ref":"good", "will":"good"},
				"skills":["autohypnosis","climb","concentration","craft","hide","jump","knowledge_psionics","listen","move_silently","profession","spot","tumble"]
				},
			wilder={"bab":.75, "dice":8, "skill":4, "arch":arch.mage.innate.attr, 'attr':'cha',
				"saves":{"fort":"poor", "ref":"poor", "will":"good"},
				"skills":["autohypnosis","balance","bluff","climb","concentration","craft","escape_artist","intimidate","jump","knowledge_psionics","listen","profession","psicraft","sense_motive","spot","swim","tumble"],
				"powers":[(2, 1, 1), (6, 2, 1), (11, 2, 1), (17, 3, 2), (25, 3, 2), (35, 4, 3), (46, 4, 3), (58, 5, 4), (72, 5, 4), (88, 6, 5), (106, 6, 5), (126, 7, 6), (147, 7, 6), (170, 8, 7), (195, 8, 7), (221, 9, 8), (250, 9, 8), (280, 10, 9), (311, 10, 9), (343, 11, 9)]
				}
			),
		CP=db(
			ardent={"bab":.75, "dice":6, "skill":2, "arch":arch.mage.innate.attr, 'attr':'wis',
				"saves":{"fort":"poor","ref":"poor","will":"good"},
				"skills":["autohypnosis","concentration","craft","diplomacy","heal","knowledge_all","profession","psicraft"],
				"powers":[(2, 2), (6, 3), (11, 4), (17, 5), (25, 6), (35, 7), (46, 8), (58, 9), (72, 10), (88, 11), (106, 12), (126, 13), (147, 14), (170, 15), (195, 16), (221, 17), (250, 18), (280, 19), (311, 20), (343, 21)]
				},
			divine_mind={"bab":.75, "dice":10, "skill":2, "arch":arch.melee.damage.attr, 'attr':'wis',
				"saves":{"fort":"good","ref":"poor","will":"good"},
				"skills":["autohypnosis","climb","concentration","craft","jump","knowledge_psionics","knowledge_religion","profession","psicraft","ride","swim"],
				"powers":[(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 1, 1), (6, 2, 1), (8, 2, 1), (10, 3, 2), (12, 3, 2), (14, 4, 2), (18, 4, 3), (22, 5, 3), (26, 5, 3), (30, 6, 4), (35, 6, 4), (40, 7, 4), (45, 7, 5), (50, 8, 5), (55, 8, 5), (62, 9, 6)]
				},
			lurk={"bab":.75, "dice":6, "skill":4, "arch":arch.rogue.damage.attr, 'attr':'int',
				"saves":{"fort":"poor","ref":"good","will":"good"},
				"skills":["autohypnosis","bluff","climb","concentration","craft","disguise","escape_artist","hide","jump","knowledge_psionics","listen","move_silently","profession","psicraft","sleight_of_hand","spot","swim","tumble","use_psionic_device"],
				"powers":[(1, 1, 1), (2, 2, 1), (3, 3, 1), (5, 4, 2), (7, 5, 2), (11, 6, 2), (15, 7, 3), (19, 8, 3), (23, 9, 3), (27, 10, 4), (35, 11, 4), (43, 12, 4), (51, 13, 5), (59, 14, 5), (67, 15, 5), (79, 16, 6), (91, 17, 6), (103, 18, 6), (115, 19, 6), (127, 20, 6)]
				},
			)
		),
	complete = db(
		divine = db(
			favored_soul={"bab":.75, "dice":8, "skill":2,"arch":arch.priest.attr,
				"saves":{"fort":"good", "ref":"good", "will":"good"},
				"skills":['concentration','craft','diplomacy','heal','jump','knowledge_arcana','profession','sense motive','spellcraft'],
				"spells":[[5,3],[6,4],[6,5],[6,6,3],[6,6,4],[6,6,5,3],[6,6,6,4],[6,6,6,5,3],[6,6,6,6,4],[6,6,6,6,5,3],[6,6,6,6,6,4],[6,6,6,6,6,5,3],[6,6,6,6,6,6,4],[6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,6,5,3],[6,6,6,6,6,6,6,6,6,6,4],[6,6,6,6,6,6,6,6,6,6,6]],
				"known":[[4,3],[5,3],[6,4],[6,4,1],[6,5,3],[7,5,3,1],[7,6,4,3],[8,6,4,3,1],[8,6,5,4,3],[9,6,5,4,3,1],[9,6,6,5,4,3],[9,6,6,5,4,3,1],[9,6,6,5,5,4,3],[9,6,6,5,5,4,3,1],[9,6,6,5,5,5,4,3],[9,6,6,5,5,5,4,3,1],[9,6,6,5,5,5,4,4,3],[9,6,6,5,5,5,4,4,3,1],[9,6,6,5,5,5,4,4,4,3],[9,6,6,5,5,5,4,4,4,4]]
				},
			shugenja={"bab":.5, "dice":6, "skill":4, "arch":arch.mage.innate.attr,
				"saves":{"fort":"poor", "ref":"poor", "will":"good"},
				"skills":['concentration','craft','diplomacy','heal','knowledge_all','profession','spellcraft']
				}
			),
		scoundrel = db(
			)
		)
	)
	
