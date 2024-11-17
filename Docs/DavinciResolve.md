# Davinci Resolve workflow
Creating quilts from video with Davinci Resolve is a great workflow if you want to use video to do real-world capture of lightields.
It allows you to work on the content, center the subject, do color grading, add effects, etc.  
I wrote a script which lets Resolve automatically assemble a quilt after rendering out the frames.

My Resolve workflow is as follows:

### Capturing
Record a video where the camera moves left to right in a steady motion. 
- The video should be at least 30-100 frames long 
- Longer is better, you can always cut or timescale footage
- Shoot wide, you can always crop in
- Shoot landscape, even though the Looking Glass display is portrait. 
  - You don't need much resolution, a single frame on the LKG-Go is 372x662
  - You'll need the width if your subject was not centered all the time
### Davinci Resolve processing
- Import the supplied sample project (see below)
- Or follow these steps  
  - Create a project in Davinci Resolve
    - Click the cog icon in the bottom right corner
    - Check _Use vertical resolution_
    - Set the _Timeline Resolution_ to 372x662 for Looking Glass Go
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
      - Davinci will 
        - Render the frames into a subfolder
        - Assemble the frames into a quilt with the correct parameters in the name  

## Davinci Resolve script setup
Resolve uses python as a scripting language.
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

### Import the sample project

Import this file into Resolve: 
_Davinci Resolve pipeline/Resolve sample project/Green Buddha.dra/project.drp_  
Using this button:  
<img alt="Resolve import.png" src="Resolve_import.png" width="500"/>

