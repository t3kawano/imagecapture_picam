# imagecapture_picam


## Overview
imcap_picam will save timelapse images taken by Raspberry Pi camera on USB drive. 

This code was written for image capture step of the Rapid C. elegans motion imaging (Remi) system.

## Requirement
 - Raspberry Pi 3B
 - Raspberry Pi Camera V2
 - USB drive
 - python2

## Usage
Prepare a USB drive formatted as exfat and named rpi. It should be mounted at `/media/pi/rpi/`. 

To capture 25,000 frame images, run the follwoing line on the terminal. 

```shell
$ imcap_picam 25000
```

It will show folder chooser to set USB drive for saving images.

You can preview how look like without saving image by; 

```shell
$ imcap_picam live
```

However, following is easier for sample positioning.

```shell
$ raspistill -t 0
```

You can see the live view, and press `ctr+c` to stop the live view.

<!-- ## Features -->

## Reference
Kawano, Taizo et al. “ER proteostasis regulators cell-non-autonomously control sleep.” Cell reports vol. 42,3 (2023): 112267. doi: 10.1016/j.celrep.2023.112267

## Licence
MPL-2.0
