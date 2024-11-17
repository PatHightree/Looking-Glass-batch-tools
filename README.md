# Looking Glass batch tools
<img align="right" src="Docs/Nixie8_qs5x9a0.5625.jpg" width="150"/>  

In this repo you will find some tools and workflows with which to create lightfield quilts for Looking Glass holographic displays.  
A Quilt is an image like the one on the right, that is composed of many (30-100) images which show the subject from a range of different perspectives.  
The result can be posted and shared on the [Blocks](https://blocks.glass/pathightree/111590) website.

## Davinci Resolve
Creating quilts from video with Davinci Resolve is a great workflow if you want to use video to do real-world capture of lightields.
It allows you to work on the content, center the subject, do color grading, add effects, etc.  
This workflow lets Resolve automatically assemble a quilt after rendering out the frames.

[Davinci Resolve workflow and script](Docs/DavinciResolve.md)

## Image Magick
These commandline scripts use Image Magick to assemble image sequences into quilts and back.  
They are pretty rough, but they served me well at the time...  
I would suggest using [Looking Gloves](https://lookinggloves.vercel.app) instead to convert image sequences to quilts.

[Image Magick commandline scripts](Docs/ImageMagick_commandline.md)