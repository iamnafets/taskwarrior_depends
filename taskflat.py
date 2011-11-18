#!/usr/bin/env python

import sys
import re
from task import *
import random

def list_difference(list1, list2):
  """uses list1 as the reference, returns list of items not in list2"""
  diff_list = []
  for item in list1:
    if not item in list2:
      diff_list.append(item)
  return diff_list

existingfilename = sys.argv[1]
existingfile = open(existingfilename, 'r')
existinglines = existingfile.readlines()
existingtasks = read_from_task(existinglines)

lines = sys.stdin.readlines()
tasks = read_from_workspace(lines)

# Create new tasks
idplaceholders = taskids.keys()
idplaceholders.sort()

for id in idplaceholders:
  task = tasks[id]
  if task.parent == "":
    print task.id+'=`task add %s %s | grep "^Created" | grep -o "[0-9]\\\\+"`' % (task.description, ' '.join(sys.argv[2:]))
  else:
    print task.id+'=`taskbreak %s %s | grep "^Created" | grep -o "[0-9]\\\\+"`' % (fixdeps(task.parent), task.description)

# Update existing tasks
for newtask in tasks:
  if tasks[newtask].id.isdigit():
    if existingtasks[newtask].description != tasks[newtask].description:
      print 'echo Y | task %s %s' % (newtask, tasks[newtask].description)
    if existingtasks[newtask].active != tasks[newtask].active:
      if tasks[newtask].active:
        print 'task start %s' % (newtask)
      else:
        print 'task stop %s' % (newtask)
    if tasks[newtask].delete:
      print 'taskdone %s' % (newtask)
    if newtask in existingtasks:
      deldeps = list_difference(existingtasks[newtask].deps, fixdeps(tasks[newtask].deps))
      if(len(deldeps)>0):
        for dep in deldeps:
          print 'task %s dep:-%s' % (newtask, dep)
      newdeps = list_difference(fixdeps(tasks[newtask].deps), existingtasks[newtask].deps)
      if(len(newdeps)>0):
        for dep in newdeps:
          print 'task %s dep:+%s' % (newtask, dep)
 
# Delete old tasks
for oldtask in existingtasks:
  if not oldtask in tasks:
    print 'echo y | task delete %s' % (oldtask)

for taskid in tasks:
  task = tasks[taskid]
  #print task
