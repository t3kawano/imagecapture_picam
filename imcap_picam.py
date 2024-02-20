# -*- coding: utf-8 -*-
"""
Created on Tue May  8 14:41:49 2018

@author: taizo kawano
"""

#240220 imcap_picam_180516 is used as base
# raspberry pi 3B python2 
#time laps image capture program for pi camera
# just for live image, use console $rapistill -t 0
#rapistill -t 0 -w 640 -h 480 -md 1
#md 7 1 6 2 


import os
import sys
import datetime
import time
import threading
import numpy as np
import cv2
#import tkinter
#import tkinter.filedialog
import Tkinter
import tkFileDialog as filedialog

#import 
import picamera 



class Imagecapture(threading.Thread):
    #framerate frame/sec, maxframe 1min? 
    def __init__(self, interval, maxframe, icg, saveflag = False):
        super(Imagecapture, self).__init__()
        #self.framerate = framerate
        #self.interval = 1/self.framerate
        self.interval = interval
        self.maxframe = maxframe
        self._running = True# used to abort process
        self.closedone = False
        self.icg = icg
        self.saveflag = saveflag
        self.camnum =0
        self.image = None
        
        #self.resolution=(1280, 720)
        #self.resolution=(640, 480)
        self.resolution=(1024, 768)
        #self.shutter_speed = 20000#20 msec
        self.shutter_speed = 40000#40 msec
        
        #camera = picamera.PiCamera(resolution=(1280, 720), framerate=30)
        #self.camera = picamera.PiCamera(resolution=(640, 480), framerate=20)
        #self.camera = picamera.PiCamera(sensor_mode=6,
        #self.camera = picamera.PiCamera(sensor_mode=1,
        #7 is first 1 seems better
        self.camera = picamera.PiCamera(sensor_mode=1,
                                        resolution=self.resolution,
                                        framerate=20)
        #camera.resolution = (1024, 768)
        # Set ISO to the desired value
        #camera.iso = 800
        #self.camera.iso = 400
        self.camera.iso = 100
        #camera.start_preview()
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        #camera.shutter_speed = camera.exposure_speed
        #micro sec usec
        #camera.shutter_speed = 20000#20 msec
        self.camera.shutter_speed = 40000#40 msec
        self.camera.shutter_speed = self.shutter_speed
        self.camera.exposure_mode = 'off'
        #(red, blue) tuple. range 0.0-8.0, typicaly 0.9-1.9
        g = self.camera.awb_gains
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = g


        
        #prep opencv window for preview
        cv2.startWindowThread()
        #WINDOW_NORMAL  need to make flexible size window
        cv2.namedWindow("image", cv2.WINDOW_NORMAL)
        #WINDOW_AUTOSIZE widow size of image
        #cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow("image", 1,1)



    def run(self):    
        starttime = time.time()
        msgstr = "Imagecapture started: "+ str(starttime)
        print(msgstr)
        if not self.saveflag:
            msgstr = "liveimage with "+ str(self.maxframe) +" frames"
            print(msgstr)
            msgstr = "liveflag  "+ str(liveflag)
            print(msgstr)
            #self.icg.writeinlog(msgstr) 
        #capture a frame. some case 1st frame is just black?
        #self.cvcapt.read()
        for i in range(self.maxframe):
            if self._running:
                # Capture frame-by-frame
                #ret, frame = self.cvcapt.read()
                #pi camera capture part
                #capture into opencv format
                # may need python3.x?
                image = np.empty((self.resolution[1] * self.resolution[0] * 3,), dtype=np.uint8)
                self.camera.capture(image, 'bgr')
                image = image.reshape((self.resolution[1],self.resolution[0],3))
                            
                #if ret:            
                if True:            
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    self.image = gray
                    #save image
                    if self.saveflag:
                        self.saveaimage(gray.copy())
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        #(img, text, (position), font, size, color, linewidth,)
                        cv2.putText(gray, str(i+1)+"/"+str(self.maxframe), 
                                    (50,50), font, 1, 255,2)
                
                    # Display the resulting frame
                    cv2.imshow('image',gray)
                    
                    #if True:
                    """
                    if self.icg.booleanvar1.get():
                        self.icg.showhistogram()
                    """
                else:
                    msgstr = "capture failed"
                    print(msgstr)
                    #self.icg.writeinlog(msgstr) 
                    self.abort()
                    


                if liveflag:
                    time.sleep(0.01)
                    pass
                    """
                    #camera.start_preview()
                    if sys.version_info.major == 2:
                        raw_input("wait key")
                    elif sys.version_info.major == 3:
                        input("wait key")
                    else:
                        print("can not detect python version")
                    sys.exit()
                    """
                else:
                    #wait for required frame rate
                    while (time.time()-starttime) < self.interval*(i+1):
                        #if not self.stop_event.is_set():
                        if self._running:                    
                            #wait
                            #without no process, cpu works 100% so wait 10msec
                            #time.sleep(0.01)
                            #100msec? not bad for timing but not much change cpu usage
                            time.sleep(0.01)
                            pass
                        else:
                            #self.shutdown()
                            #ss = None
                            break
                            #return
            else:
                msgstr = "self._running false " + str(time.time())
                print(msgstr)
                #self.icg.writeinlog(msgstr)   
                break
        cv2.destroyAllWindows()
        self.closeprocess()
 
    def saveaimage(self, img):
        timenow = datetime.datetime.now()
        timestr = "{0:%Y%m%d_%H%M%S}_{1}".format(timenow, int(timenow.microsecond/1000))
        #filename = "test{0:05d}.jpg".format(i)
        filename="".join([timestr,'.jpg'])
        #tif format saving seems not work in this way. need fix. it is saved as binary (black/white)image?
        #quality 80? 95? imagej default seems 85
        #cv2.imwrite(self.icg.dirstr+os.sep+filename, img,
        cv2.imwrite(self.icg.targetdir+os.sep+filename, img,
                    [int(cv2.IMWRITE_JPEG_QUALITY),85])
        msgstr = "saved in "+ str(self.icg.targetdir+os.sep+filename)
        print(msgstr)
        #self.icg.writeinlog(msgstr) 
        
    def closeprocess(self):
        """
        if self.cvcapt.isOpened():
            msgstr = "cvcapt isOpened"
            print(msgstr)
            #self.icg.writeinlog(msgstr)
            self.cvcapt.release()
            #cv2.destroyAllWindows()
        """
        self.closedone = True
        endtime = time.time()
        msgstr = "Imagecapture end: "+ str(endtime)
        print(msgstr)
        #self.icg.writeinlog(msgstr)       
        
    def abort(self):
        endtime = time.time()
        msgstr = "Imagecapture aborted: "+ str(endtime)
        print(msgstr)
        #self.icg.writeinlog(msgstr)   
        self._running = False


