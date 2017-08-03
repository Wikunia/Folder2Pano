# Folder2Pano

You took thousands of photos on your last vacation and you also love taking panoramas?
Unfortunately your panorama mode on the camera isn't perfect so you take all your shots manually
and have to stitch them together afterwards, right?

This project does everything for you.
Steps you normally have to do:
- Find all the single photos
- Import them into a stitching program
- Align them
- Save the panorama

This takes time and is quite boring task to do. I thought it should be possible to automate this task.
I used [hugin](http://hugin.sourceforge.net) as a panorama stitcher before. Luckily they have an option to 
use the command line instead of a GUI. 
The first part is to find all the single photos. Therefore, I wrote this little program with python.

## Requirements
You need [opencv](http://opencv.org), [hugin](http://hugin.sourceforge.net) and a shell.

Install the python requirements using:

`pip install -r requirements.txt`

The shell script `pano.sh` needs to be executable.

I tested the script on arch linux and everything I needed was already on my laptop for other projects. 
If you find something missing in this list of requirements => Please open an issue!

## Usage

At the moment you have to be in this folder to start the programm.

`python get_panos.py FOLDER`

The program iterates over all jpeg files and reads the exif data.
Only photos taken in manual mode with the same aperture,focal length,exposure time and iso are considered for a panorama.

Let's assume we have these photos:
- 001.jpg - Manual    f8 1/60s 28mm 160 ISO
- 002.jpg - Automatic f22 1/200s 28mm 160 ISO
- 003.jpg - Manual    f8 1/50s 28mm 160 ISO
- 004.jpg - Manual    f8 1/50s 28mm 160 ISO
- 005.jpg - Manual    f8 1/50s 28mm 160 ISO
- 006.jpg - Manual    f10 1/50s 28mm 160 ISO

Then the photos 003-005 would be considered as one panorama. 

After executing the script you would have a new folder.

`003-005` in your folder (the folder of this script). Hugin would create a `003-005.pto` file and at the end a
`003-005.jpg` panorama.

Of course it isn't always the case that you only shot panoramas if you have the same settings. 
That's the reason why the python script itself uses `opencv` to check whether a panorama is reasonable before the hugin script is called.

## Example
![pano](https://user-images.githubusercontent.com/4931746/28912928-7c170610-7836-11e7-8939-e2c53d9f0459.png)


Generates:
![p1070113-p1070122_small](https://user-images.githubusercontent.com/4931746/28912291-f7fd6006-7833-11e7-86b4-ceb0120c901b.jpg)







