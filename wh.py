# -*- coding: utf-8 -*-

from collections import OrderedDict

class Skill(object):
	def __init__(self, name, label, description=None, specialized=False, speciality=None):
		self.name  = name
		self.label = label
		self.description = description or "";
		self.specialized = specialized or (speciality is not None)
		self.speciality = None
		self.careers = [] #redundancy? Career.skills
		self.talents = [] #redundancy?

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.name+"]"
		if self.specialized:
			res += '('
			if self.speciality is not None:
				res += self.speciality
			else:
				res += u"au choix"
			res += ')'
		return unicode(res)

SKILLS = {
		'com': Skill('com', u"Commérages"),
		'cac': Skill('cac', u"Connaissances Académiques", specialized=True),
		'cge': Skill('cge', u"Connaissances Générales", specialized=True),
		}



class Talent(object):
	def __init__(self, name, label, description=None):
		self.name  = name
		self.label = label
		self.description = "";
		self.careers = [] #redundancy? Career.talents

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.name+"]"
		return res


class Modifier(object):
	def __init__(self):
		self.condition = None
		self.carac = None
		self.skill = None

TALENTS = {
		}



class Trait(object):
	def __init__(self, name, label, primary=True):
		self.name  = name;
		self.label = label;
		self.primary = primary

PROFILE = {
			# primary: +5%/+1
			'CC':  Trait('CC', u"Capacité de Combat"),
			'CT':  Trait('CT', u"Capacité de Tir"),
			'F':   Trait('For',u"Force"),
			'E':   Trait('Res',u"Résistance"),
			'Ag':  Trait('Ag', u"Agilité"),
			'Int': Trait('Int',u"Intelligence"),
			'FM':  Trait('FM', u"Force Mentale"),
			'Soc': Trait('Soc',u"Sociabilité"),
			# secondary: +1/+1
			'A':   Trait('A',  u"Attaques",  False),
			'B':   Trait('B',  u"Blessures", False),
			'Mag': Trait('Mag',u"Magie",     False),
		}

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
	def __init__(self, name, label, description=None, advanced=False, profile=None, skills=None, talents=None, from_=None, next_=None):
		errors = []
		self.name  = name
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
		for k,v in profile.iteritems():
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
		self.from_ = []
		complete(self.from_, from_, CAREERS, errors, "career")
		self.next_ = []
		complete(self.next_, next_, CAREERS, errors, "career")
		if len(errors) > 0:
			print("Career \""+label+"\":\n - "+"\n - ".join(errors))

	def __str__(self):
		res = "" 
		res += self.label
		res += "["+self.name+"]"
		res += u"(carrière "
		if self.advanced:
			res += u"avancée)\n"
		else:
			res += u"de base)\n"
		if (len(self.description) > 0):
			res += self.description+'\n'
		res += profile2str(self.profile)+'\n'
		res += u"Compétences ("+str(len(self.skills))+"): "
		for name in self.skills:
			skill = SKILLS[name]
			res += unicode(skill)+", "
		if len(self.skills) is 0:
			res += u"Aucune"
		else:
			res = res[:-2]
		res += '\n'
		res += u"Talents ("+str(len(self.talents))+"): "
		for name in self.talents:
			talents = TALENTS[name]
			res += unicode(talent)
		if len(self.talents) is 0:
			res += u"Aucun"
		res += '\n'
		return unicode(res)





if __name__ == '__main__':
	career = Career('bat', u"Avoué", profile={'CC':0,'CT':15,'E':5,'B':2, 'TIR':66, 'Soc': 7}, skills=['com','cca','cge'])
	print(u"Carrière: "+unicode(career));

