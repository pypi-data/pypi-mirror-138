# BZMicroStitcher
## What is BZMicroStitcher?
BZMicroStitcher was created to solve the problem with whole slide scanning using the Keyence BZ-X810 microscope. The problem with this microscope for scanning slides is that the stitching can not be easily automated and the output files are either in a proprietary format that is not compatible with BioFormats or are saved as a .TIFF file which carries with it no important metadata. This package allows the user, with the help of a simple GUI, to automatically stitch/convert their whole slide images into OME-TIFF files for further analysis.

## What type of microscopy is this compatible with?
Currently it is only compatible with brightfield microscopy. Hopefully fluorescence microscopy and Z-stacks will be implemented at some point. Phase contrast images have not been validated.

## I don't use a Keyence Microscope, can I still use BZMicroStitcher?
With the current release there is not a user-friendly way to do this. 
If you need to do some basic stitching for your microscopy work I would suggest using the "Grid/Collection stitching" plugin that comes with [FIJI](https://imagej.net/software/fiji/). 
You can semi-automate this plugin by recording a macro, stitching/saving/closing a single whole slide image, then making copies of that macro and changing any relevant information to make it work correctly.

## Where do I start?
Probably the easiest way to get started would be to download the .YAML file from this page and use it to import an environment into Anaconda.
The next best way would be to use pip from the terminal:
```
pip install BZMicroStitcher
```
## How do I use BZMicroStitcher
**CHANNEL 4 NEEDS TO BE USED FOR SCANNING, BUT THIS MAY CHANGE IN A FUTURE RELEASE**

**1.** Make sure that you save all of your whole slide images into a single directory as shown below. Since the BZ-X810 microscope can scan 3 slides at a time I am going to assume that there is only 3 scanned slides per folder:
```
Slide_Folder
├── SlideList.xlsx
├── SlideGroup-1
│   └── XY01
│   └── XY02
│   └── XY03
├── SlideGroup-2
│   └── XY01
│   └── XY02
│   └── XY03
├── SlideGroup-3
    └── XY01
    └── X...
    └── ....
```
**2. IT MAY BE A GOOD IDEA TO MAKE THIS WHILE SCANNING SLIDES** Make sure that the XLSX file is configured correctly. Please download the example file and use that as a template. 
- Column 1 = slide/sample name. This is what the final OME-TIFF is going to be labeled as and it does not need any file extension.
- Column 2 = The name of the slide group folder that contains the images.
- Column 3 = The XY folder name that contains that specific sample.

**3.** When ready, start your Anaconda environment and/or open a cmd terminal and type:
```
python -m BZMicroStitcher
```
**4.** When the GUI opens, select the MAIN folder that contains each group of scanned slides. Then select the XLSX file which you have created earlier. You can now start stitching.
Unfortunetly, there may not be an indication that anything is happening at this time depending on how large your images are, but over time the final images will be saved to the main folder containing all of the groups.

**5.** When finished, you may close the GUI. :)
