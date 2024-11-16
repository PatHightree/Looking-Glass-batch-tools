# Looking Glass batch tools
<img align="right" src="Docs/Nixie8_qs5x9a0.5625.jpg" width="150"/>  

In this repo you will find some tools with which to create lightfield quilts for Looking Glass holographic displays.  
A Quilt is an image like the one on the right, that is composed of many (50-100) images which show the subject from a range of different perspectives.  
This is the resulting [hologram](https://blocks.glass/pathightree/111590)

## Davinci Resolve
Creating quilts with Davinci Resolve is a great workflow if you want to use video to do real-world capture of lightields.  
This workflow creates quilts straight from Resolve.  
Resolve uses python as a scripting language.

[Davinci Resolve workflow and script](Docs/DavinciResolve.md)

## Image Magick commandline
These scripts use Image Magick to assemble image sequences into quilts and back  
They are a bit rough, but they served me well at the time...  
I would suggest using [Looking Gloves](https://lookinggloves.vercel.app) instead to convert your quilts

[Image Magick commandline scripts](Docs/ImageMagick_commandline.md)