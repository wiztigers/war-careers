# -*- coding: utf-8 -*-

from __future__ import unicode_literals 
from collections import OrderedDict

class Skill(object):
	def __init__(self, id_, label, description=None, specialized=False, speciality=None):
		self.id_  = id_
		self.label = label
		self.description = description or "";
		self.specialized = specialized or (speciality is not None)
		self.speciality = None
		self.careers = [] #redundancy? Career.skills
		self.talents = [] #redundancy?

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.id_+"]"
		if self.specialized:
			res += '('
			if self.speciality is not None:
				res += self.speciality
			else:
				res += "au choix"
			res += ')'
		return unicode(res)

SKILL_LIST = [
	Skill('com', "Commérages"),
	Skill('cac', "Connaissances Académiques", specialized=True),
	Skill('cge', "Connaissances Générales", specialized=True),
		]
SKILLS = {}
for skill in SKILL_LIST:
	SKILLS[skill.id_] = skill



class Talent(object):
	def __init__(self, id_, label, description=None):
		self.id_  = id_
		self.label = label
		self.description = "";
		self.careers = [] #redundancy? Career.talents

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.id_+"]"
		return unicode(res)


class Modifier(object):
	def __init__(self):
		self.condition = None
		self.carac = None
		self.skill = None

TALENTS = {
		}



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
	Trait('Mag',"Magie",     False),
		]
PROFILE = {}
for trait in TRAITS:
	PROFILE[trait.id_] = trait

def profile2str(profile):
	res = ''
	for k in profile.keys():
		res += '|{:3}'.format(k)
	res += '|\n---------------------------------------------\n|'
	for v in profile.values():
		res += ' {:<2}|'.format(v)
	return res

CAREERS = { }

def complete(dst, src, general_index, errors, message):
		src = src or []
		errors = errors or []
		for key in src:
			try:
				general_index[key]
				dst.append(key)
			except KeyError:
				errors.append("\""+key+"\" is not a valid "+message+" identifier.")

class Career(object):
	def __init__(self, id_, label, description=None, advanced=False, profile=None, skills=None, talents=None, before=None, after=None):
		errors = []
		self.id_  = id_
		self.label = label
		self.description = description or ""
		self.advanced = advanced
		self.profile = OrderedDict()
		self.profile['CC']  = 0
		self.profile['CT']  = 0
		self.profile['F']   = 0
		self.profile['E']   = 0
		self.profile['Ag']  = 0
		self.profile['Int'] = 0
		self.profile['FM']  = 0
		self.profile['Soc'] = 0
		self.profile['A']   = 0
		self.profile['B']   = 0
		self.profile['Mag'] = 0
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
		complete(self.skills, skills, SKILLS, errors, "skill")
		self.talents  = []
		complete(self.talents, talents, TALENTS, errors, "talent")
		talents = talents or []
		self.before = []
		complete(self.before, before, CAREERS, errors, "career")
		self.after = []
		complete(self.after, after, CAREERS, errors, "career")
		if len(errors) > 0:
			print("Career \""+label+"\":\n - "+"\n - ".join(errors))

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.id_+"]"
		res += "(carrière "
		if self.advanced:
			res += "avancée)\n"
		else:
			res += "de base)\n"
		if (len(self.description) > 0):
			res += self.description+'\n'
		res += profile2str(self.profile)+'\n'
		res += "Compétences ("+str(len(self.skills))+"): "
		for id_ in self.skills:
			skill = SKILLS[id_]
			res += unicode(skill)+", "
		if len(self.skills) is 0:
			res += "Aucune"
		else:
			res = res[:-2]
		res += '\n'
		res += "Talents ("+str(len(self.talents))+"): "
		for id_ in self.talents:
			talents = TALENTS[id_]
			res += unicode(talent)
		if len(self.talents) is 0:
			res += "Aucun"
		res += '\n'
		return unicode(res)





if __name__ == '__main__':
	career = Career('avé', "Avoué", profile={'CC':0,'CT':15,'E':5,'B':2, 'TIR':66, 'Soc': 7}, skills=['com','cca','cge'])
	print("Carrière: "+unicode(career));

