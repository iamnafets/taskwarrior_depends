#!/usr/bin/env python

import sys
import re
from task import *

def printtask(task, tasks):
  print '%s%s%s %s' % (task.depthstring(), task.id, '*' if task.active else ':', task.description)
  if len(task.deps) > 0:
    for dep in task.deps:
      printtask(tasks[dep], tasks)

lines = sys.stdin.readlines()
tasks = read_from_task(lines)

for taskid in tasks:
  task = tasks[taskid]
  if task.depth == 0:
    printtask(task, tasks)
