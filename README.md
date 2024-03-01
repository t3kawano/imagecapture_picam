# imagecapture_picam


## Overview
imcap_picam will save timelapse images taken by Raspberry Pi camera on USB drive. 

This code was written for image capture step of the Rapid C. elegans motion imaging (Remi) system.

## Requirement
 - Raspberry Pi 3B
 - Raspberry Pi Camera V2
 - USB drive
 - python2

## Installation
Put the `imcap_picam.py` into raspberry pi. User home directory is better location for easy use.

## Usage
Prepare a USB drive formatted as exfat and named rpi. It should be mounted at `/media/pi/rpi/`. 

To capture 25,000 frame images, run the following line on the terminal. 

```shell
$ python imcap_picam.py 25000
```

It will show folder chooser to set USB drive for saving images.

You can preview how look like without saving image by; 

```shell
$ python imcap_picam.py live
```

However, following is easier for sample positioning.

```shell
$ raspistill -t 0
```

You can see the live view, and press `ctr+c` to stop the live view.

<!-- 
## Note
## Features 
## Author -->

## Reference
Kawano, Taizo et al. “ER proteostasis regulators cell-non-autonomously control sleep.” Cell reports vol. 42,3 (2023): 112267. [doi: 10.1016/j.celrep.2023.112267](https://doi.org/10.1016/j.celrep.2023.112267)

## License
MPL-2.0
