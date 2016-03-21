# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

def double_check(table, new, message):
	try:
		old = table[new.id_]
		print("ERROR: "+new.label+" cannot overwrite "+message+" "+old.label+" (key:\""+old.id_+"\")!")
		return False
	except KeyError:
		return True

from table_skills import SKILL_LIST
SKILLS = OrderedDict()
for skill in SKILL_LIST:
	if double_check(SKILLS, skill, 'skill'):
		SKILLS[skill.id_] = skill

from table_talents import TALENT_LIST
TALENTS = OrderedDict()
for talent in TALENT_LIST:
	if double_check(TALENTS, talent, 'talent'):
		if double_check(SKILLS, talent, 'skill'):
			TALENTS[talent.id_] = talent

from table_careers import CAREER_LIST
CAREERS = OrderedDict()
for career in CAREER_LIST:
	if double_check(CAREERS, career, 'career'):
		if double_check(TALENTS, career, 'talent'):
			if double_check(SKILLS,  career, 'skill'):
				CAREERS[career.id_] = career



#def test_validity(dst, src, general_index, errors, message):
#	src = src or []
#	errors = errors or []
#	for key in src:
#		try:
#			general_index[key]
#			dst.append(key)
#		except KeyError:
#			errors.append("\""+key+"\" is not a valid "+message+" identifier.")
#
#complete(self.skills, skills, SKILLS, errors, "skill")

def get_element_by_label(table, label):
	for k,v in table.items():
		if v.label == label:
			return v
	return None

#def complete_talent(talent):
#	for key,skill in SKILLS.items():
#		found = talent.description.find(skill.label)
#		if found > -1:
#			talent.skills.append(skill.id_)


from tostring import ConsoleToString

if __name__ == '__main__':
	writer = ConsoleToString(SKILLS, TALENTS, CAREERS)
	for k,v in SKILLS.items():
		print("Compétence: "+writer.tostring(v))
	for k,v in TALENTS.items():
#		complete_talent(v)
		print("Talent: "+writer.tostring(v))
	for k,v in CAREERS.items():
		print("Carrière: "+writer.tostring(v))

