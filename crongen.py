#!/usr/bin/env python3
# Description:	Crontab job generator for task, that need to run every X minutes, where X > 60
# Author:	harloprillar

import sys, re
from datetime import time, datetime, timedelta
from optparse import OptionParser


pars = OptionParser("usage: %prog -e INTERVAL [options]", add_help_option=False)
pars.add_option("-e", "--every", type="int", dest="interval", help="interval in minutes to run command")
pars.add_option("-c", "--command", type="string", dest="command", default="command", help="command to run")
pars.add_option("-h", "--hour", type="int", dest="start_hour", default=0, help="start hour(default 0)")
pars.add_option("-m", "--minute", type="int", dest="start_min", default=0, help="start minute(default 0)")
(options,args) = pars.parse_args()

if not options.interval:
  pars.print_help()
  raise SystemExit(0)

def addMin(date, min):
  ddate = date + timedelta(minutes=min)
  m = re.search('^[0-9]{4}-[0-9]{2}-([0-9]{2}) ([0-9]{2}):([0-9]{2})', str(ddate))
  day = m.group(1)
  hour = m.group(2)
  min = m.group(3)
  return day, hour, min

date = datetime(1,1,1,options.start_hour,options.start_min)
new = addMin(date, 0)
dict_min = {}
dict_min[options.start_min] = []
dict_min[options.start_min].append(options.start_hour)

while 1:
  new = addMin(date, options.interval)
  day = int(new[0])
  hour = int(new[1])
  min = int(new[2])
  if day == 2: break 
  date = date.replace(hour=hour, minute=min)
  if not min in dict_min: dict_min[min] = []
  dict_min[min].append(hour)

for i in dict_min:
  print( str(i) + " " + ",".join(str(x) for x in dict_min[i]) + " * * * " + options.command )

