#!/usr/bin/env python3
# Description:	Crontab job generator for task, that need to run every X minutes, where X > 60
# Author:	harloprillar


import re
from datetime import datetime, timedelta
from optparse import OptionParser


pars = OptionParser("usage: %prog -e INTERVAL [options]", add_help_option=False)
pars.add_option("-e", "--every", type="int", dest="interval", help="interval in minutes to run command")
pars.add_option("-c", "--command", type="string", dest="command", default="command", help="command to run")
pars.add_option("-h", "--hour", type="int", dest="start_hour", default=0, help="start hour(default 0)")
pars.add_option("-m", "--minute", type="int", dest="start_min", default=0, help="start minute(default 0)")
(options, args) = pars.parse_args()

if not options.interval:
    pars.print_help()
    raise SystemExit(0)


def add_min(date, min):
    ddate = date + timedelta(minutes=min)
    day, hour, minute = (int(x) for x in re.findall('^[0-9]{4}-[0-9]{2}-([0-9]{2}) ([0-9]{2}):([0-9]{2})', str(ddate))[0])
    return day, hour, minute


date = datetime(1, 1, 1, options.start_hour, options.start_min)
new = add_min(date, 0)
dict_min = {}
i = 0

while 1:
    new = add_min(date, i)
    day, hour, minute = (int(x) for x in new)

    if day == 2:
        break

    if min not in dict_min:
        dict_min[minute] = []

    dict_min[minute].append(hour)
    date = date.replace(hour=hour, minute=minute)
    i = options.interval

for i in dict_min:
    print(str(i) + " " + ",".join(str(x) for x in dict_min[i]) + " * * * " + options.command)

