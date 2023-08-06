<!-- sound to image image to sound python package  -->

# Soundviewer

python package for converting sound to image and image to sound.

for now sound to image is only available.

![](https://c.tenor.com/5eU8wSWY8zkAAAAC/wow-cool.gif)


## Installation

```bash
pip3 install 'git+https://github.com/emingenc/soundviewer.git'

# Or, to install it from a local clone:
git clone +https://github.com/emingenc/soundviewer.git
pip3 install -e soundviewer
```

## Getting Started

### run from local clone

```bash
cd soundviewer
pip3 install -r requirements.txt


python3 -m soundviewer.sound2image --input sample_data/thermo.wav --show

or

python3 soundviewer/sound2image.py --input sample_data/thermo.wav --show 

```

if you want to save without showing the image, remove --show

or with --output flag you can specify custom name and spesific path

### use it on your python script

```python3
import soundviewer
sound_path = 'sample_data/thermo.wav'
soundviewer.sound2image.save_image_from_sound(sound_path)
```
this will save thermo.jpg to your working directory

if you want you can specifiy the output path and image name `soundviewer.sound2image(sound_path,output='./test.jpg')`

here is the output image for sample data thermo.wav

![sound to image](https://raw.githubusercontent.com/emingenc/soundviewer/master/sample_data/thermo.jpg)






wav source : https://people.math.sc.edu/Burkardt/data/wav/thermo.wav