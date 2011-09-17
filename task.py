#!/usr/bin/env python

import sys
import re

taskids = {}
def getid():
  id = chr(ord('A')+len(taskids))
  taskids[id] = 'new'
  return id

def fixdeps(ids):
  rval = []
  scalar = False
  if not isinstance(ids,list):
    scalar = True
    ids = [ids]
  for id in ids:
    if not id.isdigit():
      #rval.append(taskids[id])
      rval.append('$'+id)
    else:
      rval.append(id)
  if scalar:
    return rval[0]
  else:
    return rval

class Task:

  def __init__(self):
    pass

  def from_task(self, line):
    self.parent = ""
    self.depth = 0
    m = re.search('^\\s*(?P<active>[*])?\\s*(?P<id>[0-9]+)\\s+(?P<deps>[0-9,]*)\\s+(?P<desc>.*)$',line)
    if(m):
      self.description = m.group('desc')
      self.id = m.group('id')
      self.delete = False
      if m.group('active'):
        self.active = len(m.group('active')) > 0
      else:
        self.active = False
      depsgroup = m.group('deps')
      if(depsgroup and len(depsgroup) > 0):
        self.deps = m.group('deps').split(',')
      else:
        self.deps = []
    else:
      print 'Unable to parse "%s"' % (line)

  def from_workspace(self, line):
    self.parent = ""
    self.depth = 0
    self.deps = []
    oldsearch = re.search('^(?P<depth>\\s*)(?P<id>[0-9]+)(?P<status>[:*xX]) (?P<desc>.*)$', line)
    newsearch = re.search('^(?P<status>[:*xX])?(?P<depth>\\s*)(?P<desc>.*)$', line)
    if oldsearch:
      m = oldsearch
      self.delete = False
      if m.group('status') == '*':
        self.active = True
      else:
        self.active = False
        if m.group('status') == 'x' or m.group('status') == 'X':
          self.delete = True
      self.description = m.group('desc')
      self.id = m.group('id')
      self.depth = len(m.group('depth'))/2
    else:
      if newsearch:
        m = newsearch
        self.delete = False
        if m.group('status') == '*':
          self.active = True
        else:
          self.active = False
          if m.group('status') == 'x' or m.group('status') == 'X':
            self.delete = True
        self.id = getid()
        self.description = m.group('desc')
        self.depth = len(m.group('depth'))/2
      else:
        print 'Unable to parse "%s"' % (line)

  def __str__(self):
    return "%s%s: %s" % (''.center(self.depth*2,' '), self.id, self.description)

  def depthstring(self):
    return ''.center(self.depth*2,' ')

  def set_depth(self, d, tasks):
    if self.depth < d:
      self.depth = d
    for dep in self.deps:
      tasks[dep].set_depth(d+1, tasks)

def read_from_task(lines):
  tasks = {}
  linenum = 1
  for line in lines:
    if linenum >= 4 and linenum <= len(lines)-2:
      t = Task()
      t.from_task(line)
      tasks[t.id] = t
    linenum = linenum + 1
  for taskid in tasks:
    tasks[taskid].set_depth(0, tasks)
    tasks[taskid].deps.sort()
  return tasks

def read_from_workspace(lines):
  tasks = {}
  linenum = 1
  deps = []
  for line in lines:
    t = Task()
    t.from_workspace(line)
    tasks[t.id] = t
    while t.depth < len(deps):
      deps.pop()
    if len(deps) > 0:
      deps[len(deps)-1].deps.append(t.id)
      t.parent = deps[len(deps)-1].id
    if t.depth >= len(deps):
      deps.append(t)  
    linenum = linenum + 1
  return tasks
