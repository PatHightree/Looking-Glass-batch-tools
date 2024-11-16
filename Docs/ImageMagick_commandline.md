# Image Magick commandline

These scripts aren't the best, but they served me well at the time...  
[Looking Gloves](https://lookinggloves.vercel.app) is a great online tool to convert your quilts

These scripts use Image Magick to assemble image sequences into quilts and back  
They have the following requirements:
- Download and install Image Magick from https://imagemagick.org/script/download.php
- Add the folder containing these scripts to your _Path_ environment variable
- The images must be named tile_000 and their sequence number be padded to 3 digits 

Note: if you cancel the processing of a quilt with ctrl-c, Image Magick will leave large temp files in your Windows temp folder 

