# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from copy import deepcopy

def double_check(table, new, message):
	try:
		old = table[new.id_]
		print("ERROR: "+new.label+" cannot overwrite "+message+" "+old.label+" (key:\""+old.id_+"\")!")
		return False
	except KeyError:
		return True

def existence_check(table, message, o, id_):
	try:
		return table[id_]
	except KeyError:
		print("ERROR: career \""+o.label+"\"["+o.id_+"]: "+message+" \""+id_+"\" does not exist.")
		return None

from table_skills import SKILL_LIST
SKILLS = OrderedDict()
for skill in SKILL_LIST:
	if double_check(SKILLS, skill, 'skill'):
		SKILLS[skill.id_] = skill

from table_talents import TALENT_LIST
TALENTS = OrderedDict()
for talent in TALENT_LIST:
	if double_check(TALENTS, talent, 'talent'):
		TALENTS[talent.id_] = talent

def clone_skill(skill, speciality=None):
	print("clone("+str(skill)+")")
	clone = deepcopy(skill)
	if clone.specialized:
		clone.speciality = []
		if speciality is not None:
			clone.speciality.append(speciality)
		clone.specialized = True
	return clone

def load_skills(career, s):
	if type(s) is list:
		print(s.__class__.__name__)
		clones = []
		for id_ in s:
			skill = existence_check(SKILLS,  "skill", career, id_)
			clones.append(clone_skill(skill))
		return [clones]
	elif type(s) is dict:
		print(s.__class__.__name__)
		clones = []
		for id_,speciality in s.items():
			print(id_+":"+speciality)
			skill = existence_check(SKILLS,  "skill", career, id_)
			clones.append(clone_skill(skill, speciality))
		return [clones]
	else:
		print(s.__class__.__name__)
		# skills is a str id
		skill = existence_check(SKILLS,  "skill", career, s)
		if skill is not None:
			return [clone_skill(skill)]
		return []

from table_careers import CAREER_LIST
CAREERS = OrderedDict()
for career in CAREER_LIST:
	if double_check(CAREERS, career, 'career'):
		print(career.label)
		skills = []
		for s in career.skills:
			skills += load_skills(career, s)
		career.skills = skills
		print(str(skills))
		CAREERS[career.id_] = career



from table_skills import SKILL_LIST

def validate_career(career):
	for id_ in career.talents:
		existence_check(TALENTS,"talent", career, id_)
	for id_ in career.before:
		existence_check(CAREERS,"before", career, id_)
	for id_ in career.after:
		existence_check(CAREERS, "after", career, id_)


from tostring import ConsoleToString, PythonToString

if __name__ == '__main__':
	writer = ConsoleToString(SKILLS, TALENTS, CAREERS)
	for k,v in SKILLS.items():
		print("Compétence: "+writer.tostring(v))
	for k,v in TALENTS.items():
		print("Talent: "+writer.tostring(v))
	for k,v in CAREERS.items():
		validate_career(v)
		print("Carrière: "+writer.tostring(v))

