# Davinci Resolve
Creating quilts with Davinci Resolve is a great workflow if you're doing real-world capture of lightields.  
This workflow creates quilts straight from Resolve.

My Resolve workflow is as follows:
- Record a video where the camera moves left to right in a steady motion. 
  - The video should be at least 50-100 frames long 
  - Longer is better, you can always cut or timescale footage
  - Shoot wide, you can always crop in
  - Shoot landscape, even though the Looking Glass display is portrait, you will need the width
- Create a project in Davinci Resolve
  - Set the _Timeline Resolution_ to 372x662 for Looking Glass Go
  - Check _Use vertical resolution_
- Create a timeline with the footage
  - Center the footage in the frame (this doesn't have to be perfect)
    - Center the subject at the start of the clip and set a keyframe for the position
    - Center the subject in the middle of the clip and set a keyframe for the position
    - Center the subject in the end of the clip and set a keyframe for the position
  - Make something beautiful
- Go to the Deliver page
  - Set _File name_ and _Location_
  - Set _Format_ to JPEG
  - Go to the _Advanced settings_ section
    - Check _trigger script at_
    - Select _End_
    - Select _resolve_assemble_quilt_pil_
    - Render the clip
    - Davinci will render the clip

## Installation
### Install Python
    Download and install Python from https://www.python.org/downloads/
### Install pillow
Pillow is a Windows version of PIL (Python Image Library) which is used to create the quilt

    Open a command prompt and enter "pip3 install pillow"
    You might need to open the command prompt with admin rights
### Put the python script in Resolve's special folder
resolve_assemble_quilt_pil.py is the script that will create the quilt after Resolve has rendered the frames 

    The script must be placed in the following folder:
    Windows:    %ProgramData%/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
                (or %APPDATA%/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver depending on installation)
    Mac OS X:   ~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
    Linux:      /opt/resolve/Fusion/Scripts/Deliver/
                (or /home/resolve/Fusion/Scripts/Deliver depending on installation)

