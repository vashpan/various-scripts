#!/usr/bin/python

from AppKit import NSWorkspace
from AppKit import NSRunningApplication

ws = NSWorkspace.sharedWorkspace()
launchedApps = ws.launchedApplications()

appsToTerminate = []

# find apps, do not close Finder and frontmost app
for app in launchedApps:
	pid = app['NSApplicationProcessIdentifier']
	runningApp = NSRunningApplication.runningApplicationWithProcessIdentifier_(pid)
	
	if runningApp.bundleIdentifier() != 'com.apple.finder' and not runningApp.isActive():
		appsToTerminate.append(runningApp)

# close specified apps
for app in appsToTerminate:
	app.terminate()
	
print '%d apps terminated! Have a nice day!' % len(appsToTerminate)
	