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

Then the photos 002-005 would be considered as one panorama. 

After executing the script you would have a new folder.

`001-005` in your folder (the folder of this script). Hugin would create a `001-005.pto` file and at the end a
`001-005.jpg` panorama.

Of course it isn't always the case that you only shot panoramas if you have the same settings. 
That's the reason why the python script itself uses `opencv` to check whether a panorama is reasonable before the hugin script is called.

## Example
![p1070113](https://user-images.githubusercontent.com/4931746/28912302-0808d908-7834-11e7-99b1-4e0f8ec6b230.jpg)
![p1070114](https://user-images.githubusercontent.com/4931746/28912303-080c5ad8-7834-11e7-8f17-eabb282d5db3.jpg)
![p1070115](https://user-images.githubusercontent.com/4931746/28912304-0816380a-7834-11e7-9d03-714d018a68f7.jpg)
![p1070116](https://user-images.githubusercontent.com/4931746/28912305-0816d846-7834-11e7-812e-4ed8604d14fe.jpg)
![p1070117](https://user-images.githubusercontent.com/4931746/28912306-081af3ea-7834-11e7-815d-1bc477bbf57c.jpg)
![p1070118](https://user-images.githubusercontent.com/4931746/28912307-081f5138-7834-11e7-8745-a72b4de59d9d.jpg)
![p1070119](https://user-images.githubusercontent.com/4931746/28912308-08282308-7834-11e7-94ae-7cdc041eb991.jpg)
![p1070120](https://user-images.githubusercontent.com/4931746/28912309-082d38b6-7834-11e7-8b39-d6bb23df7b23.jpg)
![p1070121](https://user-images.githubusercontent.com/4931746/28912310-0834c162-7834-11e7-8b6b-6e9b50966962.jpg)
![p1070122](https://user-images.githubusercontent.com/4931746/28912311-0837eca2-7834-11e7-9869-d34854eae238.jpg)

Generates:
![p1070113-p1070122_small](https://user-images.githubusercontent.com/4931746/28912291-f7fd6006-7833-11e7-86b4-ceb0120c901b.jpg)







