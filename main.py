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

def clone(skill, speciality=None):
	clone = deepcopy(skill)
	if clone.specialized:
		clone.speciality = []
		if speciality is not None:
			clone.speciality.append(speciality)
		clone.specialized = True
	return clone

def append(clones, found, id_, message):
	if found is not None:
		clones.append(clone(found))
	else:
		print("ERROR: "+message+" \""+id_+"\" not found")

from tostring import _isstring
def load(table, message, career, o):
	clones = []
	if type(o) is list:
		for id_ in o:
			clones += load(table,message, career, id_)
		return [clones]
	elif type(o) is dict:
		for id_,speciality in o.items():
			found = existence_check(table,message, career, id_)
			if found is not None:
				if type(speciality) is list:
					for spe in speciality:
						clones.append(clone(found, spe))
				else:
					clones.append(clone(found, speciality))
			else:
				print("ERROR: "+message+" \""+id_+"\" not found")
		return [clones]
	elif _isstring(o):
		found = existence_check(table,message, career, o)
		append(clones, found, o, message)
		return clones
	else:
		print("ERROR: unsupported type for "+type(o).__name__)

def load_tables(career):
	tmp = []
	for o in career.skills:
		tmp += load(SKILLS,"skill", career, o)
	career.skills = tmp
	tmp = []
	for o in career.talents:
		tmp += load(TALENTS,"talent", career, o)
	career.talents = tmp

from table_careers import CAREER_LIST
CAREERS = OrderedDict()
for career in CAREER_LIST:
	if double_check(CAREERS, career, 'career'):
		load_tables(career)
		CAREERS[career.id_] = career



from table_skills import SKILL_LIST

def validate_career(career):
	for id_ in career.before:
		other = existence_check(CAREERS,"before", career, id_)
		if other is not None:
			if career.id_ not in other.after:
				other.after.append(career.id_)
				#print("ERROR: shouldn't \""+career.label+"\"["+career.id_+"] be added after \""+other.label+"\" ["+id_+"]?")
	for id_ in career.after:
		other = existence_check(CAREERS, "after", career, id_)
		if other is not None:
			if career.id_ not in other.before:
				other.before.append(career.id_)
				#print("ERROR: shouldn't \""+career.label+"\"["+career.id_+"] be added before \""+other.label+"\" ["+id_+"]?")


from tostring import AsciidocToString, PythonToString

if __name__ == '__main__':
	writer = AsciidocToString(SKILLS, TALENTS, CAREERS)
#	for k,v in SKILLS.items():
#		print("Compétence: "+writer.tostring(v))
#	for k,v in TALENTS.items():
#		print("Talent: "+writer.tostring(v))
	for k,v in CAREERS.items():
		validate_career(v)
		print(writer.tostring(v))

#	print("----------")
#	with open('WH2-carrières.html') as f:
#		contents = f.read()
#	from bshtmlparse import parse_html
#	CAREERS = parse_html(contents)
#	writer = PythonToString(SKILLS, TALENTS, CAREERS)
#	for k,v in CAREERS.items():
#		print(writer.tostring(v))

