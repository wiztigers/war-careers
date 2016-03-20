# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sys import version_info
PYTHON3 = version_info > (3,)

def _tostring(expr):
	if PYTHON3:
		return str(expr)
	else:
		return unicode(expr)

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
		raise Exception("Unsupported type "+x.__class__.__name__)

	def skill2string(self, skill):
		res = "" 
		res += skill.label
		res += "["+skill.id_+"]"
		if skill.specialized:
			res += '('
			if skill.speciality is not None:
				res += skill.speciality
			else:
				res += "au choix"
			res += ')'
		return _tostring(res)

	def talent2string(self, talent):
		res = "" 
		res += talent.label
		res += "["+talent.id_+"]"
		return _tostring(res)

	def career2string(self, career):
		res = "" 
		res += career.label
		res += "["+career.id_+"]"
		res += "(carrière "
		if career.advanced:
			res += "avancée)\n"
		else:
			res += "de base)\n"
		if (len(career.description) > 0):
			res += career.description+'\n'
		res += self.profile2string(career.profile)+'\n'
		res += "Compétences ("+str(len(career.skills))+"): "
		for id_ in career.skills:
			skill = self.SKILLS[id_]
			res += self.skill2string(skill)+", "
		if len(career.skills) is 0:
			res += "Aucune"
		else:
			res = res[:-2]
		res += '\n'
		res += "Talents ("+str(len(career.talents))+"): "
		for id_ in career.talents:
			talents = self.TALENTS[id_]
			res += self.talent2string(talent)
		if len(career.talents) is 0:
			res += "Aucun"
		res += '\n'
		return _tostring(res)

	def profile2string(self, profile):
		res = ''
		for k in profile.keys():
			res += '|{:3}'.format(k)
		res += '|\n---------------------------------------------\n|'
		for v in profile.values():
			res += ' {:<2}|'.format(v)
		return res