###############################################
#currently not gui. just drive Imagecapture
#class Imagecaptuergui(tkinter.Frame):
class Imagecaptuergui(Tkinter.Frame):
    
    #ui
    defaultontime = 15
    defaultofftime = 45
    defaultintensity = 50
    defaultcheckboxvale = True
    defaultprogram = "[15,45,50,10],[15,45,100,10]"

    defaultinterval = 2
    defaultslice = 25000
    defaulttempnum = 1
    defaulttempnum2 = 0.5
    
    def __init__(self, interval, slicenumber, master=None, saveflag = False):
        
        Tkinter.Frame.__init__(self, master)
        self.interval = interval
        self.slicenumber = slicenumber
        self.saveflag = saveflag
        self.targetdir = None
        
    def capstart(self):
        """
        #incase the live view is working, stop it before capture
        if not self.startstoptoggle_l:
            self.button_l.config(text=u"Live", bg=self.orignalbuttoncolor_l)
            self.startstoptoggle_l = True
            self.livestop()
            
        #orderstr = "".join(["@",str(channel).zfill(2), "L1"])
        #orderstr = "".join(["@00", "L1"])
        #self.writeinlog("lcg "+"ON "+str(self.getvalues()))
        self.writeinlog("icg "+"start ")
        #self.comm.sendorder(orderstr)
        #self.writeinlog("turnon1 check " )
        #self.intervalstr = self.box1.get()
        #self.slicestr = self.box2.get() 
        #self.dirstr = self.box3.get()
        self.getvalues()
        interval = int(self.intervalstr)
        framerate = 1/interval
        print(framerate)
        slicenumber = int(self.slicestr)
        """        
        if liveflag:
            #time.sleep(0.1)
            pass
            
        else:                    
            tk = Tkinter.Tk()
            tk.withdraw()
            
            #initialdir = "home/pi/programs"
            initialdir = "/media/pi/rpi/"
            
            parentdir = filedialog.askdirectory(initialdir = initialdir)
            print(parentdir)
            
            dirname ="".join([datetime.datetime.now().strftime('%Y%m%d_%H%M%S')])
            
            targetdir = os.path.join(parentdir, dirname)
            self.targetdir = targetdir
            #parent directory
            os.mkdir(targetdir)

        self.ic = Imagecapture(self.interval,self.slicenumber,self,
                               saveflag=self.saveflag)
        self.ic.start()
        
##########################################################


timenow = datetime.datetime.now()
timestr = "{0:%Y%m%d_%H%M%S}_{1}".format(timenow, int(timenow.microsecond/1000))
print(timestr)
print("sys.version_info " + str(sys.version_info))

liveflag = False
saveflag = True

interval = 2
framenum = 10
if liveflag:
    framenum = 100

# live for live imaging
argvs = sys.argv
for arg in argvs:
    print(arg)
if len(argvs) > 1:
    for arg in argvs:
        if arg == "live":
            liveflag = True
            saveflag = False
        # elif arg.isdecimal():#python3
        elif arg.isdigit():#python2
            framenum = int(arg)

print("is live? " + str(liveflag))
    
#sys.exit()

#monitor size
#$xdpyinfo | grep dimensions

#sys.exit()

#sys.exit()

#cvcapt = cv2.VideoCapture(0)
#640x480, 800x600, 1280x960, 1600x1200, 2048x1536

#width
#capwidth = 1280
#height
#capheight = 960

#cvcapt.set(3, capwidth)
#cvcapt.set(4, capheight)

#discard 1st read
#cvcapt.read()

#framerate frame/sec, maxframe 1min? 
#def __init__(self, framerate, maxframe, icg, saveflag = False):
#se capschedularrepeat n times, t delay
icg = Imagecaptuergui(interval, framenum, saveflag = saveflag)
icg.capstart()
#wait captureschedular finishing. otherwise preview window destroyed soon at below.
#ic.join()

print("Imagecapture thread end")











