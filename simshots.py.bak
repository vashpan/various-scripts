#!/usr/bin/python

# This script make periodical screenshots of currently active "iOS Simulator" into given folder

import os, os.path, sys, re, time

from datetime import datetime

def help():
	print "Makes periodical screenshots of currently active 'iOS Simulator' into given folder"
	print ""
	print "Usage:"
	print "%s -p=<period_in_minutes> -d=<target_folder>\n" % (sys.argv[0])

def error(msg=""):
	print "Error: %s" % (msg)
	print ""
	help()
	exit(1)

def takeScreenshot(folder, number):
	screenshotName = datetime.now().strftime("SimShot-%Y_%m_%d-%H_%M_%S.jpg")
	
	print "Taking screenshot [" + str(number) + "]: " + "'" + screenshotName + "'"

	os.system("xcrun simctl io booted screenshot --type=jpeg " + folder + "/" + screenshotName)

# get target folder & period
if len(sys.argv) != 3:
	help()
	exit()

# parse configuration
period = None
folder = None

rx = re.compile('[=]+')
for arg in sys.argv[1:]:
	cmd, value = rx.split(arg)

	# period
	if cmd == '-p':
		period = int(value)

	if cmd == '-d':
		folder = os.path.expanduser(value)

# check if we have proper config
if period == None or folder == None:
	error("incorrect parameters")

if not os.path.exists(folder):
	error("folder does not exists")

# main loop
periodTime = period * 60 # in seconds

print "Taking iOS Simulator screenshots every: " + str(period) + " minutes."
print "Target directory: " + folder
print "Press Ctrl-C to break.\n"

n = 0
while True:
	takeScreenshot(folder, n)
	n += 1

	time.sleep(periodTime)

