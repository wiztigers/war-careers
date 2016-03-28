﻿# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sys import version_info
PYTHON3 = version_info > (3,)

def _tostring(expr):
	if PYTHON3:
		return str(expr)
	else:
		return unicode(expr)

def _isstring(o):
	if PYTHON3:
		return type(o) is str
	else:
		return type(o) is unicode

class ConsoleToString(object):
	def __init__(self, skills, talents, careers):
		self.SKILLS  = skills
		self.TALENTS = talents
		self.CAREERS = careers

	def tostring(self, x):
		if x.__class__.__name__ == 'Skill':
			return self.skill2string(x)
		if x.__class__.__name__ == 'Talent':
			return self.talent2string(x)
		if x.__class__.__name__ == 'Career':
			return self.career2string(x)
		if x.__class__.__name__ == 'Source':
			return self.source2string(x)
		raise Exception("Unsupported type "+x.__class__.__name__)

	def skill2string(self, o):
		return self.unwrapped(o, 'Skill', self._skill2string)

	def _skill2string(self, skill):
		res = "" 
		res += skill.label
		res += "["+skill.id_+"]"
		if skill.specialized:
			res += '('
			if len(skill.speciality) > 0:
				for spe in skill.speciality:
					res += spe + ", "
				res = res[:-2]
			else:
				res += "au choix"
			res += ')'
		return _tostring(res)

	def talent2string(self, o):
		return self.unwrapped(o, 'Talent', self._talent2string)

	def unwrapped(self, o, type_, tostringmethod):
		res = ""
		if type(o).__name__ == type_:
			res += tostringmethod(o)
		elif type(o) is list:
			for item in o:
				res += self.unwrapped(item, type_, tostringmethod)+" ou "
			res = res[:-4]
		else:
			raise Exception("Unsupported "+type_+" type: "+o.__class__.__name__)
		return res

	def _talent2string(self, talent):
		res = "" 
		res += talent.label
		res += "["+talent.id_+"]"
		if talent.specialized:
			res += '('
			if len(talent.speciality) > 0:
				for spe in talent.speciality:
					res += spe + ", "
				res = res[:-2]
			else:
				res += "au choix"
			res += ')'
		return _tostring(res)

	def modifier2string(self, modifier):
		res = ""
		if modifier.trait is not None:
			res += modifier.trait
		elif modifier.skill is not None:
			res += modifier.skill
		else:
			res += '?'
		if modifier.value >= 0:
			res += "+"
		res += _tostring(modifier.value)
		res += ' '
		if modifier.condition is not None:
			res += modifier.condition
		return res

	def career2string(self, career):
		res = "" 
		res += career.label
		res += "["+career.id_+"]"
		res += "(carrière "
		if career.advanced:
			res += "avancée)"
		else:
			res += "de base)"
		if career.source is not None:
			res += ' '+self.source2string(career.source)
		res += '\n'
		if (len(career.description) > 0):
			res += career.description+'\n'
		res += self.profile2string(career.profile)+'\n'
		res += "Compétences("+str(len(career.skills))+"): "
		for item in career.skills:
			res += self.skill2string(item)+", "
		if len(career.skills) is 0:
			res += "Aucune"
		else:
			res = res[:-2]
		res += '\n'
		res += "Talents("+str(len(career.talents))+"): "
		for item in career.talents:
			res += self.talent2string(item)+", "
		if len(career.talents) is 0:
			res += "Aucun"
		else:
			res = res[:-2]
		res += '\n'
		return _tostring(res)

	def source2string(self, source):
		return "[%s (%s), page %s]"%(source.document, source.get_edition(), source.page)

	def profile2string(self, profile):
		res = ''
		for k in profile.keys():
			res += '|{:3}'.format(k)
		res += '|\n---------------------------------------------\n|'
		for v in profile.values():
			res += ' {:<2}|'.format(v)
		return res



class PythonToString(object):
	def __init__(self, skills, talents, careers):
		self.SKILLS  = skills
		self.TALENTS = talents
		self.CAREERS = careers

	def tostring(self, x):
		if x.__class__.__name__ == 'Career':
			return self.career2string(x)
		if x.__class__.__name__ == 'Source':
			return self.source2string(x)
		raise Exception("Unsupported type "+x.__class__.__name__)

	def career2string(self, career):
		res = "Career('%s', \"%s\", advanced=%s"%(career.id_, career.label, career.advanced)
		res += ",\nprofile=%s"%(self.profile2string(career.profile))
		res += ",\nskills=%s"%(career.skills)
		res += ",\ntalents=%s"%(career.talents)
		res += ",\nbefore=%s"%(career.before)
		res += ",\nafter=%s"%(career.after)
		if career.description is not None:
			res += ",\ndescription=\"%s\""%(career.description)
		if career.source is not None:
			res += ",\nsource=%s"%(self.source2string(career.source))
		return res+"),\n"

	def source2string(self, source):
		return 'Source("%s", %s)'%(source.document, source.get_edition(), source.page)

	def profile2string(self, profile):
		res = "{ "
		for k,v in profile.items():
			if v > 0:
				res += "'%s':%s,"%(k,v)
		return res + " }"

	def idlist2string(self, ids):
		res = "[ "
		for i in ids:
			res += "'%s',"%(i)
		return res + " ]"

