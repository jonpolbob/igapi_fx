import numpy
from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import json
import subprocess as sp
import matplotlib.pyplot as plt
#import os
#import time


import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        
        self.initvideo()
                  

    def initvideo(self):
        #lecture d'une video image par image en python avec ffmpeg
        #avec wxwidgets
        #et sans opencv
        
        
        #lecture des metadata
        #ffmpeg -i <videofile> -f ffmetadata metadata.txt
        filename="C:\\tmp\\Zebrafish_Swimming_SD.avi"
        cmdprobe = r"""c:\program files\ffmpeg\bin\ffprobe.exe""" 
        
        command = [cmdprobe,
                   "-v","quiet",
                   "-print_format","json",
                   "-show_streams",
                   filename,
                   ]
        
        ffprobeOutput = sp.check_output(command).decode('utf-8')
        ffprobeOutput = json.loads(ffprobeOutput)
        
        self.height = ffprobeOutput['streams'][0]['height']
        self.width = ffprobeOutput['streams'][0]['width']
        self.pixfmt = ffprobeOutput['streams'][0]['pix_fmt']
        
        #pipe=sp.Popen(command,stdout = sp.PIPE, bufsize=10**8)
        #b=pipe.communicate()
        print ("-----------------------------")
        print(ffprobeOutput)
        print ("-----------------------------")
        
        cmd = r"""c:\program files\ffmpeg\bin\ffmpeg.exe"""
        
        command = [cmd,
                   "-i",filename,
                   '-f', 'image2pipe',
                   '-pix_fmt','rgb24',
                   '-vcodec','rawvideo',
                   '-']
        
#        if os.name == 'nt' :
#            startupinfo = sp.STARTUPINFO()
#            startupinfo.dwFlags |= sp.STARTF_USESHOWWINDOW
         
        self.pipe=sp.Popen(command,stdout = sp.PIPE, bufsize=10**8)
        self.nbimage=0
        self.encore = True
        self.myobj=0
        self.Bind (wx.EVT_IDLE, self.OnIdle)
    
        
    def OnIdle(self, Event):
        self.nxtimage()

    def nxtimage(self):
            raw_image=self.pipe.stdout.read(self.height*self.width*3)
            image=numpy.fromstring(raw_image, dtype='uint8')
            if len(image) ==self.height*self.width*3:
                image = image.reshape((self.height,self.width,3))
                self.pipe.stdout.flush()
                self.nbimage = self.nbimage+1
                if self.nbimage == 1:
                   self.myobj = plt.imshow(image)
                else:
                   self.myobj.set_data(image)
                #plt.draw()
                
                self.canvas.Refresh()                 
                
                
            else:
                self.encore =0
            
        

if __name__ == "__main__":
    app = wx.App()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    fr.Show()
    app.MainLoop()
