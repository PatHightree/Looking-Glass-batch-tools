#!/usr/bin/env python

"""
    This script must be placed in the following folder:
    Windows:    %ProgramData%/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
                (or %APPDATA%/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver depending on installation)
    Mac OS X:   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
    Linux:      /opt/resolve/Fusion/Scripts/Deliver/
                (or /home/resolve/Fusion/Scripts/Deliver depending on installation)

    Installing python requirements:
    - Install python (this script was developed with 3.12 on windows)
    - Install PIL
        - On windows run the following from an admin commandline
          pip3 install pillow

    Configuring Davinci to use the script:
    - Go to the Deliver page
    - Under RenderSettings select Video
    - Under AdvancedSettings
        - Check TriggerScriptAt
        - Set combo box to End
        - Set combo box to assemble
    Notes:
        The project will not retain this setting, has to be applied each session
        This script is incompatible with the File/FileSubfolder option, it will create a subfolder automatically

    Output can be read on the console, found in the pull-down menu under Workspace/Console

    This trigger script will receive the following 3 global variables:
    "job" : job id.
    "status" : job status
    "error" : error string (if any)
"""

import time
import os
import shutil
from math import ceil
from PIL import Image
from PIL import ImageShow
from DisplayInBridge import BridgePreview, Playlist

def getJobDetailsBasedOnId(project, jobId):
    jobList = project.GetRenderJobList()
    for jobDetail in jobList:
        if jobDetail["JobId"] == jobId:
            return jobDetail
    return ""

time.sleep(2)

# Explore Resolve
# print('job properties')
# pprint.pp(jobs[-1])
# print('job status properties')
# detailedStatus = project.GetRenderJobStatus(job)
# pprint.pp(detailedStatus)

# Collect prerequisites
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
# timeline = project.GetCurrentTimeline()
# timelineName = timeline.GetName()
# jobs = project.GetRenderJobList()
# targetDir = jobs[-1]['TargetDir']
# filename = jobs[-1]['OutputFilename']

jobDetail = getJobDetailsBasedOnId(project, job)
targetDir = jobDetail['TargetDir']
targetDir = targetDir.replace("\\", "/")
filename = jobDetail['OutputFilename']

# Clean up filename, strip extension, numbering, _
filename = filename[:-4]
filename = filename.rstrip('0')
filename = filename.rstrip('_')

# Create our own subfolder for the frames, as we can't read the SubFolder property from Resolve
newTargetDir = targetDir+"/"+filename
if not os.path.exists(newTargetDir):
    os.makedirs(newTargetDir)

# Move rendered frames into subfolder
print('Moving files to '+newTargetDir)
files = os.listdir(targetDir)
framePaths = []
for x in files:
    if x.startswith(filename) and x.endswith(".jpg"):
        src = targetDir+"/"+x
        dst = newTargetDir+"/"+x
        if os.path.isfile(dst):
            os.remove(dst)
        shutil.move(src, newTargetDir)
        framePaths.append(dst)

frameCount = jobDetail['MarkOut'] - jobDetail['MarkIn'] + 1
rows = 6
columns = int(frameCount/rows)+1

# Read frames into memory
frames = []
width = 0
height = 0
for framePath in framePaths:
    im = Image.open(framePath)
    frames.append(im)
    width, height = im.size

# Assemble quilt
rows = 5
columns = ceil(len(frames)/rows)
aspect = 9/16
quilt = Image.new('RGB', (width*columns, height*rows))
print(f"Frame size {width}x{height} {rows} rows, {columns} columns => quilt size {quilt.size}")
i = 0
for y in reversed(range(0, height*rows, height)):
    for x in range(0, width*columns, width):
        if i<len(frames):
            quilt.paste(frames[i], (x, y))
        i += 1

# Write quilt
quiltPath = f"{newTargetDir}/{filename}_qs{columns}x{rows}a{aspect}.jpg"
print(f"Writing to {quiltPath}")
if os.path.isfile(quiltPath):
    os.remove(quiltPath)
quilt.save(quiltPath)

# Display result on monitor
# ImageShow.show(quilt)

# Display result on Looking Glass
bp = BridgePreview()
bp.connect_to_bridge()
pl = Playlist("Preview", False)
pl.add_quilt_item(quiltPath, rows, columns, aspect, rows*columns)
bp.bridge.try_play_playlist(pl)
time.sleep(10)
bp.bridge.try_show_window(False)