#!/usr/bin/env python

"""
	This script must be placed in the following folder:
    Mac OS X:   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
    Windows:    %APPDATA%/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver/
    Linux:      /opt/resolve/Fusion/Scripts/Deliver/   (or /home/resolve/Fusion/Scripts/Deliver depending on installation)

	Configuring Davinci to use the script:
	- Go to the Deliver page
	- Under RenderSettings select Video
	- Under AdvancedSettings
		- Check TriggerScriptAt
		- Set combo box to End
		- Set combo box to assemble
	Warning : The File/FileSubfolder option is not compatible with this script

	Output can be read on the console, found in the pull-down menu under Workspace/Console

    Davinci will trigger this script and supply it with the following global variables:
    "job" : job id.
    "status" : job status
    "error" : error string(if any)
"""

import time
import os
import DaVinciResolveScript as dvr_script

def getJobDetailsBasedOnId(project, jobId):
    jobList = project.GetRenderJobList()
    for jobDetail in jobList:
        if jobDetail["JobId"] == jobId:
            return jobDetail
    return ""


print('Starting quilt assembly')
time.sleep(2)

# Collect prerequisites
resolve = dvr_script.scriptapp("Resolve")
fusion = resolve.Fusion()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
# timeline = project.GetCurrentTimeline()
# timelineName = timeline.GetName()
# jobs = project.GetRenderJobList()
# targetDir = jobs[-1]['TargetDir']
# filename = jobs[-1]['OutputFilename']

jobDetail = getJobDetailsBasedOnId(project, job)
targetDir = jobDetail['TargetDir']
filename = jobDetail['OutputFilename']

print('Target folder ' + targetDir)
print('OutputFilename ' + filename)

# print('job properties')
# pprint.pp(jobs[-1])
# print('job status properties')
# detailedStatus = project.GetRenderJobStatus(job)
# pprint.pp(detailedStatus)

# Strip extension
filename = filename[:-4]
# Strip numbering
filename = filename.rstrip('0')
# Strip _
filename = filename.rstrip('_')

os.chdir(targetDir)
cmd = 'assemble_jpg \"' + filename + '_\" 5 10 \"' + filename + '\"'
print('Command ' + cmd)
os.system(cmd)
print('Finished quilt assembly')