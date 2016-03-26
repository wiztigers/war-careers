# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tostring import ConsoleToString
from collections import OrderedDict

SOURCES = {
	'core': "Warhammer (2nde édition)",
	'comp': "Le Compagnon (2nde édition)",
	'magi': "Les Royaumes de sorcellerie (2nde édition)",
	'sigm': "Les Héritiers de Sigmar (2nde édition)",
	'glac': "La Reine des Glaces (2nde édition)",
}

class Source(object):
	def __init__(self, document, page):
		self.document = document
		self.page = page

class Skill(object):
	def __init__(self, id_, label, trait=None, description=None, source=None, specialized=False, speciality=None, advanced=False):
		self.id_  = id_
		self.label = label
		self.trait = trait
		self.description = description or "";
		self.source = source
		self.specialized = specialized or (speciality is not None)
		self.speciality = speciality or []
		if isinstance(self.trait, list):
			if len(self.trait) != len(self.speciality):
				print("ERROR: Skill \""+label+"["+id_+"]: speciality:trait mismatch.")
		self.advanced = advanced
		self.careers = [] #redundancy? Career.skills
		self.talents = [] #redundancy?



class Talent(object):
	def __init__(self, id_, label, description=None, source=None, modifiers=None, specialized=False, speciality=None):
		self.id_  = id_
		self.label = label
		self.description = "" or description;
		self.source = source
		self.specialized = specialized or (speciality is not None)
		self.speciality = speciality or []
		self.modifiers = modifiers or []
		self.careers = [] #redundancy? Career.talents

class Modifier(object):
	def __init__(self, value, trait, skill, condition=None):
		self.trait = trait
		self.skill = skill
		self.value = value
		self.condition = condition



class Trait(object):
	def __init__(self, id_, label, primary=True):
		self.id_  = id_;
		self.label = label;
		self.primary = primary


TRAITS = [
	# primary: +5%/+1
	Trait('CC', "Capacité de Combat"),
	Trait('CT', "Capacité de Tir"),
	Trait('F',  "Force"),
	Trait('E',  "Résistance"),
	Trait('Ag', "Agilité"),
	Trait('Int',"Intelligence"),
	Trait('FM', "Force Mentale"),
	Trait('Soc',"Sociabilité"),
	# secondary: +1/+1
	Trait('A',  "Attaques",  False),
	Trait('B',  "Blessures", False),
	Trait('BF', "Bonus de Force",    False),
	Trait('BE', "Bonus d'Endurance", False),
	Trait('M',  "Mouvement", False),
	Trait('Mag',"Magie",     False),
	Trait('PF', "Points de Focalisation", False),
	Trait('PD', "Points de Destin", False),
		]
PROFILE = OrderedDict()
for trait in TRAITS:
	PROFILE[trait.id_] = trait



class Career(object):
	def __init__(self, id_, label, description=None, source=None, advanced=False, profile=None, skills=None, talents=None, before=None, after=None):
		errors = []
		self.id_  = id_
		self.label = label
		self.description = description or ""
		self.source = source
		if self.source is not None:
			try:
				SOURCES[self.source.document]
			except KeyError:
				errors.append("Book \""+self.source.document+"\" is not referenced.")
		self.advanced = advanced
		self.profile = OrderedDict()
		for k,v in PROFILE.items():
			self.profile[k] = 0
		profile = profile or {}
		for k,v in profile.items():
			try:
				trait = PROFILE[k]
				if trait.primary:
					if v%5 is not 0:
						errors.append("\""+k+"\" must be divisible by 5.")
						trait = None
				if trait is not None:
					self.profile[k] = v
			except KeyError:
				errors.append("\""+k+"\" is not a valid profile item.")
		self.skills  = []
		skills = skills or []
		for key in skills:
			self.skills.append(key)
		self.talents  = []
		talents = talents or []
		for key in talents:
			self.talents.append(key)
		self.before = []
		before = before or []
		for key in before:
			self.before.append(key)
		self.after = []
		after = after or []
		for key in after:
			self.after.append(key)
		if len(errors) > 0:
			print("Career \""+label+"\":\n - "+"\n - ".join(errors))

